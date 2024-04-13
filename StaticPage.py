import tkinter as tk
from tkinter import ttk  # For dropdown menus
from models.Batter import Batter 
from models.Rep import Rep 
from models.Routine import Routine
from models.Set import Set
import random
from datetime import datetime


class StaticPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.batter = None

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.check_state = 0
        # Initialize widgets
        self.init_widgets()

    def init_widgets(self):
        # Title
        self.title_label = tk.Label(self, text="Static Mode", font=('Helvetica', 20, 'bold'), bg="white")
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Grey panel
        self.config_panel = tk.Canvas(self, bg="#f0f0f0", highlightthickness=0)
        self.config_panel.place(relx=0.5, rely=0.5, anchor="center", width=600, height=250)

        # Section for Opposing Torque
        self.setup_torque_section()

        # Section for Swing Direction
        self.setup_direction_section()

        # Section for Pause Time
        self.setup_pause_section()

        # Section for Number of Reps
        self.setup_reps_section()

        # Disclaimer and checkbox
        self.disclaimer_label = tk.Label(self.config_panel, text="DISCLAIMER: If you want to just swing the arm freely, \ncheck the box to the right",
                                         bg="#f0f0f0", wraplength=500)
        self.disclaimer_label.place(relx=0.5, rely=0.9, anchor="center")
        self.disclaimer_check = tk.Checkbutton(self.config_panel, bg="#f0f0f0", variable=self.check_state)
        self.disclaimer_check.place(relx=0.85, rely=0.9, anchor="center")

        # Back button
        self.back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("HomePage", self.batter, None, None))
        self.back_button.place(relx=0.01, rely=0.01)

        # Start Execution button
        self.start_button = tk.Button(self, text="Start Execution", command=self.start_execution)
        self.start_button.place(relx=0.95, rely=0.01, anchor="ne")


    def set_batter(self, batter: Batter):
        if batter is not None:
            self.batter = batter
        else:
            self.batter = None

    def setup_torque_section(self):
        tk.Label(self.config_panel, text="Arm Speed (RPM)", bg="#f0f0f0").place(relx=0.125, rely=0.1, anchor="n")
        torque_values = [str(i) for i in range(0, 101, 5)]
        self.torque_dropdown = ttk.Combobox(self.config_panel, values=torque_values, state="readonly")
        self.torque_dropdown.place(relx=0.125, rely=0.2, anchor="n")

    def setup_direction_section(self):
        tk.Label(self.config_panel, text="Swing Direction", bg="#f0f0f0").place(relx=0.375, rely=0.1, anchor="n")
        self.direction_dropdown = ttk.Combobox(self.config_panel, values=["CW", "CCW"], state="readonly")
        self.direction_dropdown.place(relx=0.375, rely=0.2, anchor="n")

    def setup_pause_section(self):
        tk.Label(self.config_panel, text="Pause Time (s)", bg="#f0f0f0").place(relx=0.625, rely=0.1, anchor="n")
        pause_values = [str(i) for i in range(2, 31, 2)]
        self.pause_dropdown = ttk.Combobox(self.config_panel, values=pause_values, state="readonly")
        self.pause_dropdown.place(relx=0.625, rely=0.2, anchor="n")

    def setup_reps_section(self):
        tk.Label(self.config_panel, text="Number of Reps", bg="#f0f0f0").place(relx=0.875, rely=0.1, anchor="n")
        reps_values = [str(i) for i in range(2, 17)]
        self.reps_dropdown = ttk.Combobox(self.config_panel, values=reps_values, state="readonly")
        self.reps_dropdown.place(relx=0.875, rely=0.2, anchor="n")

    def on_canvas_resize(self, event):
        width, height = event.width, event.height
        self.canvas.delete("all")
        self.draw_gradient(width, height)
        # Re-adjust the positions based on the canvas size
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")
        self.config_panel.place(relx=0.5, rely=0.5, anchor="center", width=600, height=250)
        self.back_button.place(relx=0.01, rely=0.01)
        self.start_button.place(relx=0.95, rely=0.01, anchor="ne")

    def draw_gradient(self, width, height):
        for i in range(height):
            gradient_progress = i / height
            r = g = int(255 * gradient_progress)
            b = 255
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)

    def start_execution(self):
        op_torque = int(self.torque_dropdown.get())
        direction = self.direction_dropdown.get()
        pause_time = int(self.pause_dropdown.get())
        reps = int(self.reps_dropdown.get())

        new_static_exec = Routine(routineID=random.randint(1000000000, 9999999999), name=("Static Execution on " + str(datetime.now().strftime("%Y-%m-%d"))), batter=self.batter, isStatic=True, setPauseTime=None)
        static_set = Set(name="Static Set 1", setID=random.randint(1000000000, 9999999999), repPauseTime=pause_time, routine=new_static_exec, leftBound=0, rightBound=0, isSitting=False)

        for i in range(1, (reps + 1)):
            new_rep = Rep(name=("Rep " + str(i)), repID=random.randint(1000000000, 9999999999), repNum=i, setObj=static_set, armDirection=direction, startPos=8, endPos=(0 if direction == "CCW" else 16), opTorque=op_torque, avgTorque=None, peakTorque=None, timeToStop=None, initTorqueTime=None)
            static_set.reps.append(new_rep) 

        new_static_exec.sets.append(static_set)
        if self.check_state == 0:
            self.controller.show_frame("ExecutionPage", self.batter, new_static_exec, False)
        else:
            self.controller.show_frame("ExecutionPage", self.batter, None, True)
        

