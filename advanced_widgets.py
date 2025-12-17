"""
Advanced Widgets Collection
Streak Garden, Pomodoro Timer, Quick Actions, Motivation, Notifications
"""

import customtkinter as ctk
from tkinter import messagebox
from database import db
from config import COLORS
from datetime import datetime, timedelta
import time
import threading
from saved_plans_view import SavedPlansView

# ==================== STREAK GARDEN ====================

class StreakGarden(ctk.CTkFrame):
    """Visual streak tracker with flower garden"""
    
    def __init__(self, parent, user_id):
        super().__init__(parent, fg_color=COLORS['card'], corner_radius=20)
        
        self.user_id = user_id
        self.create_ui()
    
    def create_ui(self):
        """Create garden UI"""
        
        # Header
        ctk.CTkLabel(
            self,
            text="🌱 Study Streak Garden",
            font=("Arial Black", 18),
            text_color=COLORS['text']
        ).pack(pady=(25, 15), padx=25, anchor="w")
        
        # Current streak
        streak_days = db.get_current_streak(self.user_id)
        
        streak_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS['success'],
            corner_radius=15
        )
        streak_frame.pack(fill="x", padx=25, pady=(0, 15))
        
        ctk.CTkLabel(
            streak_frame,
            text=f"🔥 {streak_days} Day Streak!",
            font=("Arial Black", 24),
            text_color="white"
        ).pack(pady=15)
        
        # Garden visualization (last 7 days)
        garden_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS['background'],
            corner_radius=15
        )
        garden_frame.pack(fill="x", padx=25, pady=(0, 20))
        
        garden_data = db.get_streak_garden(self.user_id, days=7)
        
        # Days grid
        days_container = ctk.CTkFrame(garden_frame, fg_color="transparent")
        days_container.pack(padx=15, pady=15)
        
        for i in range(7):
            day_col = ctk.CTkFrame(days_container, fg_color="transparent")
            day_col.pack(side="left", padx=8)
            
            # Check if studied
            studied = False
            if i < len(garden_data):
                studied = garden_data[i]['studied']
            
            # Flower emoji
            flower = "🌸" if studied else "🥀"
            
            ctk.CTkLabel(
                day_col,
                text=flower,
                font=("Arial", 35)
            ).pack()
            
            # Day label
            date_obj = datetime.now().date() - timedelta(days=6-i)
            day_name = date_obj.strftime("%a")
            
            ctk.CTkLabel(
                day_col,
                text=day_name,
                font=("Arial", 10),
                text_color=COLORS['text_light']
            ).pack()


# ==================== POMODORO TIMER ====================

