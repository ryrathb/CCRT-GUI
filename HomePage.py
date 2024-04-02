import tkinter as tk
from models.Batter import Batter

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.batter = None
        
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self.init_widgets()

    def init_widgets(self):
        # Centered welcome title
        self.title_text = tk.Label(self.canvas, text="", font=('Helvetica', 20, 'bold'), bg="white")
        
        # Logout button
        self.logout_button = tk.Button(self.canvas, text="Logout", command=self.logout)
        self.logout_button.place(x=20, y=20)

        # Middle panel
        self.panel = tk.Canvas(self.canvas, bg="#f0f0f0", highlightthickness=0, borderwidth=2, relief="groove")

        # Static Mode section elements
        self.static_mode_title = tk.Label(self.panel, text="Static Mode", bg="#f0f0f0", font=('Helvetica', 18, 'bold'))
        self.static_mode_button = tk.Button(self.panel, text="Go to Static Mode",
                                            command=lambda: self.controller.show_frame("StaticPage", self.batter, None, None))
        self.static_mode_desc = tk.Label(self.panel, text=("Static Mode is used for simple executions of the CCRT. "
                                         "All configurations are the same through each repetition, so be careful when "
                                         "setting the amount of torque you want to oppose, which direction you plan on "
                                         "opposing, and how much time you want in between repetitions."),
                                         wraplength=180, justify="left", bg="#f0f0f0", font=('Helvetica', 10))

        # Dynamic Mode section elements
        self.dynamic_mode_title = tk.Label(self.panel, text="Dynamic Mode", bg="#f0f0f0", font=('Helvetica', 18, 'bold'))
        self.dynamic_mode_button = tk.Button(self.panel, text="Go to Dynamic Mode",
                                             command=lambda: self.controller.show_frame("DynamicPage", self.batter, None, None))
        self.dynamic_mode_desc = tk.Label(self.panel, text=("Dynamic Mode is used for more complex executions of the CCRT. "
                                          "In Dynamic Mode, you are able to construct intricate routines where the amount "
                                          "of opposing torque, arm direction, and time between repetitions can differ from "
                                          "every repetition. Please be conscious of how you build this routine; safety is "
                                          "the most important thing to keep in mind."),
                                          wraplength=180, justify="left", bg="#f0f0f0", font=('Helvetica', 10))

    def set_batter(self, batter: Batter):
        if batter is not None:
            self.title_text.config(text=f"Welcome {batter.firstName} {batter.lastName}")
            self.batter = batter
        else:
            self.title_text.config(text="Welcome")

    def logout(self):
        self.batter = None
        self.controller.show_frame("ProfilePage", None, None, None)

    def on_canvas_resize(self, event):
        # Adjust layout on resize
        width, height = event.width, event.height
        self.canvas.delete("all")
        self.draw_gradient(width, height)
        self.title_text.place(relx=0.5, rely=0.1, anchor="center")
        self.logout_button.place(x=20, y=20)

        panel_width = width * 0.5
        panel_height = height * 0.5
        self.panel.place(relx=0.5, rely=0.5, anchor="center", width=panel_width, height=panel_height)

        # Adjust Static and Dynamic Mode section layout
        section_width = panel_width / 2
        self.static_mode_title.place(x=section_width / 4, y=20)
        self.static_mode_button.place(x=section_width / 4, y=60)
        self.static_mode_desc.place(x=section_width / 5, y=100, width=section_width / 1.5)
        
        self.dynamic_mode_title.place(x=section_width * 5 / 4, y=20)
        self.dynamic_mode_button.place(x=section_width * 5 / 4, y=60)
        self.dynamic_mode_desc.place(x=section_width * 4.8 / 4, y=100, width=section_width / 1.5)

    def draw_gradient(self, width, height):
        for i in range(height):
            gradient_progress = i / height
            r = g = int(255 * gradient_progress)
            b = 255
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)
