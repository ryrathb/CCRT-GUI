import tkinter as tk

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Make the frame occupy the full window

        # Create a canvas that fills the frame
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        # Update the canvas size to fill the frame/window
        self.canvas.bind("<Configure>", self.on_resize)

        # Title and button initialization moved to on_resize to ensure
        # they are correctly placed after the canvas has been resized

    def draw_gradient(self, width, height):
        # Create the gradient from blue to white vertically
        for i in range(height):
            # Calculate how much of the gradient is completed
            gradient_progress = i / height
            # Start with blue (0, 0, 255) and transition to white (255, 255, 255)
            r = g = int(255 * gradient_progress)  # r and g values increase from 0 to 255
            b = 255  # b stays constant at 255
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)


    def on_resize(self, event):
        # Redraw the gradient to fit the new size
        width, height = event.width, event.height
        self.canvas.delete("all")  # Remove previous gradient
        self.draw_gradient(width, height)

        # Place the title directly on the canvas
        self.canvas.create_text(width / 2, height * 0.3, text="Welcome to the Chicago Cubs Rotational Trainer",
                                font=('Helvetica', 24, 'bold'), fill="white")

        # Since a Button cannot be placed directly on a Canvas and have it match the background,
        # consider using a Label as a button or another method to trigger the event.
        # For demonstration, here's how you might create a "button" on the canvas:
        self.profile_page_button = tk.Button(self, text="Go to Profile Page",
                                             command=lambda: self.controller.show_frame("ProfilePage", None, None, None))
        self.profile_page_button.place(relx=0.5, rely=0.6, anchor="center")



        
