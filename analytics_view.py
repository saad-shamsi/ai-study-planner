"""
Analytics View - Premium Aurora Theme
Beautiful progress tracking and statistics with Custom Graphs
"""

import customtkinter as ctk
from database import db
from datetime import datetime, timedelta
from config import COLORS
import math

class AnalyticsView:
    """Analytics with Premium Aurora Theme"""
    
    def __init__(self, parent, dashboard):
        self.parent = parent
        self.dashboard = dashboard
        self.user_id = dashboard.user['user_id']
        
        self.create_ui()
    
    def create_ui(self):
        """Create analytics interface"""
        
        # Main scrollable frame
        main_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color="transparent"
        )
        main_frame.pack(fill="both", expand=True, padx=35, pady=35)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 30))
        
        # Left: Title
        left_header = ctk.CTkFrame(header, fg_color="transparent")
        left_header.pack(side="left")
        
        ctk.CTkLabel(
            left_header,
            text="📊 Study Analytics",
            font=("Segoe UI Display", 34, "bold"),
            text_color=COLORS['text']
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            left_header,
            text="Track your progress and performance",
            font=("Segoe UI", 15),
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 0))
        
        # Right: Refresh button
        ctk.CTkButton(
            header,
            text="🔄 Refresh Data",
            font=("Segoe UI Bold", 14),
            width=150,
            height=45,
            corner_radius=12,
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            text_color=COLORS['background'],
            command=self.refresh_analytics
        ).pack(side="right")
        
        # Load data
        self.load_analytics_data()
        
        # Overall stats cards
        self.create_overall_stats(main_frame)
        
        # Charts Row
        charts_row = ctk.CTkFrame(main_frame, fg_color="transparent")
        charts_row.pack(fill="x", pady=(0, 25))
        charts_row.grid_columnconfigure(0, weight=1)
        charts_row.grid_columnconfigure(1, weight=1)
        
        # Subject Distribution (Pie Chart)
        self.create_subject_chart(charts_row)
        
        # Daily Activity (Line Chart)
        self.create_activity_chart(charts_row)
        
        # Goals progress
        self.create_goals_section(main_frame)
    
    def load_analytics_data(self):
        """Load analytics data"""
        self.total_time = db.get_total_study_time(self.user_id)
        self.sessions = db.get_user_sessions(self.user_id) or []
        self.subjects = db.get_user_subjects(self.user_id) or []
        self.subject_stats = db.get_subject_wise_time(self.user_id) or []
        self.goals = db.get_user_goals(self.user_id) or []
        
        # Weekly stats
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        self.weekly_sessions = [s for s in self.sessions if s['session_date'] >= week_ago]
        self.weekly_time = sum(s['duration_minutes'] for s in self.weekly_sessions)
    
    def create_overall_stats(self, parent):
        """Create overall statistics cards"""
        stats_container = ctk.CTkFrame(parent, fg_color="transparent")
        stats_container.pack(fill="x", pady=(0, 25))
        
        stats_data = [
            ("⏱️", "Total Study Time", f"{self.total_time // 60}h {self.total_time % 60}m", COLORS['info'], COLORS['background']),
            ("📚", "Total Sessions", str(len(self.sessions)), COLORS['success'], COLORS['background']),
            ("📖", "Active Subjects", str(len(self.subjects)), COLORS['warning'], COLORS['background']),
            ("📅", "This Week", f"{self.weekly_time // 60}h {self.weekly_time % 60}m", COLORS['secondary'], COLORS['background']),
        ]
        
        for i, (icon, label, value, color, text_color) in enumerate(stats_data):
            card = ctk.CTkFrame(
                stats_container,
                fg_color=color, # Using colored cards for emphasis
                corner_radius=20,
                border_width=1,
                border_color=COLORS['border']
            )
            card.grid(row=0, column=i, padx=10, sticky="nsew")
            stats_container.grid_columnconfigure(i, weight=1)
            
            # Icon
            icon_bg = ctk.CTkFrame(
                card,
                fg_color=COLORS['background'], # Dark cutout for icon
                corner_radius=50,
                width=75,
                height=75
            )
            icon_bg.pack(pady=(30, 15))
            icon_bg.pack_propagate(False)
            
            ctk.CTkLabel(
                icon_bg,
                text=icon,
                font=("Segoe UI", 40),
                text_color=color # Icon matches card color
            ).place(relx=0.5, rely=0.5, anchor="center")
            
            # Label
            ctk.CTkLabel(
                card,
                text=label,
                font=("Segoe UI", 13),
                text_color=text_color
            ).pack()
            
            # Value
            ctk.CTkLabel(
                card,
                text=value,
                font=("Segoe UI Display", 30, "bold"),
                text_color=text_color
            ).pack(pady=(8, 30))
    
    def create_subject_chart(self, parent):
        """Create Subject Distribution Pie Chart"""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS['card'], 
            corner_radius=20,
            border_width=1,
            border_color=COLORS['border']
        )
        card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        ctk.CTkLabel(
            card,
            text="📈 Subject Distribution",
            font=("Segoe UI Display", 18, "bold"),
            text_color=COLORS['text']
        ).pack(pady=(20, 10), padx=20, anchor="w")
        
        if not self.subject_stats:
            ctk.CTkLabel(card, text="No data", text_color=COLORS['text_light']).pack(pady=50)
            return
            
        # Canvas for Pie Chart - Use CARD color for background
        canvas_bg = COLORS['card']
        canvas = ctk.CTkCanvas(card, width=300, height=300, bg=canvas_bg, highlightthickness=0)
        canvas.pack(pady=10)
        
        total_minutes = sum(s['total_minutes'] for s in self.subject_stats)
        if total_minutes == 0:
            return
            
        start_angle = 90
        center_x, center_y = 150, 150
        radius = 100
        
        for subject in self.subject_stats:
            minutes = subject['total_minutes']
            if minutes == 0: continue
            
            extent = (minutes / total_minutes) * 360
            color = subject['color_code']
            
            canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=-extent,
                fill=color, outline=canvas_bg, width=2 # Outline matches background to look like gap
            )
            
            start_angle -= extent
            
        # Legend below
        legend_frame = ctk.CTkFrame(card, fg_color="transparent")
        legend_frame.pack(pady=10, padx=20, fill="x")
        
        for subject in self.subject_stats[:4]: # Show top 4
            row = ctk.CTkFrame(legend_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            box = ctk.CTkFrame(row, width=12, height=12, fg_color=subject['color_code'], corner_radius=4)
            box.pack(side="left", padx=(0, 5))
            
            ctk.CTkLabel(row, text=subject['subject_name'], font=("Segoe UI", 11), text_color=COLORS['text']).pack(side="left")
            ctk.CTkLabel(row, text=f"{int(subject['total_minutes']/total_minutes*100)}%", font=("Segoe UI Bold", 11), text_color=COLORS['text_light']).pack(side="right")

    def create_activity_chart(self, parent):
        """Create Daily Activity Line Chart"""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS['card'],
            corner_radius=20,
            border_width=1,
            border_color=COLORS['border']
        )
        card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        
        ctk.CTkLabel(
            card,
            text="📅 Study Trends (Last 7 Days)",
            font=("Segoe UI Display", 18, "bold"),
            text_color=COLORS['text']
        ).pack(pady=(20, 10), padx=20, anchor="w")
        
        daily_stats = db.get_daily_study_stats(self.user_id, days=7) or []
        
        if not daily_stats:
            ctk.CTkLabel(card, text="No data", text_color=COLORS['text_light']).pack(pady=50)
            return

        # Canvas for Line Chart
        canvas_bg = COLORS['card']
        canvas = ctk.CTkCanvas(card, width=400, height=300, bg=canvas_bg, highlightthickness=0)
        canvas.pack(pady=10, padx=20)
        
        # Dimensions
        w, h = 400, 250
        padding = 30
        graph_w = w - 2 * padding
        graph_h = h - 2 * padding
        
        # Axes
        canvas.create_line(padding, h - padding, w - padding, h - padding, fill=COLORS['border'], width=2) # X
        canvas.create_line(padding, h - padding, padding, padding, fill=COLORS['border'], width=2) # Y
        
        # Data points
        max_mins = max((s['total_minutes'] for s in daily_stats), default=60)
        points = []
        
        num_days = len(daily_stats)
        step_x = graph_w / (num_days - 1) if num_days > 1 else graph_w
        
        for i, stat in enumerate(daily_stats):
            x = padding + i * step_x
            y = (h - padding) - (stat['total_minutes'] / max_mins) * graph_h
            points.append((x, y))
            
            # Draw point
            canvas.create_oval(x-4, y-4, x+4, y+4, fill=COLORS['primary'], outline=canvas_bg, width=2)
            
            # Draw label (Day)
            canvas.create_text(x, h - padding + 15, text=stat['session_date'].strftime("%a"), font=("Segoe UI", 9), fill=COLORS['text_light'])
            
        # Draw line
        if len(points) > 1:
            canvas.create_line(points, fill=COLORS['primary'], width=3, smooth=True)

    def create_goals_section(self, parent):
        """Create goals overview"""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS['card'],
            corner_radius=20,
            border_width=1,
            border_color=COLORS['border']
        )
        card.pack(fill="x", pady=(0, 25))
        
        # Header
        ctk.CTkLabel(
            card,
            text="🎯 Goals Overview",
            font=("Segoe UI Display", 22, "bold"),
            text_color=COLORS['text']
        ).pack(pady=(30, 25), padx=30, anchor="w")
        
        if not self.goals:
            ctk.CTkLabel(card, text="No goals set yet", font=("Segoe UI", 14), text_color=COLORS['text_light']).pack(pady=30)
            return
        
        # Goals stats
        completed = len([g for g in self.goals if g['status'] == 'completed'])
        in_progress = len([g for g in self.goals if g['status'] == 'in_progress'])
        pending = len([g for g in self.goals if g['status'] == 'pending'])
        
        stats_grid = ctk.CTkFrame(card, fg_color="transparent")
        stats_grid.pack(fill="x", padx=30, pady=(0, 30))
        
        goal_stats = [
            ("✅", "Completed", completed, COLORS['success']),
            ("🔄", "In Progress", in_progress, COLORS['warning']),
            ("⏳", "Pending", pending, COLORS['text_light']),
            ("📊", "Total Goals", len(self.goals), COLORS['primary'])
        ]
        
        for i, (icon, label, value, color) in enumerate(goal_stats):
            stat_card = ctk.CTkFrame(
                stats_grid,
                fg_color=COLORS['background'],
                corner_radius=15,
                border_width=1,
                border_color=COLORS['border']
            )
            stat_card.grid(row=0, column=i, padx=8, sticky="nsew")
            stats_grid.grid_columnconfigure(i, weight=1)
            
            ctk.CTkLabel(stat_card, text=icon, font=("Segoe UI", 30)).pack(pady=(15, 5))
            ctk.CTkLabel(stat_card, text=label, font=("Segoe UI", 12), text_color=COLORS['text_light']).pack()
            ctk.CTkLabel(stat_card, text=str(value), font=("Segoe UI Display", 24, "bold"), text_color=COLORS['text']).pack(pady=(5, 15))

    def refresh_analytics(self):
        """Refresh analytics"""
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.__init__(self.parent, self.dashboard)