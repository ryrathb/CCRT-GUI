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
        self.check_state = tk.IntVar()
        # Initialize widgets
        self.init_widgets()

    def init_widgets(self):
        # Title
        self.title_label = tk.Label(self, text="Static Mode", font=('Helvetica', 20, 'bold'), bg="white")
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Grey panel
        self.config_panel = tk.Canvas(self, bg="#f0f0f0", highlightthickness=0)
        self.config_panel.place(relx=0.5, rely=0.55, anchor="center", width=700, height=600)

        # Add column labels
        self.setup_column_labels()

        # Add entries for individual rep configuration
        self.reps_entries = []
        self.setup_rep_entries()

        # Disclaimer and checkbox
        self.disclaimer_label = tk.Label(self.config_panel, text="DISCLAIMER: If you want to just swing the arm freely, \ncheck the box to the right",
                                         bg="#f0f0f0", wraplength=500)
        self.disclaimer_label.place(relx=0.5, rely=0.95, anchor="center")
        self.disclaimer_check = tk.Checkbutton(self.config_panel, bg="#f0f0f0", variable=self.check_state)
        self.disclaimer_check.place(relx=0.85, rely=0.95, anchor="center")

        # Back button
        self.back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("HomePage", self.batter, None, None))
        self.back_button.place(relx=0.01, rely=0.01)

        # Start Execution button
        self.start_button = tk.Button(self, text="Start Execution", command=self.start_execution)
        self.start_button.place(relx=0.95, rely=0.01, anchor="ne")

    def setup_column_labels(self):
        labels = ["RPM", "Torque %", "Direction", "Pause Time"]
        for i, label in enumerate(labels):
            tk.Label(self.config_panel, text=label, bg="#f0f0f0", font=('Helvetica', 12, 'bold')).place(relx=0.2 + i*0.15, rely=0.05, anchor="w")

    def setup_rep_entries(self):
        directions = ["CW", "CCW"]
        torque_values = [f"{i*2.5:.1f}" for i in range(13)]
        rpm_values = [str(i) for i in range(5, 45, 5)]
        pause_time_values = [str(i) for i in range(0, 32, 2)]

        for i in range(12):
            tk.Label(self.config_panel, text=f"Rep {i+1}", bg="#f0f0f0").place(relx=0.1, rely=(i+1)/15 + 0.1, anchor="w")

            rep_frame = tk.Frame(self.config_panel, bg="#f0f0f0")
            rep_frame.place(relx=0.2, rely=(i+1)/15 + 0.1, anchor="w", width=500, height=30)

            rpm_dropdown = ttk.Combobox(rep_frame, values=rpm_values, state="readonly", width=8)
            rpm_dropdown.grid(row=0, column=0, padx=15)
            torque_dropdown = ttk.Combobox(rep_frame, values=torque_values, state="readonly", width=8)
            torque_dropdown.grid(row=0, column=1, padx=15)
            direction_dropdown = ttk.Combobox(rep_frame, values=directions, state="readonly", width=8)
            direction_dropdown.grid(row=0, column=2, padx=15)
            pause_dropdown = ttk.Combobox(rep_frame, values=pause_time_values, state="readonly", width=8)
            pause_dropdown.grid(row=0, column=3, padx=15)

            self.reps_entries.append((rpm_dropdown, torque_dropdown, direction_dropdown, pause_dropdown))

    def set_batter(self, batter: Batter):
        if batter is not None:
            self.batter = batter
        else:
            self.batter = None

    def on_canvas_resize(self, event):
        width, height = event.width, event.height
        self.canvas.delete("all")
        self.draw_gradient(width, height)
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")
        self.config_panel.place(relx=0.5, rely=0.55, anchor="center", width=700, height=600)
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
        reps = []
        for rpm_dropdown, torque_dropdown, direction_dropdown, pause_dropdown in self.reps_entries:
            rpm = rpm_dropdown.get()
            torque = torque_dropdown.get()
            direction = direction_dropdown.get()
            pause = pause_dropdown.get()

            if rpm and torque and direction and pause:
                reps.append({
                    "rpm": int(rpm),
                    "torque": float(torque),
                    "direction": direction,
                    "pause": int(pause)
                })

        if not reps:
            print("No reps configured")
            return

        new_static_exec = Routine(routineID=random.randint(1000000000, 9999999999), name=("Static Execution on " + str(datetime.now().strftime("%Y-%m-%d"))), batter=self.batter, isStatic=True, setPauseTime=None)
        static_set = Set(name="Static Set 1", setID=random.randint(1000000000, 9999999999), repPauseTime=None, routine=new_static_exec, leftBound=0, rightBound=0, isSitting=False)

        for i, rep_config in enumerate(reps, 1):
            new_rep = Rep(
                name=f"Rep {i}",
                repID=random.randint(1000000000, 9999999999),
                repNum=i,
                setObj=static_set,
                armDirection=rep_config["direction"],
                startPos=8,
                endPos=(0 if rep_config["direction"] == "CCW" else 16),
                opTorque=rep_config["rpm"],
                avgTorque=rep_config["torque"],
                peakTorque=None,
                timeToStop=None,
                initTorqueTime=None,
                peakTorqueTime=None,
                pauseTime=rep_config["pause"]
            )
            static_set.reps.append(new_rep)

        new_static_exec.sets.append(static_set)
        if self.check_state.get() == 0:
            for set in new_static_exec.sets:
                for rep in set.reps:
                    rep_string = "Rep " + str(rep.repNum) + ": " + str(rep.opTorque) + " RPM, " + str(rep.avgTorque) + "% Torque, " + str(rep.armDirection) + ", " + str(rep.pauseTime)
                    print(rep_string)
            self.controller.show_frame("ExecutionPage", self.batter, new_static_exec, False)
        else:
            self.controller.show_frame("ExecutionPage", self.batter, None, True)
