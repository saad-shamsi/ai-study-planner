"""
Mood Tracker Widget - Daily Mood Selection
Track how you're feeling each day
"""

import customtkinter as ctk
from tkinter import messagebox
from database import db
from config import COLORS


class MoodTracker(ctk.CTkFrame):
    """Daily mood tracker widget"""
    
    def __init__(self, parent, user_id):
        super().__init__(parent, fg_color=COLORS['card'], corner_radius=20)
        
        self.user_id = user_id
        
        self.moods = {
            'happy': ('😊', 'Happy', COLORS['success']),
            'okay': ('😐', 'Okay', COLORS['info']),
            'tired': ('😴', 'Tired', COLORS['text_light']),
            'stressed': ('😫', 'Stressed', COLORS['warning']),
            'motivated': ('🤩', 'Motivated', COLORS['secondary'])
        }
        
        self.selected_mood = None
        
        self.create_ui()
        self.load_today_mood()
    
    def create_ui(self):
        """Create mood tracker UI"""
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(25, 15))
        
        ctk.CTkLabel(
            header,
            text="💭 How are you feeling today?",
            font=("Arial Black", 18),
            text_color=COLORS['text']
        ).pack(anchor="w")
        
        # Mood buttons grid
        mood_grid = ctk.CTkFrame(self, fg_color="transparent")
        mood_grid.pack(fill="x", padx=25, pady=10)
        
        self.mood_buttons = {}
        col = 0
        
        for mood_key, (emoji, label, color) in self.moods.items():
            btn_frame = ctk.CTkFrame(mood_grid, fg_color="transparent")
            btn_frame.grid(row=0, column=col, padx=5, pady=5)
            
            btn = ctk.CTkButton(
                btn_frame,
                text=emoji,
                font=("Arial", 40),
                width=70,
                height=70,
                corner_radius=35,
                fg_color=COLORS['background'],
                hover_color=color,
                border_width=3,
                border_color=COLORS['border'],
                command=lambda m=mood_key: self.select_mood(m)
            )
            btn.pack()
            
            ctk.CTkLabel(
                btn_frame,
                text=label,
                font=("Arial", 10),
                text_color=COLORS['text_light']
            ).pack(pady=(5, 0))
            
            self.mood_buttons[mood_key] = btn
            col += 1
        
        # Status message
        self.status_label = ctk.CTkLabel(
            self,
            text="Select your mood",
            font=("Arial", 12),
            text_color=COLORS['text_light']
        )
        self.status_label.pack(pady=(10, 20))
    
    def load_today_mood(self):
        """Load today's mood if exists"""
        today_mood = db.get_today_mood(self.user_id)
        
        if today_mood:
            mood_type = today_mood['mood_type']
            self.selected_mood = mood_type
            
            # Highlight selected mood
            emoji, label, color = self.moods[mood_type]
            self.mood_buttons[mood_type].configure(
                fg_color=color,
                border_color=color
            )
            
            self.status_label.configure(
                text=f"You're feeling {label.lower()} today!",
                text_color=color
            )
    
    def select_mood(self, mood_key):
        """Select a mood"""
        # Reset all buttons
        for key, btn in self.mood_buttons.items():
            btn.configure(
                fg_color=COLORS['background'],
                border_color=COLORS['border']
            )
        
        # Highlight selected
        emoji, label, color = self.moods[mood_key]
        self.mood_buttons[mood_key].configure(
            fg_color=color,
            border_color=color
        )
        
        self.selected_mood = mood_key
        
        # Save to database
        result = db.add_mood(self.user_id, mood_key)
        
        if result:
            self.status_label.configure(
                text=f"Mood logged: {label}! ✨",
                text_color=color
            )
        else:
            self.status_label.configure(
                text="Failed to save mood",
                text_color=COLORS['warning']
            )