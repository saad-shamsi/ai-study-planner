import customtkinter as ctk
from config import COLORS
from database import db
from datetime import datetime

class NotificationView:
    def __init__(self, parent, dashboard):
        self.parent = parent
        self.dashboard = dashboard
        self.user_id = dashboard.user['user_id']
        
        # Main container with scrolling
        self.container = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            corner_radius=0
        )
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header()
        
        # List
        self.load_notifications()
        
    def create_header(self):
        header_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="Notifications",
            font=("Segoe UI Display", 28, "bold"),
            text_color=COLORS['text']
        ).pack(side="left")
        
        # Refresh Button
        ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            width=100,
            fg_color=COLORS['card'],
            hover_color=COLORS['hover'],
            text_color=COLORS['text'],
            command=self.load_notifications
        ).pack(side="right")
        
        # Test Button (Debug)
        ctk.CTkButton(
            header_frame,
            text="🔔 Test",
            width=80,
            fg_color=COLORS['secondary'],
            hover_color=COLORS['primary'],
            text_color=COLORS['background'],
            command=self.send_test_notification
        ).pack(side="right", padx=10)

    def load_notifications(self):
        # Clear existing content frame if exists, else create new
        if hasattr(self, 'content_frame'):
            self.content_frame.destroy()
            
        self.content_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.content_frame.pack(fill="x", expand=True)

        # Get data
        notifications = db.get_notifications(self.user_id, limit=50) # Fetch all recent
        
        if not notifications:
            self.show_empty_state()
            return
            
        for notif in notifications:
            self.create_notification_card(notif)
            
    def show_empty_state(self):
        frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        frame.pack(pady=50, fill="x")
        
        ctk.CTkLabel(
            frame,
            text="🔕",
            font=("Segoe UI", 48)
        ).pack()
        
        ctk.CTkLabel(
            frame,
            text="No notifications found",
            font=("Segoe UI", 16),
            text_color=COLORS['text_light']
        ).pack(pady=10)

    def create_notification_card(self, notif):
        """Create a Facebook-style notification card"""
        is_read = notif.get('is_read', 0)
        
        # Style: Unread = Highlighted Card, Read = Transparent/Dimmed
        if not is_read:
            bg_color = COLORS['card']
            border_color = COLORS['primary']
            border_width = 1
            text_color = COLORS['text']
        else:
            bg_color = "transparent"
            border_color = COLORS['border']
            border_width = 0
            text_color = COLORS['text_light']
            
        card = ctk.CTkFrame(
            self.content_frame,
            fg_color=bg_color,
            corner_radius=10,
            border_width=border_width,
            border_color=border_color
        )
        card.pack(fill="x", pady=2, padx=5)
        
        # Inner layout
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 1. Indicator Dot (Left) - Only if unread
        if not is_read:
            dot = ctk.CTkLabel(inner, text="●", font=("Arial", 16), text_color=COLORS['secondary'])
            dot.pack(side="left", padx=(0, 8))
        else:
            # Spacer for alignment
            ctk.CTkFrame(inner, width=20, height=1, fg_color="transparent").pack(side="left")
        
        # 2. Content (Middle)
        msg_frame = ctk.CTkFrame(inner, fg_color="transparent")
        msg_frame.pack(side="left", fill="both", expand=True)
        
        # Message Text
        font_style = ("Segoe UI", 13, "bold") if not is_read else ("Segoe UI", 13)
        
        ctk.CTkLabel(
            msg_frame,
            text=notif.get('message', ''),
            font=font_style,
            text_color=text_color,
            wraplength=450,
            justify="left",
            anchor="w"
        ).pack(fill="x")
        
        # Time
        time_str = str(notif.get('created_at'))
        ctk.CTkLabel(
            msg_frame,
            text=time_str,
            font=("Segoe UI", 11),
            text_color=COLORS['text_light'],
            anchor="w"
        ).pack(fill="x")

        # 3. Actions (Right)
        actions = ctk.CTkFrame(inner, fg_color="transparent")
        actions.pack(side="right", padx=(5, 0))
        
        # Mark Read (Circle Check)
        if not is_read:
            ctk.CTkButton(
                actions,
                text="✔",
                width=28,
                height=28,
                corner_radius=14,
                fg_color=COLORS['background'],
                hover_color=COLORS['success'],
                text_color=COLORS['success'],
                font=("Arial", 12, "bold"),
                command=lambda: self.mark_read(notif['notification_id'])
            ).pack(side="left", padx=2)
            
        # Delete (Trash)
        ctk.CTkButton(
            actions,
            text="✕",
            width=28,
            height=28,
            corner_radius=14,
            fg_color="transparent",
            hover_color=COLORS['warning'],
            text_color=COLORS['text_light'],
            font=("Arial", 12, "bold"),
            command=lambda: self.delete_notif(notif['notification_id'])
        ).pack(side="left", padx=2)

    def mark_read(self, notification_id):
        db.mark_notification_read(notification_id)
        self.load_notifications()
        # Optionally update dashboard badge
        if hasattr(self.dashboard, 'update_notification_badge'):
            self.dashboard.update_notification_badge()
        
    def delete_notif(self, notification_id):
        db.delete_notification(notification_id)
        self.load_notifications()
        # Optionally update dashboard badge
        if hasattr(self.dashboard, 'update_notification_badge'):
            self.dashboard.update_notification_badge()

    def send_test_notification(self):
        """Send a test notification to verify system"""
        db.add_notification(
            self.user_id, 
            'system', 
            f"Test Notification at {datetime.now().strftime('%I:%M %p')} 🔔", 
            'medium'
        )
        self.load_notifications()
        # Update badge
        if hasattr(self.dashboard, 'update_notification_badge'):
            self.dashboard.update_notification_badge()
