import customtkinter as ctk
from data_manager import checksIfFileExists
from auth import AuthScreen
from dashboard import Dashboard

# Defines the Window
ctk.set_appearance_mode("system")   # Chooses based on the user system theme
ctk.set_default_color_theme("blue") # Sets the theme to colour blue


class App(ctk.CTk):


    def __init__(self):
        super().__init__()

        # Defines the window size
        self.title("StudyTrack")
        self.geometry("1100x680")
        self.minsize(900, 580)

        # Allows the window to be expanded
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Verifies CSV files exist before any screen tries to read them
        checksIfFileExists()

        # Start on the login screen
        self._show_auth()

    def _show_auth(self):
        
        # Displays the Login Screen
        self.clearScreen()
        self.geometry("520x540")
        self.resizable(False, False)

        auth = AuthScreen(self, onAuthenticated=self.showDashboard)
        auth.grid(row=0, column=0, sticky="nsew")

    def showDashboard(self, username: str):
        # Once Logged in Displayst the Dashboard 
        self.clearScreen()
        self.geometry("1100x680")
        self.resizable(True, True)

        dashboard = Dashboard(self, username=username, onLogout=self._show_auth)
        dashboard.grid(row=0, column=0, sticky="nsew")

    def clearScreen(self):
        # Destroy all current child widgets before switching screens.
        for widget in self.winfo_children():
            widget.destroy()


# Runs the app
if __name__ == "__main__":
    app = App()
    app.mainloop()
