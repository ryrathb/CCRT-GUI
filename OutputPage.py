import tkinter as tk 
import csv
import os

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
        self.config_panel.place(relx=0.5, rely=0.5, anchor="center", width=600, height=300)

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
        self.config_panel.place(relx=0.5, rely=0.5, anchor="center", width=600, height=300)
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
        rep_field_names = ['Name', 'Rep ID', 'Rep Number', 'Set', 'Arm Direction', 'Start Position', 'End Position', 'Input RPM', 'Average Torque', 'Peak Torque', 'Time to Stop', 'Initial Torque Time']

        rep_lists = [[rep.name, rep.repID, rep.repNum, 'Static Set', rep.armDirection, 'Center', ('Left' if rep.ArmDirection == "CCW" else 'Right'), rep.opTorque, 'N/A', rep.peakTorque, rep.timeToStop, rep.initTorqueTime] for rep in self.routine.sets[0].reps]

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
        for i in range(0, len(self.routine.sets[0].reps)):  # Create 16 subsections
            row = i // 4  # There are 4 rows
            column = i % 4  # There are 4 columns
            text = f"Repetition Number: {str(self.routine.sets[0].reps[i].repNum)}\nPeak Torque: {str(self.routine.sets[0].reps[i].peakTorque)}\nTime to Stop: {str(self.routine.sets[0].reps[i].timeToStop)}\nInitial Torque Applied Time: {str(self.routine.sets[0].reps[i].initTorqueTime)}"
            label = tk.Label(self.config_panel, text=text, bg="#f0f0f0", justify=tk.LEFT, anchor="w", font=('Helvetica', 8))
            label.place(x=10 + column * 140, y=10 + row * 70, width=130, height=65)
            self.repetition_labels.append(label)

    
    def set_batter(self, batter):
        self.batter = batter


        
