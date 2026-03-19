import customtkinter as ctk
from data_manager import createUser, verifyLogin

# Defines the Login Screen Class
class AuthScreen(ctk.CTkFrame):
    def __init__(self, parent, onAuthenticated):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self.onAuthenticated = onAuthenticated
        self.isInLoginMode = True

        self.definesUI()

    def definesUI(self):

        # Defines Window
        self.grid_columnconfigure(0, weight=1)
        title = ctk.CTkFrame(self, fg_color="transparent")
        title.grid(row=0, column=0, pady=(40, 10))


        # Title
        ctk.CTkLabel(title,text="StudyTrack",font=ctk.CTkFont(family="Georgia", size=42, weight="bold"),text_color=("#1a1a2e", "#e2e2f0")).pack()

        # App Text
        ctk.CTkLabel(title,text="Track your study sessions!",font=ctk.CTkFont(size=13),text_color=("gray50", "gray60")).pack()

        # Card
        self.card = ctk.CTkFrame(self, width=380, corner_radius=16,fg_color=("#ffffff", "#1e1e2e"),border_width=1, border_color=("#e0e0e0", "#2e2e4e"))
        self.card.grid(row=1, column=0, padx=40, pady=20, sticky="ew")
        self.card.grid_columnconfigure(0, weight=1)

        # Header
        self.modeLabel = ctk.CTkLabel(self.card, text="Welcome back", font=ctk.CTkFont(size=20, weight="bold"))
        self.modeLabel.grid(row=0, column=0, padx=30, pady=(28, 4))

        self.modeSubLabel = ctk.CTkLabel(self.card, text="Sign in to your account", font=ctk.CTkFont(size=12), text_color=("gray50", "gray60"))
        self.modeSubLabel.grid(row=1, column=0, padx=30, pady=(0, 20))

        # Inputs
        def make_label(text, row):
            ctk.CTkLabel(self.card, text=text, font=ctk.CTkFont(size=12, weight="bold"), anchor="w").grid(row=row, column=0, padx=30, sticky="w")

        def make_entry(placeholder, show=None):
            return ctk.CTkEntry(self.card, placeholder_text=placeholder,show=show,height=40,corner_radius=8,border_color=("#d0d0d0", "#3e3e5e"))

        # Fields for Username, Password and Confirming details
        make_label("Username", 2)
        self.username_entry = make_entry("Enter your username")
        self.username_entry.grid(row=3, column=0, padx=30, pady=(4, 12), sticky="ew")

        make_label("Password", 4)
        self.password_entry = make_entry("Enter your password", show="●")
        self.password_entry.grid(row=5, column=0, padx=30, pady=(4, 12), sticky="ew")

        # Confirm password (hidden by default)
        self.confirmLabel = ctk.CTkLabel(self.card, text="Confirm Password",font=ctk.CTkFont(size=12, weight="bold"),anchor="w")
        self.confirmPassword = make_entry("Re-enter your password", show="●")

        # Status
        self.status_label = ctk.CTkLabel(self.card, text="", font=ctk.CTkFont(size=12),text_color=("#c0392b", "#e74c3c"), wraplength=300)
        self.status_label.grid(row=7, column=0, padx=30, pady=(0, 4))

        # Action button
        self.actionBtn = ctk.CTkButton(self.card,text="Sign In",height=42,corner_radius=8,font=ctk.CTkFont(size=14, weight="bold"),fg_color=("#4f46e5", "#6366f1"),hover_color=("#3730a3", "#4f46e5"),command=self.handlesAuthentication)
        self.actionBtn.grid(row=8, column=0, padx=30, pady=(8, 12), sticky="ew")

        # Toggle
        toggle = ctk.CTkFrame(self.card, fg_color="transparent")
        toggle.grid(row=9, column=0, padx=30, pady=(0, 24))

        self.toggleLabel = ctk.CTkLabel(toggle, text="Don't have an account?",font=ctk.CTkFont(size=12),text_color=("gray50", "gray60"))
        self.toggleLabel.pack(side="left")

        self.toggleBtn = ctk.CTkButton(toggle,text="Register",width=70,height=24,fg_color="transparent",text_color=("#4f46e5", "#818cf8"),hover_color=("gray90", "gray20"),font=ctk.CTkFont(size=12, weight="bold"),command=self.chooseMode
        )
        self.toggleBtn.pack(side="left", padx=(4, 0))

        # Enter key bindings
        for entry in (self.username_entry, self.password_entry, self.confirmPassword):
            entry.bind("<Return>", lambda e: self.handlesAuthentication())

    def chooseMode(self):
        self.isInLoginMode = not self.isInLoginMode
        self.setStaus("", error=False)

        # Checks if the User is Logged in
        if self.isInLoginMode:

            # Defines the text labels on screen
            self.modeLabel.configure(text="Welcome back")
            self.modeSubLabel.configure(text="Sign in to your account")
            self.actionBtn.configure(text="Sign In")
            self.toggleLabel.configure(text="Don't have an account?")
            self.toggleBtn.configure(text="Register")

            self.confirmLabel.grid_forget()
            self.confirmPassword.grid_forget()

        else:

            # Displays the text labels for Registering an Account
            self.modeLabel.configure(text="Create account")
            self.modeSubLabel.configure(text="Start tracking your studies today")
            self.actionBtn.configure(text="Create Account")
            self.toggleLabel.configure(text="Already have an account?")
            self.toggleBtn.configure(text="Sign In")

            self.confirmLabel.grid(row=6, column=0, padx=30, sticky="w")
            self.confirmPassword.grid(row=6, column=0, padx=30, pady=(20, 12), sticky="ew")

    def handlesAuthentication(self):
        # Grabs the username and password
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        # Checks if logged in 
        if self.isInLoginMode:
            self.logUserIn(username, password)
        else:
            self.registerAccount(username, password)

    # Logs the user into the account
    def logUserIn(self, username, password):
        authenticated, msg = verifyLogin(username, password)
        if authenticated:
            self.setStaus("", error=False)
            self.onAuthenticated(username)
        else:
            self.setStaus(msg, error=True)

    # Creates the Users Account
    def registerAccount(self, username, password):
        # Checks if the password in both boxes are the same
        if password != self.confirmPassword.get():
            self.setStaus("Passwords do not match.", error=True)
            return

        # Creates User
        authenticated, msg = createUser(username, password)
        if authenticated:
            self.setStaus("Account created! You can now sign in.", error=False)
            self.chooseMode()
        else:
            self.setStaus(msg, error=True)

    def setStaus(self, message, error=True):
        self.status_label.configure(text=message,text_color=("#c0392b", "#e74c3c") if error else ("#27ae60", "#2ecc71"))