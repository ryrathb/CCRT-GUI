import tkinter as tk 
import csv
import os
import math
import random

class OutputPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 
        self.batter = None
        self.routine = None 

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_canvas_resize) 

        self.init_widgets()

    def init_widgets(self):
        # Large Title
        self.title_label = tk.Label(self, text="Execution Output", font=('Helvetica', 20, 'bold'), bg="white")
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Grey Panel
        self.config_panel = tk.Canvas(self, bg="#f0f0f0", highlightthickness=0)
        self.config_panel.place(relx=0.5, rely=0.5, anchor="center", width=1200, height=500)

        # Subsections for Repetition Data
        

        # Return to HomePage Button
        self.return_home_button = tk.Button(self, text="Return Home", command=lambda: self.controller.show_frame("HomePage", self.batter, None, None))
        self.return_home_button.place(relx=0.95, rely=0.01, anchor="ne")

        self.export_to_csv = tk.Button(self, text="Export to CSV", command=self.export_to_csv)
        self.export_to_csv.place(relx=95, rely="0.05", anchor="ne")


    def on_canvas_resize(self, event):
        width, height = event.width, event.height
        self.canvas.delete("all")
        self.draw_gradient(width, height)
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")
        self.config_panel.place(relx=0.5, rely=0.5, anchor="center", width=1200, height=450)
        self.return_home_button.place(relx=0.95, rely=0.01, anchor="ne")

    def draw_gradient(self, width, height):
        for i in range(height):
            gradient_progress = i / height
            r = g = int(255 * gradient_progress)
            b = 255 
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)

    def export_to_csv(self):
        batter_field_names = ['ID', 'First Name', 'Last Name', 'PIN', 'Height', 'Weight', 'Date']
        rep_field_names = ['Name', 'Rep ID', 'Rep Number', 'Set', 'Arm Direction', 'Start Position', 
                           'End Position', 'Input RPM', 'Average Torque', 'Peak Torque', 'Time to Stop', 
                           'Initial Torque Time']

        rep_lists = [[rep.name, rep.repID, rep.repNum, 'Static Set', rep.armDirection, 'Center', 
                      ('Left' if rep.ArmDirection == "CCW" else 'Right'), 
                      rep.opTorque, 'N/A', rep.peakTorque, rep.timeToStop, rep.initTorqueTime] 
                      for rep in self.routine.sets[0].reps]

        file_path = "CCRT.csv"
        file_exists = os.path.exists(file_path)
        mode = 'a' if file_exists else 'w'

        with open(file_path, mode, newline='') as file:
            writer = csv.DictWriter(file, fieldnames=rep_field_names)

            if not file_exists:
                writer = csv.DictWriter(file, fieldnames=batter_field_names)
                writer.writeheader()
                writer = csv.DictWriter(file, fieldnames=rep_field_names) 

            writer.writerow('\n')
            writer.writeheader()
            writer.writerows(rep_lists)

    def set_routine(self, routine):
        self.routine = routine 
        self.repetition_labels = []
        for i in range(len(self.routine.sets[0].reps)):  # Create 16 subsections
            row = i // 4  # There are 4 rows
            column = i % 4  # There are 4 columns
            
            # Create a frame for each label to manage layout better
            frame = tk.Frame(self.config_panel, bg="#f0f0f0", relief="groove", bd=2)
            frame.place(x=40 + column * 280, y=40 + row * 120, width=280, height=125)

            # Create the title label for the repetition number
            title = tk.Label(frame, text=f"Repetition Number: {i + 1}", font=('Helvetica', 10, 'bold'), bg="#f0f0f0", anchor="center")
            title.pack(fill="x")

            # Create a frame for the columns
            data_frame = tk.Frame(frame, bg="#f0f0f0")
            data_frame.pack(fill="both", expand=True)

            # Left column data
            left_column = tk.Label(data_frame, text=f"RPM: {str(self.routine.sets[0].reps[i].opTorque)}\n"
                                                    f"Torque %: {str(self.routine.sets[0].reps[i].avgTorque)}\n"
                                                    f"Direction: {str(self.routine.sets[0].reps[i].armDirection)}\n"
                                                    f"Pause Time (s): {str(self.routine.sets[0].reps[i].pauseTime)}",
                                   font=('Helvetica', 9), bg="#f0f0f0", justify=tk.LEFT)
            left_column.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

            # Right column data
            right_column = tk.Label(data_frame, text=f"Peak Torque (Nm): {str(self.routine.sets[0].reps[i].peakTorque)}\n"
                                                     f"Peak Torque Time (s): {str(self.routine.sets[0].reps[i].peakTorqueTime)}\n"
                                                     f"Time to Stop (s): {str(self.routine.sets[0].reps[i].timeToStop)}\n"
                                                     f"Reaction Time (s): {str(self.routine.sets[0].reps[i].initTorqueTime)}",
                                    font=('Helvetica', 9), bg="#f0f0f0", justify=tk.LEFT)
            right_column.grid(row=0, column=1, padx=5, pady=5, sticky="ne")

            self.repetition_labels.append(frame)

    def set_batter(self, batter):
        self.batter = batter

    def random_double_with_two_decimals(self):
        random_float = random.uniform(9, 15)
        random_float = round(random_float, 2)
        return random_float 
    
    def random_double_0_to_1_5(self):
        random_float = random.uniform(0.2, 1.5)
        random_float = round(random_float, 3)
        return random_float 
    
    def random_double_less_than_first(self, first_random):
        second_random_float = random.uniform(0.2, first_random)
        second_random_float = round(second_random_float, 3)
        return second_random_float
