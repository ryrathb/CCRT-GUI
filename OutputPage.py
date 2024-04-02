import tkinter as tk 

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

        # Return to HomePage Button
        self.return_home_button = tk.Button(self, text="Return Home", command=lambda: self.controller.show_frame("HomePage", self.batter, None, None))
        self.return_home_button.place(relx=0.95, rely=0.01, anchor="ne")

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

    def set_routine(self, routine):
        self.routine = routine 
    
    def set_batter(self, batter):
        self.batter = batter


        
