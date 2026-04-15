import customtkinter as ctk
from data_manager import getStats


class StatsPanel(ctk.CTkFrame):

    def __init__(self, parent, username: str):
        super().__init__(parent, fg_color="transparent")

        self.username = username
        self.grid_columnconfigure(0, weight=1)

        # Load stats straight away when panel is created
        self.refresh()

    def refresh(self):
        # wWpe old UI before rebuilding (simplest way to keep it updated)
        for w in self.winfo_children(): w.destroy()

        stats = getStats(self.username)
        self.buildUI(stats)

    def buildUI(self, stats: dict):

        # Small title at top
        ctk.CTkLabel(self, text="Your Stats", font=ctk.CTkFont(size=15, weight="bold"), anchor="w").grid(row=0, column=0, pady=(0,10), sticky="w")

        # Container for the 4 main stat cards
        cardFrame = ctk.CTkFrame(self, fg_color="transparent")
        cardFrame.grid(row=1, column=0, sticky="ew")
        cardFrame.grid_columnconfigure((0,1), weight=1)

        totalHours = round(stats["total_minutes"] / 60, 1)

        # Quick overview cards
        self.statCard(cardFrame, "Total Hours", f"{totalHours}h", 0, 0)
        self.statCard(cardFrame, "Sessions", str(stats["session_count"]), 0, 1)
        self.statCard(cardFrame, "Day Streak", f"{stats['current_streak']}🔥", 1, 0)
        self.statCard(cardFrame, "Top Subject", stats["top_subject"], 1, 1, small=True)

        # Only show breakdown if we actually have data
        if stats["subjects"]:

            ctk.CTkLabel(self, text="Time by Subject", font=ctk.CTkFont(size=13, weight="bold"), anchor="w").grid(row=2, column=0, pady=(16,6), sticky="w")

            sortedSubjects = sorted(stats["subjects"].items(), key=lambda x: x[1], reverse=True)
            total = stats["total_minutes"] if stats["total_minutes"] > 0 else 1

            subjectFrame = ctk.CTkFrame(self, fg_color="transparent")
            subjectFrame.grid(row=3, column=0, sticky="ew")
            subjectFrame.grid_columnconfigure(0, weight=1)

            colors = ["#6366f1","#06b6d4","#10b981","#f59e0b","#ef4444","#8b5cf6","#ec4899","#14b8a6"]

            for i, (subject, minutes) in enumerate(sortedSubjects[:6]):
                pct = int((minutes / total) * 100)
                self.subjectRow(subjectFrame, subject, minutes, pct, colors[i % len(colors)], i)

    def statCard(self, parent, label: str, value: str, row: int, col: int, small: bool = False):

        # One reusable card for the top stats
        card = ctk.CTkFrame(parent, corner_radius=10, fg_color=("#f0f0f8","#252535"), border_width=1, border_color=("#e0e0ee","#3a3a5a"))
        card.grid(row=row, column=col, padx=4, pady=4, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=10), text_color=("gray50","gray55"), anchor="w").grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")

        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=14 if small else 20, weight="bold"), anchor="w", wraplength=100).grid(row=1, column=0, padx=10, pady=(2,10), sticky="w")

    def subjectRow(self, parent, subject: str, minutes: int, pct: int, color: str, index: int):

        # One row per subject with a small progress bar
        rowFrame = ctk.CTkFrame(parent, fg_color="transparent")
        rowFrame.grid(row=index, column=0, pady=3, sticky="ew")
        rowFrame.grid_columnconfigure(1, weight=1)

        # Little colored dot so each subject is easy to visually separate
        ctk.CTkFrame(rowFrame, width=10, height=10, corner_radius=5, fg_color=color).grid(row=0, column=0, padx=(0,8))

        displayName = subject if len(subject) <= 14 else subject[:13] + "…"

        ctk.CTkLabel(rowFrame, text=displayName, font=ctk.CTkFont(size=11), anchor="w").grid(row=0, column=1, sticky="w")

        hrs = minutes // 60
        mins = minutes % 60
        timeStr = f"{hrs}h {mins}m" if hrs > 0 else f"{mins}m"

        ctk.CTkLabel(rowFrame, text=f"{timeStr} ({pct}%)", font=ctk.CTkFont(size=11), text_color=("gray50","gray55")).grid(row=0, column=2, padx=(8,0))

        bar = ctk.CTkProgressBar(parent, height=5, corner_radius=3, fg_color=("#e0e0e0","#333350"), progress_color=color)
        bar.grid(row=index * 2 + 1, column=0, pady=(0,4), sticky="ew")
        bar.set(pct / 100)