import customtkinter as ctk
from datetime import date
from data_manager import createSession, updateSessions

# simple dropdown list for subjects
SUBJECTS = ["Mathematics","Computer Science","English","Physics","Chemistry","Biology","History","Geography","Psychology","Business Studies","Economics","Art & Design","Other"]


class SessionFormDialog(ctk.CTkToplevel):

    def __init__(self, parent, username: str, onSave, sessionData: dict = None):
        super().__init__(parent)

        self.username = username
        self.onSave = onSave
        self.sessionData = sessionData
        self.isEdit = sessionData is not None

        self.title("Edit Session" if self.isEdit else "Log New Session")
        self.geometry("440x560")
        self.resizable(False, False)
        self.after(0, self.grab_set)
        self.focus_set()

        self.createUI()
        if self.isEdit: self.populateFields()

    def createUI(self):
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color=("#4f46e5","#6366f1"), corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(header, text="Edit Session" if self.isEdit else "Log New Session", font=ctk.CTkFont(size=18, weight="bold"), text_color="white").grid(row=0, column=0, padx=24, pady=18, sticky="w")

        body = ctk.CTkScrollableFrame(self, fg_color="transparent")
        body.grid(row=1, column=0, padx=20, pady=12, sticky="nsew")
        body.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        def label(t, r): ctk.CTkLabel(body, text=t, font=ctk.CTkFont(size=12, weight="bold"), anchor="w").grid(row=r, column=0, sticky="w")

        label("Subject *",0)
        self.subjectVar = ctk.StringVar(value=SUBJECTS[0])
        self.subjectMenu = ctk.CTkOptionMenu(body, values=SUBJECTS, variable=self.subjectVar, height=38, corner_radius=8, fg_color=("#f4f4f8","#2a2a3e"), button_color=("#4f46e5","#6366f1"), button_hover_color=("#3730a3","#4f46e5"))
        self.subjectMenu.grid(row=1, column=0, pady=(4,12), sticky="ew")

        self.customSubject = ctk.CTkEntry(body, placeholder_text="Enter subject name...", height=38, corner_radius=8)
        self.subjectVar.trace_add("write", self.onSubjectChange)

        label("Duration (minutes) *",2)
        self.durationEntry = ctk.CTkEntry(body, placeholder_text="e.g. 45", height=38, corner_radius=8)
        self.durationEntry.grid(row=3, column=0, pady=(4,12), sticky="ew")

        label("Daily Goal (minutes)",4)
        self.goalEntry = ctk.CTkEntry(body, placeholder_text="e.g. 120", height=38, corner_radius=8)
        self.goalEntry.grid(row=5, column=0, pady=(4,12), sticky="ew")

        label("Date *",6)
        self.dateEntry = ctk.CTkEntry(body, placeholder_text="YYYY-MM-DD", height=38, corner_radius=8)
        self.dateEntry.insert(0, str(date.today()))
        self.dateEntry.grid(row=7, column=0, pady=(4,12), sticky="ew")

        label("Notes",8)
        self.notesBox = ctk.CTkTextbox(body, height=90, corner_radius=8, fg_color=("#f4f4f8","#2a2a3e"), border_width=1, border_color=("#d0d0d0","#3e3e5e"))
        self.notesBox.grid(row=9, column=0, pady=(4,12), sticky="ew")

        self.statusLabel = ctk.CTkLabel(body, text="", font=ctk.CTkFont(size=12), text_color=("#c0392b","#e74c3c"), wraplength=360)
        self.statusLabel.grid(row=10, column=0, pady=(0,4))

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, padx=20, pady=(0,16), sticky="ew")
        footer.grid_columnconfigure((0,1), weight=1)

        ctk.CTkButton(footer, text="Cancel", height=40, corner_radius=8, fg_color=("gray85","gray25"), command=self.destroy).grid(row=0, column=0, padx=(0,6), sticky="ew")
        ctk.CTkButton(footer, text="Save Session" if self.isEdit else "Log Session", height=40, corner_radius=8, fg_color=("#4f46e5","#6366f1"), font=ctk.CTkFont(weight="bold"), command=self.saveData).grid(row=0, column=1, padx=(6,0), sticky="ew")

    def onSubjectChange(self, *args):
        if self.subjectVar.get() == "Other":
            self.customSubject.grid(row=1, column=0, pady=(0,12), sticky="ew")
        else:
            self.customSubject.grid_forget()

    def populateFields(self):
        s = self.sessionData
        if s["subject"] in SUBJECTS: self.subjectVar.set(s["subject"])
        else: self.subjectVar.set("Other"); self.customSubject.insert(0, s["subject"])

        self.durationEntry.insert(0, s["duration_minutes"])
        self.goalEntry.insert(0, s.get("goal_minutes", "0"))
        self.dateEntry.insert(0, s["date"])
        self.notesBox.insert("1.0", s.get("notes", ""))

    def saveData(self):
        subject = self.subjectVar.get()
        if subject == "Other":
            subject = self.customSubject.get().strip()
            if not subject: self.setStatus("Please enter a subject name."); return

        try: duration = int(self.durationEntry.get().strip())
        except: self.setStatus("Duration must be a number."); return

        goalRaw = self.goalEntry.get().strip()
        try: goal = int(goalRaw) if goalRaw else 0
        except: self.setStatus("Goal must be a number."); return

        sessionDate = self.dateEntry.get().strip()
        notes = self.notesBox.get("1.0","end").strip()

        if self.isEdit:
            success, msg = updateSessions(self.sessionData["session_id"], self.username, subject, duration, sessionDate, notes, goal)
        else:
            success, msg = createSession(self.username, subject, duration, sessionDate, notes, goal)

        if success: self.onSave(); self.destroy()
        else: self.setStatus(msg)

    def setStatus(self, msg): 
        self.statusLabel.configure(text=msg)