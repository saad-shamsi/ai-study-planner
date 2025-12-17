"""
Leaderboard View - Community Ranking
"""

import customtkinter as ctk
from config import COLORS
from database import db

class LeaderboardView:
    """Displays the community leaderboard"""
    
    def __init__(self, parent, dashboard):
        self.parent = parent
        self.dashboard = dashboard
        
        self.create_ui()
        self.load_data()
        
    def create_ui(self):
        """Create leaderboard UI"""
        
        # Main container
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=35, pady=35)
        
        # Header
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        
        ctk.CTkLabel(
            header,
            text="🏆 Community Leaderboard",
            font=("Arial Black", 28),
            text_color=COLORS['text']
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text="Top students this week",
            font=("Arial", 14),
            text_color=COLORS['text_light']
        ).pack(side="left", padx=15, pady=(10, 0))
        
        # Leaderboard List (Scrollable)
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.scroll_frame.pack(fill="both", expand=True)
        
    def load_data(self):
        """Load and display leaderboard data"""
        leaders = db.get_leaderboard(limit=20)
        
        if not leaders:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No data available yet.",
                font=("Arial", 16),
                text_color=COLORS['text_light']
            ).pack(pady=50)
            return
            
        for index, student in enumerate(leaders):
            self.create_student_card(index + 1, student)
            
    def create_student_card(self, rank, student):
        """Create a card for a student"""
        
        # Colors based on rank
        if rank == 1:
            bg_color = "#FFD700" # Gold
            text_color = "black"
        elif rank == 2:
            bg_color = "#C0C0C0" # Silver
            text_color = "black"
        elif rank == 3:
            bg_color = "#CD7F32" # Bronze
            text_color = "white"
        else:
            bg_color = COLORS['card']
            text_color = COLORS['text']
            
        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=bg_color,
            corner_radius=15,
            height=70
        )
        card.pack(fill="x", pady=6, padx=10)
        card.pack_propagate(False)
        
        # Rank
        ctk.CTkLabel(
            card,
            text=f"#{rank}",
            font=("Arial Black", 20),
            text_color=text_color
        ).pack(side="left", padx=25)
        
        # Name & Level
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            info_frame,
            text=student['full_name'],
            font=("Arial Bold", 15),
            text_color=text_color
        ).pack(anchor="w", pady=(12, 0))
        
        ctk.CTkLabel(
            info_frame,
            text=f"@{student['username']} • {student.get('student_level', 'Student')}",
            font=("Arial", 12),
            text_color=text_color if rank <= 3 else COLORS['text_light']
        ).pack(anchor="w")
        
        # Study Time
        minutes = int(student['total_minutes'])
        hours = minutes // 60
        mins = minutes % 60
        
        time_text = f"{hours}h {mins}m"
        
        ctk.CTkLabel(
            card,
            text=time_text,
            font=("Arial Black", 16),
            text_color=text_color
        ).pack(side="right", padx=25)
