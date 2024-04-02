import tkinter as tk
from tkinter import ttk  # For dropdown menus
from models.Batter import Batter 
from models.Rep import Rep 
from models.Routine import Routine
from models.Set import Set
import random
from datetime import datetime

"""
    Elements I need to add still:
        - While the routine object will be packed and sent to the clearcore
        to perform motor actions, there needs to be some function in which 
        a while loop is running and grabbing data from the controller. This 
        will pull it all into a routine object and send it to the output page 
        to be displayed. 
        - I need to figure out if I want to send the routine data to the controller 
        right on page switch, or if I should wait for the start button to be pressed
        - Pause and Resume implementation. This needs to align with the while loop running,
        so that if the user wants to resume execution, the data will be preserved
        - I need to find a place to store the data. Maybe I'll create a large text file or something 
        that will hold all of the necessary data. Need to figure that out this week.

"""


class ExecutionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.batter = None
        self.routine = None
        self.free_use = False

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
        start_button = tk.Button(self.config_panel, text="Start", font=('Helvetica', 12), height=2, width=10)
        start_button.place(relx=0.17, rely=0.25, anchor="n")

    def setup_pause_section(self):
        tk.Label(self.config_panel, text="Pause Execution", bg="#f0f0f0").place(relx=0.5, rely=0.1, anchor="n")
        pause_button = tk.Button(self.config_panel, text="Pause", font=('Helvetica', 12), height=2, width=10)
        pause_button.place(relx=0.42, rely=0.25, anchor="n")
        resume_button = tk.Button(self.config_panel, text="Resume", font=('Helvetica', 12), height=2, width=10)
        resume_button.place(relx=0.58, rely=0.25, anchor="n")

    def setup_stop_section(self):
        tk.Label(self.config_panel, text="Stop Execution", bg="#f0f0f0").place(relx=0.83, rely=0.1, anchor="n")
        stop_button = tk.Button(self.config_panel, text="Stop", font=('Helvetica', 12), height=2, width=10, command=lambda: self.controller.show_frame("OutputPage", self.batter, self.routine, None))
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
