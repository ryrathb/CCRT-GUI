import tkinter as tk
from tkinter import messagebox
from models.Batter import Batter
from models import seeds
import random
import random as rnd

class CreateUserPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # Initialize widgets
        self.init_widgets()

    def init_widgets(self):
        # Title
        self.title_label = tk.Label(self, text="Create Your New User Account", font=('Helvetica', 24, 'bold'), bg="white")
        self.title_label.pack(pady=20)

        # Enlarged grey panel
        self.config_panel = tk.Canvas(self, bg="#f0f0f0", highlightthickness=0)
        self.config_panel.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        # Input labels and fields with added spacing and styling
        labels = ['First Name', 'Last Name', '4-Digit PIN', 'Height', 'Weight']
        self.entries = []
        for i, label in enumerate(labels):
            tk.Label(self.config_panel, text=label, bg="#f0f0f0", font=('Helvetica', 12, 'bold')).place(relx=0.1, rely=(i+1)/7, anchor="w")
            entry = tk.Entry(self.config_panel)
            entry.place(relx=0.1, rely=(i+1.5)/7, anchor="w", width=200)
            self.entries.append(entry)

        # Enlarged and repositioned Finish button
        self.finish_button = tk.Button(self.config_panel, text="Finish", command=self.validate_and_create_user, font=('Helvetica', 14, 'bold'), bg="#4CAF50", fg="white")
        self.finish_button.place(relx=0.8, rely=0.5, anchor="center", width=120, height=50)

    def validate_and_create_user(self):
        # Error checking for user inputs
        fname, lname, pin, height, weight = (entry.get().strip() for entry in self.entries)
        fname = str(fname[0]).upper() + str(fname[1:])
        lname = str(lname[0]).upper() + str(lname[1:])
        id = rnd.randint(1000000000, 9999999999)
        newBatter = Batter(id, fname, lname, pin, height, weight)
        seeds.add_batter(batter=newBatter)

        self.controller.show_frame("HomePage", newBatter, None, None)


    def on_canvas_resize(self, event):
        self.canvas.delete("all")
        self.draw_gradient(event.width, event.height)
        self.config_panel.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)
        self.title_label.place(relx=0.5, rely=0.1, anchor="center")

    def draw_gradient(self, width, height):
        for i in range(height):
            gradient_progress = i / height
            r = g = int(255 * gradient_progress)
            b = 255
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)
