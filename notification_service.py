"""
Notification Service - Background Task Reminders
"""

import threading
import time
from datetime import datetime
import customtkinter as ctk
from database import db
from config import COLORS

class NotificationService:
    """Background service to check and display reminders"""
    
    def __init__(self, root):
        self.root = root
        self.running = False
        self.thread = None
        self.user_id = None
        
    def start(self, user_id):
        """Start the notification service"""
        if self.running:
            return
            
        self.user_id = user_id
        self.running = True
        self.thread = threading.Thread(target=self._check_loop, daemon=True)
        self.thread.start()
        print(f"Notification service started for user {user_id}")
        
    def stop(self):
        """Stop the service"""
        self.running = False
        
    def _check_loop(self):
        """Main loop to check for reminders"""
        last_social_check = 0
        
        while self.running:
            try:
                # 1. Check Standard Reminders
                self._check_reminders()
                
                # 2. Check Social Motivation (Every 1 hour)
                current_time = time.time()
                if current_time - last_social_check > 3600: # 3600 seconds = 1 hour
                    db.check_and_generate_social_notification(self.user_id)
                    
                    # Check Streak Risk (Also hourly)
                    risk_alert = db.check_streak_risk(self.user_id)
                    if risk_alert:
                        self.show_notification(risk_alert)
                        
                    last_social_check = current_time
                    
            except Exception as e:
                print(f"Error in notification loop: {e}")
            
            # Check every minute
            for _ in range(60):
                if not self.running:
                    break
                time.sleep(1)
                
    def _check_reminders(self):
        """Check database for pending reminders"""
        if not self.user_id:
            return
            
        reminders = db.get_pending_reminders(self.user_id)
        
        for reminder in reminders:
            # Show notification
            self.root.after(0, lambda r=reminder: self.show_notification(r))
            
            # Save to Notification List (History)
            db.add_notification(self.user_id, 'reminder', reminder['message'], 'high')
            
            # Mark as sent
            db.mark_reminder_sent(reminder['reminder_id'])
            
            # Brief delay to prevent toaster stacking
            time.sleep(2)
            
    def show_notification(self, reminder):
        """Display a custom notification popup and system notification"""
        # 1. System Notification (Always show, even if minimized)
        try:
            from plyer import notification
            notification.notify(
                title="🔔 Study Reminder",
                message=reminder['message'],
                app_name="AI Study Planner",
                timeout=10
            )
        except Exception as e:
            print(f"Notification error: {e}")

        # 2. In-App Popup (Only if window is visible)
        try:
            if self.root.winfo_exists() and self.root.winfo_viewable():
                NotificationPopup(self.root, reminder)
        except Exception:
            pass

class NotificationPopup(ctk.CTkToplevel):
    """Modern notification popup"""
    
    def __init__(self, parent, reminder):
        super().__init__(parent)
        
        self.reminder = reminder
        
        # Window config
        self.title("Reminder")
        self.overrideredirect(True) # No title bar
        self.attributes('-topmost', True)
        self.configure(fg_color=COLORS['card'])
        
        # Position (Bottom Right)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 350
        height = 120
        x = screen_width - width - 20
        y = screen_height - height - 60
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # UI
        self.create_ui()
        
        # Auto close after 10 seconds
        self.after(10000, self.destroy)
        
        # Click to close
        self.bind("<Button-1>", lambda e: self.destroy())
        
    def create_ui(self):
        """Create notification UI"""
        
        # Color strip
        strip = ctk.CTkFrame(self, width=8, fg_color=COLORS['primary'], corner_radius=0)
        strip.pack(side="left", fill="y")
        
        # Content
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        
        # Header
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="🔔 Reminder",
            font=("Arial Bold", 12),
            text_color=COLORS['primary']
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text=datetime.now().strftime("%H:%M"),
            font=("Arial", 10),
            text_color=COLORS['text_light']
        ).pack(side="right")
        
        # Message
        ctk.CTkLabel(
            content,
            text=self.reminder['message'],
            font=("Arial Bold", 14),
            text_color=COLORS['text'],
            wraplength=300,
            justify="left",
            anchor="w"
        ).pack(fill="x", pady=(5, 0))
        
        # Close button (X)
        close_btn = ctk.CTkButton(
            self,
            text="×",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=COLORS['background'],
            text_color=COLORS['text_light'],
            font=("Arial", 20),
            command=self.destroy
        )
        close_btn.place(relx=1.0, rely=0.0, anchor="ne")
