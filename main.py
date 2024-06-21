import tkinter as tk
from StartPage import StartPage
from DataPage import DataPage
from DynamicPage import DynamicPage 
from ExecutionPage import ExecutionPage
from HomePage import HomePage
from OutputPage import OutputPage
from ProfilePage import ProfilePage
from StaticPage import StaticPage
from CreateUserPage import CreateUserPage

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Chicago Cubs Rotational Trainer")

        self.frames = {}

        # Pack control frame first
        control_frame = tk.Frame(self, height=30, bg='grey')
        control_frame.pack(fill=tk.X, side=tk.TOP)  # This ensures it's at the top

        exit_button = tk.Button(control_frame, text="X", command=self.exit_app)
        exit_button.pack(side=tk.RIGHT)

        self.toggle_fs_button = tk.Button(control_frame, text="[ ]", command=self.toggle_fullscreen)
        self.toggle_fs_button.pack(side=tk.RIGHT)
       
        minimize_button = tk.Button(control_frame, text='-', command=self.minimize_window)
        minimize_button.pack(side=tk.RIGHT)

        # Then pack the container frame
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)  # Configure the container
        container.grid_columnconfigure(0, weight=1)

        for F in (StaticPage, ProfilePage, CreateUserPage, DataPage, HomePage, StartPage, OutputPage, ExecutionPage, DynamicPage):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.fullscreen_state = True
        self.attributes('-fullscreen', self.fullscreen_state)

        self.bind("<F11>", self.toggle_fullscreen_event)
        self.bind('<Escape>', self.exit_fullscreen_event)

        self.show_frame("StartPage", None, None, None)


    def show_frame(self, page_name, batter, routine, free_use):
        frame = self.frames[page_name]
        if str(page_name) in ["HomePage", "StaticPage", "DynamicPage", "DataPage", "ExecutionPage", "OutputPage"]:
            if page_name in ["ExecutionPage", "OutputPage"]:
                if page_name == "ExecutionPage":
                    frame.set_free_use(free_use)
                    frame.set_start_button()
                    frame.set_cont_limit() 
                frame.set_routine(routine)
            if page_name == "StaticPage":
                frame.setup_rep_entries()
            frame.set_batter(batter) 
        frame.tkraise()

    def toggle_fullscreen(self):
        self.fullscreen_state = not self.fullscreen_state
        self.attributes("-fullscreen", self.fullscreen_state)
        self.toggle_fs_button.config(text="[ ]" if self.fullscreen_state else "[]")

    def toggle_fullscreen_event(self, event=None):
        self.toggle_fullscreen() 

    def exit_fullscreen_event(self, event=None):
        if self.fullscreen_state:
            self.toggle_fullscreen()

    def minimize_window(self):
        self.iconify()

    def exit_app(self):
        self.quit()
        self.destroy()

    
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
