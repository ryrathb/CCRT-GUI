import tkinter as tk
from tkinter import ttk  # For Scrollable Frame and Scrollbar

class DataPage(tk.Frame):
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
        self.title_label = tk.Label(self, text="View Past Executions", font=('Helvetica', 20, 'bold'), bg="white")
        self.title_label.pack(pady=(20, 0))

        # Grey Panel for Data
        self.data_panel = tk.Canvas(self, bg="#f0f0f0", highlightthickness=0, borderwidth=2, relief="groove")
        self.data_panel.pack(fill="both", expand=True, padx=20, pady=50)

        self.scroll_frame = ttk.Frame(self.data_panel)
        self.scrollable_window = self.data_panel.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.data_panel.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.data_panel.configure(yscrollcommand=self.scrollbar.set)
        self.scroll_frame.bind("<Configure>", lambda e: self.configure_data_widgets())

        # Initial population of data panels
        self.data_widgets = []
        self.populate_data_panels()

    def populate_data_panels(self):
        for i in range(17):  # Assuming 17 data objects
            data_widget = ttk.Frame(self.scroll_frame, height=150)
            data_widget.grid(row=i // 4, column=i % 4, padx=10, pady=10, sticky="nsew")
            data_widget.grid_propagate(False)

            text_scroll = tk.Scrollbar(data_widget)
            text_box = tk.Text(data_widget, height=4, yscrollcommand=text_scroll.set)
            text_box.insert("end", "Hello World")
            text_box.pack(side='left', fill='both', expand=True)
            text_scroll.config(command=text_box.yview)
            text_scroll.pack(side='right', fill='y')

            self.data_widgets.append(data_widget)

    def configure_data_widgets(self):
        """ Adjust the width of each data widget based on the current size of the grey panel """
        width = self.data_panel.winfo_width()
        each_width = width // 4 - 40  # Adjusting for padding and better fit
        for widget in self.data_widgets:
            widget.config(width=each_width)

    def on_canvas_resize(self, event):
        width, height = event.width, event.height
        self.canvas.delete("all")
        self.draw_gradient(width, height)
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")
        panel_width = width - 40  # Assuming padding of 20 on each side
        panel_height = height / 1.5  # Adjust as needed
        self.data_panel.place(relx=0.5, rely=0.5, anchor="center", width=panel_width, height=panel_height)
        self.back_button.place(relx=0.02, rely=0.02)
        self.configure_data_widgets()

    def draw_gradient(self, width, height):
        for i in range(height):
            gradient_progress = i / height
            r = g = int(255 * gradient_progress)
            b = 255
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)

    def set_batter(self, batter):
        self.batter = batter

 