class PomodoroTimer(ctk.CTkFrame):
    """Pomodoro focus timer"""
    
    def __init__(self, parent, user_id):
        super().__init__(parent, fg_color=COLORS['card'], corner_radius=20)
        
        self.user_id = user_id
        self.is_running = False
        self.time_left = 25 * 60  # 25 minutes
        self.timer_thread = None
        self.completed_cycles = 0
        
        self.create_ui()
    
    def create_ui(self):
        """Create timer UI"""
        
        # Header
        ctk.CTkLabel(
            self,
            text="⏱️ Pomodoro Timer",
            font=("Arial Black", 18),
            text_color=COLORS['text']
        ).pack(pady=(25, 15), padx=25, anchor="w")
        
        # Timer display
        timer_bg = ctk.CTkFrame(
            self,
            fg_color=COLORS['primary'],
            corner_radius=100,
            width=200,
            height=200
        )
        timer_bg.pack(pady=20)
        timer_bg.pack_propagate(False)
        
        self.timer_label = ctk.CTkLabel(
            timer_bg,
            text="25:00",
            font=("Arial Black", 48),
            text_color="white"
        )
        self.timer_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Status
        self.status_label = ctk.CTkLabel(
            self,
            text="Focus Time",
            font=("Arial Bold", 14),
            text_color=COLORS['text']
        )
        self.status_label.pack(pady=(10, 20))
        
        # Controls
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(padx=25, pady=(0, 20))
        
        self.start_btn = ctk.CTkButton(
            btn_frame,
            text="▶️ Start",
            font=("Arial Bold", 14),
            width=100,
            height=45,
            corner_radius=12,
            fg_color=COLORS['success'],
            hover_color=COLORS['success'],
            command=self.start_timer
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ctk.CTkButton(
            btn_frame,
            text="⏸️ Pause",
            font=("Arial Bold", 14),
            width=100,
            height=45,
            corner_radius=12,
            fg_color=COLORS['warning'],
            hover_color=COLORS['warning'],
            command=self.stop_timer,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=5)
        
        self.reset_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Reset",
            font=("Arial Bold", 14),
            width=100,
            height=45,
            corner_radius=12,
            fg_color=COLORS['text_light'],
            hover_color=COLORS['text_light'],
            command=self.reset_timer
        )
        self.reset_btn.pack(side="left", padx=5)
        
        # Cycles completed
        self.cycles_label = ctk.CTkLabel(
            self,
            text=f"Completed: {self.completed_cycles} cycles",
            font=("Arial", 12),
            text_color=COLORS['text_light']
        )
        self.cycles_label.pack(pady=(0, 20))
    
    def start_timer(self):
        """Start the timer"""
        if not self.is_running:
            self.is_running = True
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.status_label.configure(text="⏳ Focusing...")
            
            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()
    
    def stop_timer(self):
        """Pause the timer"""
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="⏸️ Paused")
    
    def reset_timer(self):
        """Reset timer"""
        self.is_running = False
        self.time_left = 25 * 60
        self.update_display()
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="Focus Time")
    
    def run_timer(self):
        """Timer countdown logic"""
        while self.time_left > 0 and self.is_running:
            time.sleep(1)
            self.time_left -= 1
            self.after(0, self.update_display)
        
        if self.time_left == 0:
            self.after(0, self.timer_completed)
    
    def update_display(self):
        """Update timer display"""
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
    
    def timer_completed(self):
        """Handle timer completion"""
        self.completed_cycles += 1
        self.cycles_label.configure(text=f"Completed: {self.completed_cycles} cycles")
        
        # Save to database
        db.add_pomodoro_session(self.user_id, None, 1, 25)
        
        # Reset for break (5 minutes)
        self.time_left = 5 * 60
        self.status_label.configure(text="☕ Break Time!")
        
        messagebox.showinfo(
            "Pomodoro Complete!",
            "Great work! Take a 5-minute break! ☕",
            parent=self
        )
        
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")


# ==================== QUICK ACTIONS ====================

