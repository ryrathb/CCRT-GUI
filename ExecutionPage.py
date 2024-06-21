import tkinter as tk
from tkinter import ttk  # For dropdown menus
from models.Batter import Batter 
from models.Rep import Rep 
from models.Routine import Routine
from models.Set import Set
import random
from datetime import datetime
import socket 
import threading
import time

class ExecutionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.batter = None
        self.routine = None
        self.free_use = False

        self.start_button_pressed = False
        self.cont_limit = 0
        self.stop_hit = 0
        
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # Initialize additional widgets
        self.init_widgets()

    def init_widgets(self):
        # Large title
        self.title_label = tk.Label(self, text="CCRT Execution", font=('Helvetica', 20, 'bold'), bg="white")
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Grey panel
        self.config_panel = tk.Canvas(self, bg="#f0f0f0", highlightthickness=0)
        self.config_panel.place(relx=0.5, rely=0.5, anchor="center", width=600, height=300)

        # Divide the panel into three sections and add the required elements
        self.setup_execution_section()
        self.setup_pause_section()
        self.setup_stop_section()

        # Disclaimer
        self.disclaimer_label = tk.Label(self.config_panel, text="Before pressing the Start or Resume button,\nplease make sure you are ready to use the CCRT",
                                         bg="#f0f0f0", wraplength=650)
        self.disclaimer_label.place(relx=0.5, rely=0.85, anchor="center")

    def setup_execution_section(self):
        tk.Label(self.config_panel, text="Start Execution", bg="#f0f0f0").place(relx=0.17, rely=0.1, anchor="n")
        start_button = tk.Button(self.config_panel, text="Start", font=('Helvetica', 12), height=3, width=15, command=self.send_routine)
        start_button.place(relx=0.17, rely=0.25, anchor="n")

    def setup_pause_section(self):
        tk.Label(self.config_panel, text="Continue Execution", bg="#f0f0f0").place(relx=0.5, rely=0.1, anchor="n")
        pause_button = tk.Button(self.config_panel, text="Continue", font=('Helvetica', 12), height=3, width=15, command=self.continue_routine)
        pause_button.place(relx=0.50, rely=0.25, anchor="n")


    def setup_stop_section(self):
        tk.Label(self.config_panel, text="Stop Execution", bg="#f0f0f0").place(relx=0.83, rely=0.1, anchor="n")
        stop_button = tk.Button(self.config_panel, text="Stop", font=('Helvetica', 12), height=3, width=15, command=self.stop_routine)
        stop_button.place(relx=0.83, rely=0.25, anchor="n")

    def on_canvas_resize(self, event):
        width, height = event.width, event.height
        self.canvas.delete("all")
        self.draw_gradient(width, height)
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")
        self.config_panel.place(relx=0.5, rely=0.5, anchor="center", width=600, height=300)

    def draw_gradient(self, width, height):
        for i in range(height):
            gradient_progress = i / height
            r = g = int(255 * gradient_progress)
            b = 255
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)

    def set_batter(self, batter: Batter):
        if batter is not None:
            self.batter = batter
        else:
            self.batter = None

    def set_routine(self, routine: Routine):
        if routine is not None:
            self.routine = routine
        else:
            self.routine = None

    def set_free_use(self, free_use):
        self.free_use = free_use 

    def send_routine(self):
        if self.start_button_pressed == False:
            self.start_button_pressed = True
            set = self.routine.sets[0]
            rep_data_list = []
            for rep in set.reps:
                rpm, torquePercent, pauseTime, armDirection = int(rep.opTorque), int(rep.avgTorque), int(rep.pauseTime), str(rep.armDirection)

                if rpm < 100:
                    if rpm < 10:
                        rpm = '00' + str(rpm)
                    else:
                        rpm = '0' + str(rpm)
                else:
                    rpm = str(rpm)

                if torquePercent < 10:
                    torquePercent = '0' + str(torquePercent) + '.0'
                else:
                    torquePercent = str(torquePercent) + '.0'

                if pauseTime < 10:
                    pauseTime = '0' + str(pauseTime)
                else:
                    pauseTime = str(pauseTime)

                if armDirection == 'CW':
                    armDirection = '0'
                else:
                    armDirection = '1'

                rep_string = rpm + "," + torquePercent + "," + armDirection + "," + pauseTime
                print(rep_string)
                rep_data_list.append(rep_string)

            
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = ('192.168.0.10', 8888)
            #sock.bind(server_address)
            try:           
                message = "START"
                print(f"Sending: {message}")
                sock.sendto(message.encode(), server_address)

                print("Waiting to receive...")
                data, server = sock.recvfrom(24)
                print(f"Received: {data.decode()}")
                
                # Sends the handle position so the correct moment of inertia value can be selected in the microcontroller code.
                message = str(self.routine.sets[0].repPauseTime)
                print(f"Sending: {message}")
                sock.sendto(message.encode(), server_address)

                print("Waiting to receive...")
                data, server = sock.recvfrom(24)
                print(f"Received: {data.decode()}")

            finally:
                for i in range(len(rep_data_list)):
                    print(f"Sending: {rep_data_list[i]}")
                    message = str(rep_data_list[i])
                    sock.sendto(message.encode(), server_address) 

                print("Waiting to receive...")
                data, server = sock.recvfrom(24)
                print(f"Received: {data.decode()}")

                print("Closing socket")
                sock.close()
            


    def continue_routine(self):
        if self.cont_limit < len(self.routine.sets[0].reps):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = ('192.168.0.10', 8888)

            try:
                message = "CONT"
                print(f"Sending: {message}")
                sock.sendto(message.encode(), server_address)

                print("Waiting to receive...")
                data, server = sock.recvfrom(24)
                print(f"Received: {data.decode()}")
            finally:
                print("Closing socket")
                sock.close()
                self.cont_limit += 1

    def stop_routine(self):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('192.168.0.10', 8888)
        try:
            
            message = "STOP"
            print(f"Sending: {message}")
            sock.sendto(message.encode(), server_address)       

            # Messages will come in the format (peakTorque, timetoStop, initTorqueTime, repNum)
            
            for i in range(0, len(self.routine.sets[0].reps)):
                data, server = sock.recvfrom(24)
                stop_test = str(data.decode())
                if (stop_test == "acknowledged") or (stop_test == "acknowledged\n"):
                    self.stop_hit = 1
                    break               
                message = str(data.decode()).split(',')
                self.routine.sets[0].reps[i].timeToStop = message[0]
                self.routine.sets[0].reps[i].initTorqueTime = message[1]
                self.routine.sets[0].reps[i].peakTorque = message[2]
                self.routine.sets[0].reps[i].peakTorqueTime = message[3]      

            if self.stop_hit == 0:
                print("Waiting to receive...")
                data, server = sock.recvfrom(24)
                print(f"Received: {data.decode()}")    
                

            

        finally:
            sock.close()
            self.controller.show_frame("OutputPage", self.batter, self.routine, None)  

    def set_start_button(self):
        self.start_button_pressed = False

    def set_cont_limit(self):
        self.cont_limit = 0
        self.stop_hit = 0





            


        


