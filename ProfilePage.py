import tkinter as tk
from models import seeds

class ProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pin = ""  # To store the user's PIN input

        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self.init_widgets()

    def init_widgets(self):
        # Widgets are initialized without placing them in the canvas yet
        self.title_text = tk.Label(self, text="Type in your player pin to get started", font=('Helvetica', 16), bg='white')
        self.pin_display = tk.Entry(self, justify='center', font=('Helvetica', 20), bd=2, width=10)
        self.keypad_frame = tk.Frame(self, bg='white')

        btn_texts = [str(i) for i in range(1, 10)] + ["0"]
        for i, btn_text in enumerate(btn_texts):
            btn = tk.Button(self.keypad_frame, text=btn_text, width=5, height=2, command=lambda b=btn_text: self.append_pin(b))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)

        self.enter_btn = tk.Button(self, text="Enter", command=self.check_pin)

    def on_canvas_resize(self, event):
        # This method is called every time the canvas is resized.
        # It positions the widgets on the canvas based on its current size.
        self.canvas.delete("all")
        self.draw_gradient(event.width, event.height)

        # Dynamically position widgets based on canvas size
        self.place_widgets(event.width, event.height)

    def place_widgets(self, canvas_width, canvas_height):
        # Calculate positions based on canvas size
        mid_x = canvas_width / 2
        mid_y = canvas_height / 2

        # Position widgets on the canvas
        self.canvas.create_window(mid_x, 50, window=self.title_text)
        self.canvas.create_window(mid_x, 100, window=self.pin_display)
        self.canvas.create_window(mid_x, mid_y, window=self.keypad_frame)
        self.canvas.create_window(mid_x, 150, window=self.enter_btn)

    def append_pin(self, value):
        # Add digit to PIN
        if len(self.pin) < 4:
            self.pin += value
            self.pin_display.delete(0, tk.END)
            self.pin_display.insert(0, self.pin)

    def check_pin(self):
        # Check PIN validity
        if int(self.pin) in seeds.batterpins:
            userBatter = None
            for batter in seeds.batters:
                if int(self.pin) == batter.PIN:
                    userBatter = batter
            self.controller.show_frame("HomePage", userBatter, None, None)
        else:
            print("Invalid PIN")  # Consider showing this message in the UI
        self.pin = ""
        self.pin_display.delete(0, tk.END)

    def draw_gradient(self, width, height):
        # Redraw gradient to fit the canvas size
        for i in range(height):
            gradient_progress = i / height
            r = g = int(255 * gradient_progress)
            b = 255
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)