class QuickActions(ctk.CTkFrame):
    """Floating quick action buttons"""
    
    def __init__(self, parent, dashboard):
        super().__init__(parent, fg_color=COLORS['card'], corner_radius=20)
        
        self.dashboard = dashboard
        self.create_ui()
    
    def create_ui(self):
        """Create quick actions UI"""
        
        ctk.CTkLabel(
            self,
            text="⚡ Quick Actions",
            font=("Arial Black", 18),
            text_color=COLORS['text']
        ).pack(pady=(25, 15), padx=25, anchor="w")
        
        actions = [
            ("➕ Add Subject", COLORS['info'], "subjects"),
            ("📝 New Session", COLORS['success'], "planner"),
            ("📋 Add Note", COLORS['warning'], self.add_note),
            ("💬 Ask AI", COLORS['secondary'], "chatbot"),
            ("💾 Saved Plans", COLORS['primary'], self.show_saved_plans), # NEW ACTION
        ]
        
        for text, color, action in actions:
            btn = ctk.CTkButton(
                self,
                text=text,
                font=("Arial Bold", 14),
                height=50,
                corner_radius=12,
                fg_color=color,
                hover_color=color,
                text_color="white",
                command=lambda a=action: self.handle_action(a)
            )
            btn.pack(fill="x", padx=25, pady=5)
        
        ctk.CTkFrame(self, fg_color="transparent", height=15).pack()
    
    def handle_action(self, action):
        """Handle quick action"""
        if callable(action):
            action()
        else:
            self.dashboard.navigate_to(action)

    def show_saved_plans(self):
        """Show saved plans window"""
        SavedPlansView(self.winfo_toplevel(), self.dashboard)
    
    def add_note(self):
        """Quick add note dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Quick Note")
        dialog.geometry("450x350")
        dialog.configure(fg_color=COLORS['background'])
        dialog.grab_set()
        
        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 225
        y = (dialog.winfo_screenheight() // 2) - 175
        dialog.geometry(f'450x350+{x}+{y}')
        
        content = ctk.CTkFrame(dialog, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(
            content,
            text="📋 Quick Note",
            font=("Arial Black", 22),
            text_color=COLORS['text']
        ).pack(pady=(0, 20))
        
        ctk.CTkLabel(
            content,
            text="Title",
            font=("Arial Bold", 12),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        title_entry = ctk.CTkEntry(
            content,
            placeholder_text="Note title",
            height=45,
            font=("Arial", 13)
        )
        title_entry.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            content,
            text="Content",
            font=("Arial Bold", 12),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        content_text = ctk.CTkTextbox(
            content,
            height=100,
            font=("Arial", 13)
        )
        content_text.pack(fill="both", expand=True, pady=(0, 20))
        
        def save_note():
            title = title_entry.get().strip()
            note_content = content_text.get("1.0", "end").strip()
            
            if title and note_content:
                db.add_note(self.dashboard.user['user_id'], title, note_content)
                messagebox.showinfo("Success", "Note saved!", parent=dialog)
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Please fill all fields!", parent=dialog)
        
        ctk.CTkButton(
            content,
            text="Save Note",
            height=45,
            font=("Arial Bold", 14),
            fg_color=COLORS['warning'],
            hover_color=COLORS['warning'],
            command=save_note
        ).pack(fill="x")


# ==================== MOTIVATION WIDGET ====================

class MotivationWidget(ctk.CTkFrame):
    """Daily motivation quote"""
    
    def __init__(self, parent, user_id):
        super().__init__(parent, fg_color=COLORS['primary'], corner_radius=20)
        
        self.user_id = user_id
        self.create_ui()
    
    def create_ui(self):
        """Create motivation UI"""
        
        ctk.CTkLabel(
            self,
            text="💡",
            font=("Arial", 50)
        ).pack(pady=(25, 10))
        
        ctk.CTkLabel(
            self,
            text="Daily Motivation",
            font=("Arial Black", 16),
            text_color="white"
        ).pack()
        
        # Get random quote
        quote = db.get_random_quote()
        
        if quote:
            ctk.CTkLabel(
                self,
                text=f'"{quote["quote_text"]}"',
                font=("Arial", 13),
                text_color="white",
                wraplength=280,
                justify="center"
            ).pack(pady=(15, 10), padx=20)
            
            ctk.CTkLabel(
                self,
                text=f"— {quote['author']}",
                font=("Arial Italic", 11),
                text_color="white"
            ).pack(pady=(0, 25))
        else:
            ctk.CTkLabel(
                self,
                text="Keep going!\nYou're doing great!",
                font=("Arial", 14),
                text_color="white",
                justify="center"
            ).pack(pady=(15, 25), padx=20)


# ==================== NOTIFICATIONS PANEL ====================

class NotificationsPanel(ctk.CTkFrame):
    """Smart notifications display"""
    
    def __init__(self, parent, user_id):
        super().__init__(parent, fg_color=COLORS['card'], corner_radius=20)
        
        self.user_id = user_id
        self.create_ui()
    
    def create_ui(self):
        """Create notifications UI"""
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(25, 15))
        
        ctk.CTkLabel(
            header,
            text="🔔 Notifications",
            font=("Arial Black", 18),
            text_color=COLORS['text']
        ).pack(side="left")
        
        # Get notifications
        notifications = db.get_notifications(self.user_id)
        
        if not notifications:
            ctk.CTkLabel(
                self,
                text="✅ All caught up!\nNo new notifications",
                font=("Arial", 13),
                text_color=COLORS['text_light'],
                justify="center"
            ).pack(pady=40)
        else:
            for notif in notifications[:5]:
                self.create_notification_item(notif)
        
        ctk.CTkFrame(self, fg_color="transparent", height=15).pack()
    
    def create_notification_item(self, notif):
        """Create notification item"""
        item = ctk.CTkFrame(
            self,
            fg_color=COLORS['background'],
            corner_radius=12
        )
        item.pack(fill="x", padx=25, pady=5)
        
        content = ctk.CTkFrame(item, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=12)
        
        # Icon based on type
        icon = "📌" if notif['priority'] == 'high' else "💬"
        
        ctk.CTkLabel(
            content,
            text=icon,
            font=("Arial", 20)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            content,
            text=notif['message'],
            font=("Arial", 12),
            text_color=COLORS['text'],
            wraplength=200,
            justify="left"
        ).pack(side="left", fill="x", expand=True)