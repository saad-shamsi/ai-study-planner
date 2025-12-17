"""
Study Pet Widget - Virtual Companion
Animated pet that reacts to user's study activity
"""

import customtkinter as ctk
from database import db
from config import COLORS
import random


class StudyPet(ctk.CTkFrame):
    """Animated study pet widget"""
    
    def __init__(self, parent, user_id):
        super().__init__(parent, fg_color=COLORS['card'], corner_radius=20)
        
        self.user_id = user_id
        self.pet_data = db.get_or_create_pet(user_id)
        
        self.pet_states = {
            'happy': '😊',
            'excited': '🤩',
            'sleeping': '😴',
            'clapping': '👏',
            'studying': '📚',
            'confused': '🤔',
            'proud': '😎'
        }
        
        self.current_state = 'happy'
        self.animation_running = False
        
        self.create_ui()
        self.update_pet_mood()
    
    def create_ui(self):
        """Create pet widget UI"""
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            header,
            text="🐾 Your Study Pet",
            font=("Arial Black", 16),
            text_color=COLORS['text']
        ).pack(side="left")
        
        # Pet name
        ctk.CTkLabel(
            header,
            text=self.pet_data['pet_name'],
            font=("Arial Bold", 12),
            text_color=COLORS['text_light']
        ).pack(side="right")
        
        # Pet display
        self.pet_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS['background'],
            corner_radius=15,
            height=150
        )
        self.pet_frame.pack(fill="x", padx=20, pady=10)
        self.pet_frame.pack_propagate(False)
        
        # Pet emoji (animated)
        self.pet_label = ctk.CTkLabel(
            self.pet_frame,
            text=self.pet_states[self.current_state],
            font=("Arial", 80)
        )
        self.pet_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Status message
        self.status_label = ctk.CTkLabel(
            self.pet_frame,
            text="Ready to study!",
            font=("Arial", 11),
            text_color=COLORS['text_light']
        )
        self.status_label.place(relx=0.5, rely=0.85, anchor="center")
        
        # Stats bars
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        # Happiness bar
        happy_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        happy_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            happy_frame,
            text="😊",
            font=("Arial", 16)
        ).pack(side="left", padx=(0, 8))
        
        self.happiness_bar = ctk.CTkProgressBar(
            happy_frame,
            height=12,
            corner_radius=6,
            progress_color=COLORS['success']
        )
        self.happiness_bar.pack(side="left", fill="x", expand=True)
        self.happiness_bar.set(self.pet_data['happiness_level'] / 100)
        
        ctk.CTkLabel(
            happy_frame,
            text=f"{self.pet_data['happiness_level']}%",
            font=("Arial Bold", 11),
            text_color=COLORS['text']
        ).pack(side="right", padx=(8, 0))
        
        # Energy bar
        energy_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        energy_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            energy_frame,
            text="⚡",
            font=("Arial", 16)
        ).pack(side="left", padx=(0, 8))
        
        self.energy_bar = ctk.CTkProgressBar(
            energy_frame,
            height=12,
            corner_radius=6,
            progress_color=COLORS['warning']
        )
        self.energy_bar.pack(side="left", fill="x", expand=True)
        self.energy_bar.set(self.pet_data['energy_level'] / 100)
        
        ctk.CTkLabel(
            energy_frame,
            text=f"{self.pet_data['energy_level']}%",
            font=("Arial Bold", 11),
            text_color=COLORS['text']
        ).pack(side="right", padx=(8, 0))
        
        # Interaction buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            btn_frame,
            text="🍪 Feed",
            font=("Arial Bold", 11),
            width=80,
            height=35,
            corner_radius=10,
            fg_color=COLORS['warning'],
            hover_color=COLORS['warning'],
            command=self.feed_pet
        ).pack(side="left", padx=3)
        
        ctk.CTkButton(
            btn_frame,
            text="🎾 Play",
            font=("Arial Bold", 11),
            width=80,
            height=35,
            corner_radius=10,
            fg_color=COLORS['info'],
            hover_color=COLORS['info'],
            command=self.play_with_pet
        ).pack(side="left", padx=3)
        
        ctk.CTkButton(
            btn_frame,
            text="😴 Rest",
            font=("Arial Bold", 11),
            width=80,
            height=35,
            corner_radius=10,
            fg_color=COLORS['secondary'],
            hover_color=COLORS['secondary'],
            command=self.rest_pet
        ).pack(side="left", padx=3)
    
    def update_pet_mood(self):
        """Update pet mood based on stats"""
        happiness = self.pet_data['happiness_level']
        
        if happiness >= 80:
            self.change_state('excited', "I'm so happy! 🎉")
        elif happiness >= 60:
            self.change_state('happy', "Feeling great!")
        elif happiness >= 40:
            self.change_state('confused', "Could use some fun...")
        elif happiness >= 20:
            self.change_state('sleeping', "Feeling sleepy...")
        else:
            self.change_state('sleeping', "Need rest...")
    
    def change_state(self, state, message):
        """Change pet state with animation"""
        self.current_state = state
        self.pet_label.configure(text=self.pet_states[state])
        self.status_label.configure(text=message)
        
        # Bounce animation
        self.animate_bounce()
    
    def animate_bounce(self):
        """Smoother bounce animation (Higher FPS)"""
        # Smoother steps array
        sizes = [80, 85, 90, 95, 90, 85, 80]
        
        def step(index):
            if index < len(sizes):
                self.pet_label.configure(font=("Arial", sizes[index]))
                # Reduced delay from 50ms to 20ms for smoother look
                self.after(20, lambda: step(index + 1))
        
        step(0)
    
    def feed_pet(self):
        """Feed the pet"""
        db.update_pet_status(self.user_id, happiness_change=10, energy_change=5)
        self.refresh_pet()
        self.change_state('excited', "Yummy! Thanks! 🍪")
    
    def play_with_pet(self):
        """Play with pet"""
        db.update_pet_status(self.user_id, happiness_change=15, energy_change=-10)
        self.refresh_pet()
        self.change_state('excited', "That was fun! 🎾")
    
    def rest_pet(self):
        """Let pet rest"""
        db.update_pet_status(self.user_id, energy_change=20)
        self.refresh_pet()
        self.change_state('sleeping', "Zzz... 😴")
    
    def celebrate_task(self):
        """Pet celebrates task completion"""
        db.update_pet_status(self.user_id, happiness_change=20, claps=1)
        self.refresh_pet()
        self.change_state('clapping', "Well done! 👏")
        
        # Auto return to happy after 3 seconds
        self.after(3000, lambda: self.change_state('happy', "Ready for more!"))
    
    def start_study(self):
        """Pet enters study mode"""
        self.change_state('studying', "Let's focus! 📚")
    
    def refresh_pet(self):
        """Refresh pet data from database"""
        self.pet_data = db.get_or_create_pet(self.user_id)
        self.happiness_bar.set(self.pet_data['happiness_level'] / 100)
        self.energy_bar.set(self.pet_data['energy_level'] / 100)
        self.update_pet_mood()