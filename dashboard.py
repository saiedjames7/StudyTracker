# Imports relevant modules
import customtkinter as ctk
from data_manager import readUserSessions, deleteSession
from session_form import SessionFormDialog
from stats import StatsPanel

# Creates Dashboard Class
class Dashboard(ctk.CTkFrame):

    def __init__(self, parent, username: str, onLogout):
        super().__init__(parent, fg_color="transparent")
        self.username = username
        self.onLogout = onLogout
        self.filterSubject = "All"
        self.searchQuery = ""

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.buildSidebar()
        self.buildMainArea()
        self.loadSessions()

    # Defines the Sidebar for the UI
    def buildSidebar(self):

        sidebar = ctk.CTkFrame(self, width=240, fg_color=("#f8f8fc", "#16162a"), corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_columnconfigure(0, weight=1)
        sidebar.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(sidebar, text="StudyTrack", font=ctk.CTkFont(family="Georgia", size=22, weight="bold"), text_color=("#4f46e5", "#818cf8")).grid(row=0, column=0, padx=20, pady=(24, 4), sticky="w")
        ctk.CTkLabel(sidebar, text=f"Hi, {self.username}", font=ctk.CTkFont(size=12), text_color=("gray50", "gray55")).grid(row=1, column=0, padx=20, pady=(0, 16), sticky="w")

        self.statsPanel = StatsPanel(sidebar, self.username)
        self.statsPanel.grid(row=2, column=0, padx=20, pady=(0, 8), sticky="new")

        ctk.CTkLabel(sidebar, text="Filter by Subject", font=ctk.CTkFont(size=12, weight="bold"), anchor="w").grid(row=3, column=0, padx=20, pady=(16, 4), sticky="w")

        self.filterVar = ctk.StringVar(value="All")
        self.filterMenu = ctk.CTkOptionMenu(sidebar, values=["All"], variable=self.filterVar, height=34, corner_radius=8, fg_color=("#eeeef8", "#252535"), button_color=("#4f46e5", "#6366f1"), button_hover_color=("#3730a3", "#4f46e5"), command=self.onFilterChange)
        self.filterMenu.grid(row=4, column=0, padx=20, pady=(0, 8), sticky="ew")

        ctk.CTkButton(sidebar, text="Sign Out", height=34, corner_radius=8, fg_color="transparent", border_width=1, border_color=("#d0d0d0", "#3e3e5e"), text_color=("gray40", "gray60"), hover_color=("gray90", "gray20"), command=self.onLogout).grid(row=5, column=0, padx=20, pady=(8, 24), sticky="ew")

    # Creates Main Body of GUI (Dashboard)
    def buildMainArea(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        topbar = ctk.CTkFrame(main, height=64, fg_color=("#ffffff", "#1e1e2e"))
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.grid_columnconfigure(1, weight=1)
        topbar.grid_propagate(False)

        ctk.CTkLabel(topbar, text="My Study Sessions", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=24, pady=16, sticky="w")

        self.searchEntry = ctk.CTkEntry(topbar, placeholder_text="Search by subject or notes...", height=34, width=220, corner_radius=8)
        self.searchEntry.grid(row=0, column=1, padx=12, pady=14, sticky="e")
        self.searchEntry.bind("<KeyRelease>", self.onSearch)

        ctk.CTkButton(topbar, text="+ Log Session", height=34, corner_radius=8, font=ctk.CTkFont(size=13, weight="bold"), fg_color=("#4f46e5", "#6366f1"), hover_color=("#3730a3", "#4f46e5"), command=self.openAddForm).grid(row=0, column=2, padx=24, pady=14)

        self.sessionsFrame = ctk.CTkScrollableFrame(main, fg_color=("#f4f4f8", "#13131f"))
        self.sessionsFrame.grid(row=1, column=0, sticky="nsew")
        self.sessionsFrame.grid_columnconfigure(0, weight=1)

    # Loads Study Sessions from CSV File
    def loadSessions(self):
        for w in self.sessionsFrame.winfo_children(): w.destroy()

        sessions = readUserSessions(self.username)
        subjects = sorted(list(set(s["subject"] for s in sessions)))
        self.filterMenu.configure(values=["All"] + subjects)

        if self.filterSubject != "All": sessions = [s for s in sessions if s["subject"] == self.filterSubject]

        q = self.searchQuery.lower()
        if q: sessions = [s for s in sessions if q in s["subject"].lower() or q in s.get("notes", "").lower()]

        if not sessions:
            self.emptyState()
            return

        for i, s in enumerate(sessions): self.renderCard(s, i)
        self.statsPanel.refresh()

    # Resets the State
    def emptyState(self):
        empty = ctk.CTkFrame(self.sessionsFrame, fg_color="transparent")
        empty.grid(row=0, column=0, pady=80)
        ctk.CTkLabel(empty, text="No sessions found", font=ctk.CTkFont(size=18, weight="bold"), text_color=("gray50", "gray55")).pack()
        ctk.CTkLabel(empty, text='Click "+ Log Session" to record your first study session.', font=ctk.CTkFont(size=13), text_color=("gray60", "gray50")).pack(pady=(6, 0))

    # Defines the Card to hold Subjects
    def renderCard(self, session, i):
        card = ctk.CTkFrame(self.sessionsFrame, corner_radius=12, fg_color=("#ffffff", "#1e1e2e"), border_width=1, border_color=("#e0e0ee", "#2e2e4e"))
        card.grid(row=i, column=0, padx=20, pady=6, sticky="ew")
        card.grid_columnconfigure(1, weight=1)

        colours = ["#6366f1", "#06b6d4", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899"]
        ctk.CTkFrame(card, width=4, corner_radius=2, fg_color=colours[hash(session["subject"]) % len(colours)]).grid(row=0, column=0, rowspan=3, padx=(12, 12), pady=14, sticky="ns")

        ctk.CTkLabel(card, text=session["subject"], font=ctk.CTkFont(size=15, weight="bold"), anchor="w").grid(row=0, column=1, sticky="w", pady=(14, 0))
        ctk.CTkLabel(card, text=session["date"], font=ctk.CTkFont(size=11), text_color=("gray50", "gray55"), anchor="w").grid(row=1, column=1, sticky="w")

        notes = session.get("notes", "").strip()
        if notes:
            preview = notes[:80] + "…" if len(notes) > 80 else notes
            ctk.CTkLabel(card, text=preview, font=ctk.CTkFont(size=11), text_color=("gray55", "gray50"), anchor="w", wraplength=400).grid(row=2, column=1, sticky="w", pady=(2, 14))
        
        # Defines the Study Session Length
        duration = int(session["duration_minutes"])
        hrs= duration // 60
        mins = duration % 60

        dur = f"{hrs}h {mins}m" if hrs else f"{mins}m"

        goal = int(session.get("goal_minutes", 0))
        metGoal = goal > 0 and duration >= goal

        badge = ctk.CTkFrame(card, fg_color=("#dcfce7", "#14532d") if metGoal else ("#ede9fe", "#2e1065"), corner_radius=6)
        badge.grid(row=0, column=2, padx=(8, 12), pady=(14, 0), sticky="ne")

        ctk.CTkLabel(badge, text=dur, font=ctk.CTkFont(size=12, weight="bold"), text_color=("#166534", "#86efac") if metGoal else ("#5b21b6", "#c4b5fd")).grid(padx=10, pady=4)

        # Defines the label on the card if the goal has been met
        if metGoal: 
            ctk.CTkLabel(card, text="Goal met!", font=ctk.CTkFont(size=10), text_color=("#166534", "#86efac")).grid(row=1, column=2, padx=12, sticky="ne")
        else:
             ctk.CTkLabel(card, text="Goal not met!", font=ctk.CTkFont(size=10), text_color=("#9F2626", "#a81313")).grid(row=1, column=2, padx=12, sticky="ne")
        
        btns = ctk.CTkFrame(card, fg_color="transparent")
        btns.grid(row=2, column=2, padx=12, pady=(0, 12), sticky="se")

        ctk.CTkButton(btns, text="Edit", width=60, height=28, corner_radius=6, command=lambda s=session: self.openEditForm(s)).pack(side="left", padx=(0, 6))
        ctk.CTkButton(btns, text="Delete", width=60, height=28, corner_radius=6, command=lambda s=session: self.confirmDelete(s)).pack(side="left")

    # Defines the Forms to Add/Edit Subjects
    def openAddForm(self): SessionFormDialog(self, self.username, onSave=self.loadSessions)
    def openEditForm(self, session): SessionFormDialog(self, self.username, onSave=self.loadSessions, sessionData=session)

    # Deletes the Session
    def confirmDelete(self, session):
        dashboard = ctk.CTkToplevel(self)
        dashboard.title("Confirm Delete")
        dashboard.geometry("340x180")
        dashboard.resizable(False, False)
        dashboard.update_idletasks()
        dashboard.grab_set()

        ctk.CTkLabel(dashboard, text="Delete this session?", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(28, 6))
        ctk.CTkLabel(dashboard, text=f"{session['subject']} · {session['date']} · {session['duration_minutes']}min", font=ctk.CTkFont(size=12), text_color=("gray50", "gray55")).pack()

        row = ctk.CTkFrame(dashboard, fg_color="transparent")
        row.pack(pady=24)

        ctk.CTkButton(row, text="Cancel", width=120, height=36, command=dashboard.destroy).pack(side="left", padx=8)

        def doDelete():
            deleteSession(session["session_id"], self.username)
            dashboard.destroy()
            self.loadSessions()

        ctk.CTkButton(row, text="Delete", width=120, height=36, fg_color=("#dc2626", "#991b1b"), command=doDelete).pack(side="left", padx=8)
    
    # Filters by Subject
    def onFilterChange(self, value):
        self.filterSubject = value
        self.loadSessions()

    # Searches for subject
    def onSearch(self, e=None):
        self.searchQuery = self.searchEntry.get()
        self.loadSessions()