"""
Home View with ALL Aesthetic Enhancements Applied
Shadow effects, hover animations, badges, circular progress, etc.
"""

import customtkinter as ctk
from datetime import datetime, timedelta
from database import db
from tkinter import Canvas
import math

# Modern colors
# Modern colors - Synced with config.py (Aurora Dark)
MODERN_COLORS = {
    'background': '#1E293B', # Sidebar/Card color for variation
    'card': '#0F172A',       # Deep background for contrast
    'primary': '#38BDF8',
    'secondary': '#818CF8',
    'success': '#34D399',
    'warning': '#fbbf24',
    'info': '#60A5FA',
    'text': '#F8FAFC',
    'text_light': '#94A3B8',
    'shadow': '#334155'      # Border color as shadow
}


class EnhancedHomeView:
    """Home view with advanced aesthetic features"""
    
    def __init__(self, parent, dashboard):
        self.parent = parent
        self.dashboard = dashboard
        self.user_id = dashboard.user['user_id']
        
        self.create_ui()
    
    def create_ui(self):
        """Create enhanced UI"""
        # Main scrollable frame
        main_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color="transparent"
        )
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header with search and notifications
        self.create_modern_header(main_frame)
        
        # Main grid
        content_grid = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_grid.pack(fill="both", expand=True, pady=20)
        
        content_grid.grid_columnconfigure(0, weight=2)
        content_grid.grid_columnconfigure(1, weight=2)
        content_grid.grid_columnconfigure(2, weight=1)
        
        # Left column
        self.create_stats_overview(content_grid)
        
        # Middle column
        self.create_activity_timeline(content_grid)
        
        # Right column
        self.create_circular_stats(content_grid)
    
    def create_modern_header(self, parent):
        """Header with search and icons"""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        # Left: Greeting
        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")
        
        ctk.CTkLabel(
            left,
            text=f"Hello, {self.dashboard.user['full_name']}! 👋",
            font=("Segoe UI", 28, "bold"),
            text_color=MODERN_COLORS['text']
        ).pack(anchor="w")
        
        date_label = ctk.CTkLabel(
            left,
            text=datetime.now().strftime("%A, %B %d, %Y"),
            font=("Segoe UI", 13),
            text_color=MODERN_COLORS['text_light']
        )
        date_label.pack(anchor="w", pady=(3, 0))
        
        # Right: Search and icons
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right")
        
        # Search bar with glass effect
        search_frame = ctk.CTkFrame(
            right,
            fg_color=MODERN_COLORS['card'],
            corner_radius=20,
            border_width=1,
            border_color=MODERN_COLORS['shadow']
        )
        search_frame.pack(side="left", padx=5)
        
        ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=("Segoe UI", 14)
        ).pack(side="left", padx=(12, 5))
        
        ctk.CTkEntry(
            search_frame,
            placeholder_text="Search...",
            font=("Segoe UI", 12),
            width=200,
            border_width=0,
            fg_color="transparent"
        ).pack(side="left", padx=(0, 12), pady=10)
        
        # Notification button with badge
        self.create_icon_with_badge(right, "🔔", 3)
        
        # Settings button
        self.create_hover_button(right, "⚙️")
    
    def create_icon_with_badge(self, parent, icon, count):
        """Icon with notification badge"""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(side="left", padx=5)
        
        btn = ctk.CTkButton(
            container,
            text=icon,
            font=("Segoe UI", 18),
            width=45,
            height=45,
            corner_radius=22,
            fg_color=MODERN_COLORS['card'],
            hover_color=MODERN_COLORS['shadow'],
            border_width=1,
            border_color=MODERN_COLORS['shadow']
        )
        btn.pack()
        
        if count > 0:
            badge = ctk.CTkFrame(
                container,
                fg_color="#FF5252",
                corner_radius=9,
                width=18,
                height=18
            )
            badge.place(relx=0.7, rely=0.2)
            badge.pack_propagate(False)
            
            ctk.CTkLabel(
                badge,
                text=str(count),
                font=("Segoe UI", 9, "bold"),
                text_color="white"
            ).place(relx=0.5, rely=0.5, anchor="center")
    
    def create_hover_button(self, parent, icon):
        """Simple icon button"""
        btn = ctk.CTkButton(
            parent,
            text=icon,
            font=("Segoe UI", 18),
            width=45,
            height=45,
            corner_radius=22,
            fg_color=MODERN_COLORS['card'],
            hover_color=MODERN_COLORS['shadow'],
            border_width=1,
            border_color=MODERN_COLORS['shadow']
        )
        btn.pack(side="left", padx=5)
        return btn
    
    def create_stats_overview(self, parent):
        """Left column with shadow cards"""
        col = ctk.CTkFrame(parent, fg_color="transparent")
        col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Quick stats with shadow
        self.create_shadow_card_with_stats(col)
        
        # Recent subjects
        self.create_subjects_card(col)
    
    def create_shadow_card_with_stats(self, parent):
        """Card with shadow effect"""
        # Shadow layer
        shadow = ctk.CTkFrame(
            parent,
            fg_color=MODERN_COLORS['shadow'],
            corner_radius=20
        )
        shadow.pack(fill="x", pady=(0, 15))
        
        # Main card
        card = ctk.CTkFrame(
            shadow,
            fg_color=MODERN_COLORS['card'],
            corner_radius=18
        )
        card.pack(fill="x", padx=3, pady=3)
        
        # Header
        ctk.CTkLabel(
            card,
            text="📊 Quick Overview",
            font=("Segoe UI", 18, "bold"),
            text_color=MODERN_COLORS['text']
        ).pack(anchor="w", padx=25, pady=(20, 15))
        
        # Stats grid
        stats_grid = ctk.CTkFrame(card, fg_color="transparent")
        stats_grid.pack(fill="x", padx=25, pady=(0, 20))
        
        stats = [
            ("📚", "Subjects", len(self.dashboard.subjects), MODERN_COLORS['info']),
            ("⏱️", "Hours Today", "4.5h", MODERN_COLORS['success']),
            ("🔥", "Streak", db.get_current_streak(self.user_id), MODERN_COLORS['warning']),
            ("🎯", "Goals", len(self.dashboard.goals), MODERN_COLORS['secondary'])
        ]
        
        for i, (icon, label, value, color) in enumerate(stats):
            stat_card = ctk.CTkFrame(
                stats_grid,
                fg_color=color + "20",  # Light version
                corner_radius=15,
                border_width=2,
                border_color=color
            )
            stat_card.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")
            
            stats_grid.grid_columnconfigure(0, weight=1)
            stats_grid.grid_columnconfigure(1, weight=1)
            
            # Icon
            ctk.CTkLabel(
                stat_card,
                text=icon,
                font=("Segoe UI", 28)
            ).pack(pady=(15, 5))
            
            # Value
            ctk.CTkLabel(
                stat_card,
                text=str(value),
                font=("Segoe UI", 24, "bold"),
                text_color=MODERN_COLORS['text']
            ).pack()
            
            # Label
            ctk.CTkLabel(
                stat_card,
                text=label,
                font=("Segoe UI", 11),
                text_color=MODERN_COLORS['text_light']
            ).pack(pady=(0, 15))
    
    def create_subjects_card(self, parent):
        """Subjects with badges"""
        # Shadow
        shadow = ctk.CTkFrame(
            parent,
            fg_color=MODERN_COLORS['shadow'],
            corner_radius=20
        )
        shadow.pack(fill="x", pady=(0, 15))
        
        # Card
        card = ctk.CTkFrame(
            shadow,
            fg_color=MODERN_COLORS['card'],
            corner_radius=18
        )
        card.pack(fill="x", padx=3, pady=3)
        
        # Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(20, 15))
        
        ctk.CTkLabel(
            header,
            text="📖 Your Subjects",
            font=("Segoe UI", 18, "bold"),
            text_color=MODERN_COLORS['text']
        ).pack(side="left")
        
        # Badge
        badge = ctk.CTkFrame(
            header,
            fg_color=MODERN_COLORS['primary'],
            corner_radius=10,
            height=24
        )
        badge.pack(side="right")
        badge.pack_propagate(False)
        
        ctk.CTkLabel(
            badge,
            text=f"{len(self.dashboard.subjects)} Active",
            font=("Segoe UI", 10, "bold"),
            text_color="white"
        ).pack(padx=10, pady=3)
        
        # Subject items
        if self.dashboard.subjects:
            for subject in self.dashboard.subjects[:4]:
                item = ctk.CTkFrame(
                    card,
                    fg_color=MODERN_COLORS['background'],
                    corner_radius=12
                )
                item.pack(fill="x", padx=25, pady=5)
                
                content = ctk.CTkFrame(item, fg_color="transparent")
                content.pack(fill="x", padx=15, pady=12)
                
                # Color dot
                dot = ctk.CTkFrame(
                    content,
                    width=12,
                    height=12,
                    corner_radius=6,
                    fg_color=subject.get('color_code', MODERN_COLORS['primary'])
                )
                dot.pack(side="left")
                
                # Name
                ctk.CTkLabel(
                    content,
                    text=subject['subject_name'],
                    font=("Segoe UI", 13, "bold"),
                    text_color=MODERN_COLORS['text']
                ).pack(side="left", padx=12)
        
        ctk.CTkFrame(card, fg_color="transparent", height=15).pack()
    
    def create_activity_timeline(self, parent):
        """Middle column with timeline"""
        col = ctk.CTkFrame(parent, fg_color="transparent")
        col.grid(row=0, column=1, sticky="nsew", padx=10)
        
        # Shadow
        shadow = ctk.CTkFrame(
            col,
            fg_color=MODERN_COLORS['shadow'],
            corner_radius=20
        )
        shadow.pack(fill="both", expand=True)
        
        # Card
        card = ctk.CTkFrame(
            shadow,
            fg_color=MODERN_COLORS['card'],
            corner_radius=18
        )
        card.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Header
        ctk.CTkLabel(
            card,
            text="📅 Recent Activity",
            font=("Segoe UI", 18, "bold"),
            text_color=MODERN_COLORS['text']
        ).pack(anchor="w", padx=25, pady=(20, 15))
        
        # Timeline items
        if self.dashboard.sessions:
            for session in self.dashboard.sessions[:5]:
                self.create_timeline_item(card, session)
        else:
            ctk.CTkLabel(
                card,
                text="No sessions yet 🚀\nStart studying!",
                font=("Segoe UI", 14),
                text_color=MODERN_COLORS['text_light']
            ).pack(pady=40)
    
    def create_timeline_item(self, parent, session):
        """Timeline entry with dot"""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=25, pady=8)
        
        # Timeline dot
        dot_frame = ctk.CTkFrame(container, fg_color="transparent", width=30)
        dot_frame.pack(side="left")
        dot_frame.pack_propagate(False)
        
        dot = ctk.CTkFrame(
            dot_frame,
            width=14,
            height=14,
            corner_radius=7,
            fg_color=session.get('color_code', MODERN_COLORS['primary']),
            border_width=3,
            border_color=MODERN_COLORS['background']
        )
        dot.place(relx=0.5, rely=0.2, anchor="center")
        
        # Content
        content = ctk.CTkFrame(
            container,
            fg_color=MODERN_COLORS['background'],
            corner_radius=12
        )
        content.pack(side="left", fill="x", expand=True)
        
        inner = ctk.CTkFrame(content, fg_color="transparent")
        inner.pack(fill="x", padx=12, pady=10)
        
        ctk.CTkLabel(
            inner,
            text=session['subject_name'],
            font=("Segoe UI", 13, "bold"),
            text_color=MODERN_COLORS['text']
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            inner,
            text=f"{session.get('session_date', 'Today')} • {session.get('duration_minutes', 0)} min",
            font=("Segoe UI", 10),
            text_color=MODERN_COLORS['text_light']
        ).pack(anchor="w")
    
    def create_circular_stats(self, parent):
        """Right column with circular progress"""
        col = ctk.CTkFrame(parent, fg_color="transparent")
        col.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        
        # Progress cards
        stats = [
            ("Focus Time", 75, MODERN_COLORS['secondary']),
            ("Completion", 60, MODERN_COLORS['success']),
            ("Consistency", 85, MODERN_COLORS['warning'])
        ]
        
        for title, percentage, color in stats:
            self.create_circular_card(col, title, percentage, color)
    
    def create_circular_card(self, parent, title, percentage, color):
        """Card with circular progress"""
        # Shadow
        shadow = ctk.CTkFrame(
            parent,
            fg_color=MODERN_COLORS['shadow'],
            corner_radius=20
        )
        shadow.pack(fill="x", pady=(0, 15))
        
        # Card
        card = ctk.CTkFrame(
            shadow,
            fg_color=MODERN_COLORS['card'],
            corner_radius=18
        )
        card.pack(fill="x", padx=3, pady=3)
        
        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 14, "bold"),
            text_color=MODERN_COLORS['text']
        ).pack(pady=(20, 10))
        
        # Circular progress
        canvas = Canvas(
            card,
            width=110,
            height=110,
            bg=MODERN_COLORS['card'],
            highlightthickness=0
        )
        canvas.pack(pady=10)
        
        # Background circle
        canvas.create_oval(5, 5, 105, 105, outline=MODERN_COLORS['background'], width=10)
        
        # Progress arc
        extent = (percentage / 100) * 360
        canvas.create_arc(
            5, 5, 105, 105,
            start=90,
            extent=-extent,
            outline=color,
            width=10,
            style='arc'
        )
        
        # Center text
        canvas.create_text(
            55, 55,
            text=f"{percentage}%",
            font=("Segoe UI", 20, "bold"),
            fill=MODERN_COLORS['text']
        )
        
        ctk.CTkFrame(card, fg_color="transparent", height=20).pack()