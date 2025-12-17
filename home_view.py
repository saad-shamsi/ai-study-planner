"""
Enhanced Home View with All Advanced Features
Study Pet, Mood Tracker, Streak Garden, Pomodoro, Quick Actions, etc.
"""

import customtkinter as ctk
from datetime import datetime, timedelta
from database import db
from config import COLORS

# Import advanced widgets
from study_pet import StudyPet
from mood_tracker import MoodTracker
from advanced_widgets import (
    StreakGarden, PomodoroTimer, QuickActions,
    MotivationWidget, NotificationsPanel
)


class HomeView:
    """Enhanced home dashboard with all features"""
    
    def __init__(self, parent, dashboard):
        self.parent = parent
        self.dashboard = dashboard
        self.user_id = dashboard.user['user_id']
        
        self.create_ui()
    
    def create_ui(self):
        """Create enhanced home interface"""
        
        # Main scrollable frame
        main_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color="transparent"
        )
        main_frame.pack(fill="both", expand=True, padx=35, pady=35)
        
        # ==================== TOP SECTION ====================
        
        # Welcome header with date
        self.create_header(main_frame)
        
        # Mood Tracker (full width)
        mood_tracker = MoodTracker(main_frame, self.user_id)
        mood_tracker.pack(fill="x", pady=(0, 20))
        
        # ==================== MAIN CONTENT GRID ====================
        
        # 3-column layout
        content_grid = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_grid.pack(fill="both", expand=True)
        
        content_grid.grid_columnconfigure(0, weight=1)
        content_grid.grid_columnconfigure(1, weight=1)
        content_grid.grid_columnconfigure(2, weight=1)
        
        # Column 1: Study Pet + Streak Garden
        col1 = ctk.CTkFrame(content_grid, fg_color="transparent")
        col1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        study_pet = StudyPet(col1, self.user_id)
        study_pet.pack(fill="x", pady=(0, 20))
        
        streak_garden = StreakGarden(col1, self.user_id)
        streak_garden.pack(fill="x", pady=(0, 20))
        
        motivation = MotivationWidget(col1, self.user_id)
        motivation.pack(fill="x")
        
        # Column 2: Pomodoro Timer + Quick Actions
        col2 = ctk.CTkFrame(content_grid, fg_color="transparent")
        col2.grid(row=0, column=1, sticky="nsew", padx=10)
        
        pomodoro = PomodoroTimer(col2, self.user_id)
        pomodoro.pack(fill="x", pady=(0, 20))
        
        quick_actions = QuickActions(col2, self.dashboard)
        quick_actions.pack(fill="x")
        
        # Column 3: Stats + Notifications + Recent Activity
        col3 = ctk.CTkFrame(content_grid, fg_color="transparent")
        col3.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        
        self.create_stats_card(col3)
        
        notifications = NotificationsPanel(col3, self.user_id)
        notifications.pack(fill="x", pady=(0, 20))
        
        self.create_recent_activity(col3)
    
    def create_header(self, parent):
        """Create welcome header"""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        
        # Left: Welcome text
        left_header = ctk.CTkFrame(header, fg_color="transparent")
        left_header.pack(side="left")
        
        ctk.CTkLabel(
            left_header,
            text=f"Welcome back, {self.dashboard.user['full_name']}! 👋",
            font=("Arial Black", 34),
            text_color=COLORS['text']
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            left_header,
            text="Here's your personalized study dashboard",
            font=("Arial", 15),
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 0))
        
        # Right: Date card
        date_card = ctk.CTkFrame(
            header,
            fg_color=COLORS['primary'],
            corner_radius=15
        )
        date_card.pack(side="right", padx=20)
        
        today = datetime.now()
        
        ctk.CTkLabel(
            date_card,
            text=today.strftime("%B %d, %Y"),
            font=("Arial Bold", 15),
            text_color="white"
        ).pack(padx=25, pady=(12, 3))
        
        ctk.CTkLabel(
            date_card,
            text=today.strftime("%A"),
            font=("Arial", 12),
            text_color="white"
        ).pack(padx=25, pady=(0, 12))
    
    def create_stats_card(self, parent):
        """Create quick stats overview"""
        stats_card = ctk.CTkFrame(
            parent,
            fg_color=COLORS['card'],
            corner_radius=20
        )
        stats_card.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            stats_card,
            text="📊 Quick Stats",
            font=("Arial Black", 18),
            text_color=COLORS['text']
        ).pack(pady=(25, 20), padx=25, anchor="w")
        
        stats = [
            ("📚", "Subjects", len(self.dashboard.subjects), COLORS['info']),
            ("⏱️", "Study Hours", f"{self.dashboard.total_study_time // 60}h", COLORS['success']),
            ("📝", "Sessions", len(self.dashboard.sessions), COLORS['warning']),
            ("🔥", "Streak", db.get_current_streak(self.user_id), COLORS['secondary'])
        ]
        
        for icon, label, value, color in stats:
            stat_row = ctk.CTkFrame(
                stats_card,
                fg_color=COLORS['background'],
                corner_radius=10
            )
            stat_row.pack(fill="x", padx=25, pady=5)
            
            content = ctk.CTkFrame(stat_row, fg_color="transparent")
            content.pack(fill="x", padx=15, pady=10)
            
            # Icon
            icon_bg = ctk.CTkFrame(
                content,
                fg_color=color,
                corner_radius=8,
                width=35,
                height=35
            )
            icon_bg.pack(side="left")
            icon_bg.pack_propagate(False)
            
            ctk.CTkLabel(
                icon_bg,
                text=icon,
                font=("Arial", 18)
            ).place(relx=0.5, rely=0.5, anchor="center")
            
            # Text
            text_frame = ctk.CTkFrame(content, fg_color="transparent")
            text_frame.pack(side="left", padx=12, fill="x", expand=True)
            
            ctk.CTkLabel(
                text_frame,
                text=label,
                font=("Arial", 11),
                text_color=COLORS['text_light'],
                anchor="w"
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                text_frame,
                text=str(value),
                font=("Arial Bold", 16),
                text_color=COLORS['text'],
                anchor="w"
            ).pack(anchor="w")
        
        ctk.CTkFrame(stats_card, fg_color="transparent", height=15).pack()
    
    def create_recent_activity(self, parent):
        """Create recent sessions list"""
        activity_card = ctk.CTkFrame(
            parent,
            fg_color=COLORS['card'],
            corner_radius=20
        )
        activity_card.pack(fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(activity_card, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(25, 15))
        
        ctk.CTkLabel(
            header,
            text="📋 Recent Sessions",
            font=("Arial Black", 18),
            text_color=COLORS['text']
        ).pack(side="left")
        
        ctk.CTkButton(
            header,
            text="View All",
            font=("Arial Bold", 11),
            width=80,
            height=30,
            corner_radius=8,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary'],
            text_color="white",
            command=lambda: self.dashboard.navigate_to("planner")
        ).pack(side="right")
        
        # Sessions
        if self.dashboard.sessions:
            for session in self.dashboard.sessions[:4]:
                session_item = ctk.CTkFrame(
                    activity_card,
                    fg_color=COLORS['background'],
                    corner_radius=10
                )
                session_item.pack(fill="x", padx=25, pady=5)
                
                # Color bar
                color_bar = ctk.CTkFrame(
                    session_item,
                    width=4,
                    fg_color=session['color_code']
                )
                color_bar.pack(side="left", fill="y")
                
                # Content
                content = ctk.CTkFrame(session_item, fg_color="transparent")
                content.pack(side="left", fill="x", expand=True, padx=12, pady=10)
                
                ctk.CTkLabel(
                    content,
                    text=session['subject_name'],
                    font=("Arial Bold", 13),
                    text_color=COLORS['text'],
                    anchor="w"
                ).pack(anchor="w")
                
                ctk.CTkLabel(
                    content,
                    text=f"{session['session_date']} • {session['duration_minutes']} min",
                    font=("Arial", 10),
                    text_color=COLORS['text_light'],
                    anchor="w"
                ).pack(anchor="w")
        else:
            ctk.CTkLabel(
                activity_card,
                text="No sessions yet\nStart studying! 🚀",
                font=("Arial", 13),
                text_color=COLORS['text_light'],
                justify="center"
            ).pack(pady=40)
        
        ctk.CTkFrame(activity_card, fg_color="transparent", height=15).pack()