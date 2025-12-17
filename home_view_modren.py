"""
Modern Home View - Premium Aurora Theme
"""

import customtkinter as ctk
from datetime import datetime
from config import COLORS

class ModernHomeView:
    """Premium Aurora Home Dashboard"""
    
    def __init__(self, parent, dashboard):
        self.parent = parent
        self.dashboard = dashboard
        self.user_id = dashboard.user['user_id']
        
        self.create_ui()
    
    def create_ui(self):
        """Create premium interface"""
        
        # Main container with padding for "floating" feel
        main_frame = ctk.CTkFrame(
            self.parent,
            fg_color="transparent" 
        )
        main_frame.pack(fill="both", expand=True)
        
        # 1. Top Greeting Section
        self.create_header(main_frame)
        
        # 2. Scrollable Dashboard Area
        content_scroll = ctk.CTkScrollableFrame(
            main_frame,
            fg_color="transparent",
            height=600
        )
        content_scroll.pack(fill="both", expand=True, padx=0, pady=(0, 20))
        
        # Grid Layout (2 Columns: Main Content vs Side Widgets)
        content_scroll.grid_columnconfigure(0, weight=3) # Main
        content_scroll.grid_columnconfigure(1, weight=1) # Side
        
        # === LEFT COLUMN (Daily Focus) ===
        left_col = ctk.CTkFrame(content_scroll, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=10)
        
        self.create_hero_stats(left_col)
        self.create_schedule_section(left_col)
        
        # === RIGHT COLUMN (Quick Actions & Events) ===
        right_col = ctk.CTkFrame(content_scroll, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew", pady=10)
        
        self.create_profile_widget(right_col)
        self.create_events_widget(right_col)

    def create_header(self, parent):
        """Create clean header interaction area"""
        header = ctk.CTkFrame(parent, fg_color="transparent", height=80)
        header.pack(fill="x", pady=(10, 30))
        
        # Greeting
        left_box = ctk.CTkFrame(header, fg_color="transparent")
        left_box.pack(side="left")
        
        time_greeting = "Good Morning" if datetime.now().hour < 12 else "Good Evening"
        
        ctk.CTkLabel(
            left_box,
            text=f"{time_greeting},",
            font=("Segoe UI", 16),
            text_color=COLORS['text_light']
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            left_box,
            text=self.dashboard.user['full_name'],
            font=("Segoe UI Display", 32, "bold"),
            text_color=COLORS['text']
        ).pack(anchor="w")
        
        # Action Buttons (Search / Notifs)
        right_box = ctk.CTkFrame(header, fg_color="transparent")
        right_box.pack(side="right")
        
        self.create_icon_btn(right_box, "🔍")
        self.create_icon_btn(right_box, "🔔", badge=True)

    def create_hero_stats(self, parent):
        """High-level stats row"""
        stats_row = ctk.CTkFrame(parent, fg_color="transparent")
        stats_row.pack(fill="x", pady=(0, 25))
        
        # 3 Stats Cards
        self.create_stat_card(stats_row, "Study Time", f"{self.dashboard.total_study_time // 60}h", "⏱️", COLORS['primary'])
        self.create_stat_card(stats_row, "Sessions", str(len(self.dashboard.sessions)), "📚", COLORS['secondary'])
        self.create_stat_card(stats_row, "Streak", "Day 3", "🔥", COLORS['warning'])

    def create_stat_card(self, parent, title, value, icon, color):
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS['card'],
            corner_radius=16,
            border_width=1,
            border_color=COLORS['border']
        )
        card.pack(side="left", fill="x", expand=True, padx=8)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(padx=20, pady=20)
        
        # Icon Box
        icon_box = ctk.CTkFrame(
            content, width=45, height=45,
            fg_color=color, corner_radius=12
        )
        icon_box.pack(side="left")
        
        ctk.CTkLabel(icon_box, text=icon, font=("Segoe UI", 20)).place(relx=0.5, rely=0.5, anchor="center")
        
        # Text
        text_box = ctk.CTkFrame(content, fg_color="transparent")
        text_box.pack(side="left", padx=(15, 0))
        
        ctk.CTkLabel(
            text_box, text=value,
            font=("Segoe UI", 22, "bold"),
            text_color=COLORS['text']
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            text_box, text=title,
            font=("Segoe UI", 12),
            text_color=COLORS['text_light']
        ).pack(anchor="w")

    def create_schedule_section(self, parent):
        """Upcoming tasks/schedule"""
        section = ctk.CTkFrame(
            parent,
            fg_color=COLORS['card'],
            corner_radius=20,
            border_width=1,
            border_color=COLORS['border']
        )
        section.pack(fill="both", expand=True, padx=8)
        
        # Header
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(
            header, text="Today's Focus",
            font=("Segoe UI", 18, "bold"),
            text_color=COLORS['text']
        ).pack(side="left")
        
        ctk.CTkButton(
            header, text="View Calendar",
            width=100, height=30,
            fg_color=COLORS['hover'],
            text_color=COLORS['primary'],
            font=("Segoe UI", 12, "bold"),
            corner_radius=8,
            command=lambda: self.dashboard.navigate_to("planner")
        ).pack(side="right")
        
        # List
        tasks_frame = ctk.CTkFrame(section, fg_color="transparent")
        tasks_frame.pack(fill="both", expand=True, padx=15, pady=(0, 20))
        
        # Dummy Tasks for UI Demo
        tasks = [
            ("Math - Calculus II", "10:00 AM", COLORS['primary']),
            ("Physics - Mechanics", "02:00 PM", COLORS['secondary']),
            ("CS - Algorithms", "04:30 PM", COLORS['success'])
        ]
        
        for title, time, color in tasks:
            row = ctk.CTkFrame(tasks_frame, fg_color=COLORS['background'], corner_radius=12)
            row.pack(fill="x", pady=5)
            
            stripe = ctk.CTkFrame(row, width=6, height=50, fg_color=color, corner_radius=0)
            stripe.pack(side="left", fill="y")
            
            content = ctk.CTkFrame(row, fg_color="transparent")
            content.pack(side="left", fill="x", expand=True, padx=15, pady=12)
            
            ctk.CTkLabel(
                content, text=title,
                font=("Segoe UI", 14, "bold"),
                text_color=COLORS['text']
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                content, text=f"Scheduled for {time}",
                font=("Segoe UI", 11),
                text_color=COLORS['text_light']
            ).pack(anchor="w")
            
            ctk.CTkButton(
                row, text="Start",
                width=70, height=30,
                fg_color="transparent",
                border_width=1,
                border_color=color,
                text_color=color,
                hover_color=color,
                command=lambda: None
            ).pack(side="right", padx=15)

    def create_events_widget(self, parent):
        """Right side events widget"""
        widget = ctk.CTkFrame(
            parent,
            fg_color=COLORS['card'],
            corner_radius=20,
            border_width=1,
            border_color=COLORS['border']
        )
        widget.pack(fill="x", pady=(20, 0))
        
        ctk.CTkLabel(
            widget, text="Upcoming Events",
            font=("Segoe UI", 16, "bold"),
            text_color=COLORS['text']
        ).pack(anchor="w", padx=20, pady=20)
        
        events = [
            ("Webinar: AI Future", "Tomorrow, 2 PM", "🎤"),
            ("Study Group", "Fri, 5 PM", "👥")
        ]
        
        for title, time, icon in events:
            row = ctk.CTkFrame(widget, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=(0, 15))
            
            ctk.CTkLabel(row, text=icon, font=("Segoe UI", 20)).pack(side="left", padx=(0, 10))
            
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left")
            
            ctk.CTkLabel(
                info, text=title,
                font=("Segoe UI", 13, "bold"),
                text_color=COLORS['text']
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info, text=time,
                font=("Segoe UI", 11),
                text_color=COLORS['text_light']
            ).pack(anchor="w")

    def create_profile_widget(self, parent):
        """Mini Profile Summary"""
        widget = ctk.CTkFrame(
            parent,
            fg_color=COLORS['primary'], # Brand color
            corner_radius=20
        )
        widget.pack(fill="x")
        
        content = ctk.CTkFrame(widget, fg_color="transparent")
        content.pack(padx=20, pady=20)
        
        ctk.CTkLabel(
            content, text="Pro Plan Active",
            font=("Segoe UI", 14, "bold"),
            text_color="#0F172A"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            content, text="You have access to all\nAI features.",
            font=("Segoe UI", 12),
            text_color="#0F172A",
            justify="left"
        ).pack(anchor="w", pady=(5, 15))
        
        ctk.CTkButton(
            content, text="Upgrade Tier",
            fg_color="#0F172A",
            text_color="white",
            height=35,
            corner_radius=10,
            hover_color="#1E293B"
        ).pack(fill="x")

    def create_icon_btn(self, parent, icon, badge=False):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(side="right", padx=5)
        
        btn = ctk.CTkButton(
            container, text=icon, width=45, height=45,
            fg_color=COLORS['card'],
            hover_color=COLORS['hover'],
            text_color=COLORS['text'],
            font=("Segoe UI", 18),
            corner_radius=15,
            command=lambda: None
        )
        btn.pack()
        
        if badge:
            badge_indicator = ctk.CTkFrame(
                container, width=12, height=12,
                fg_color="#ef4444", corner_radius=6,
                border_width=2, border_color=COLORS['background']
            )
            badge_indicator.place(relx=0.75, rely=0.2)
