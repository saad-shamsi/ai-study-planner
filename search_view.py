"""
Search View - Global Search Results
"""

import customtkinter as ctk
from config import COLORS
from database import db

class SearchView:
    """Displays search results from Global Search"""
    
    def __init__(self, parent, dashboard, search_term):
        self.parent = parent
        self.dashboard = dashboard
        self.search_term = search_term
        self.user_id = dashboard.user['user_id']
        
        self.create_ui()
        self.perform_search()
        
    def create_ui(self):
        """Create search results UI"""
        
        # Main container
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=35, pady=35)
        
        # Header
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        
        ctk.CTkLabel(
            header,
            text=f"🔍 Search Results for '{self.search_term}'",
            font=("Arial Black", 24),
            text_color=COLORS['text']
        ).pack(side="left")
        
        # Results container (Scrollable)
        self.results_scroll = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.results_scroll.pack(fill="both", expand=True)
        
    def perform_search(self):
        """Execute search and display results"""
        results = db.search_everything(self.user_id, self.search_term)
        
        # 1. Subjects
        if results.get('subjects'):
            self.create_section_header("📚 Subjects")
            for sub in results['subjects']:
                self.create_result_card(
                    f"{sub['subject_name']} ({sub['subject_code']})",
                    "Subject",
                    lambda s=sub: self.dashboard.show_subjects() # Navigate to subjects
                )
        
        # 2. Notes
        if results.get('notes'):
            self.create_section_header("📝 Notes")
            for note in results['notes']:
                self.create_result_card(
                    note['note_title'],
                    f"Note: {note['note_content'][:50]}...",
                    None # TODO: Open note details
                )
                
        # 3. Chat History
        if results.get('chat'):
            self.create_section_header("💬 Chat History")
            for chat in results['chat']:
                self.create_result_card(
                    "AI Conversation",
                    f"You: {chat['message'][:50]}...\nAI: {chat['response'][:50]}...",
                    lambda: self.dashboard.show_chatbot()
                )
                
        # No results
        if not any(results.values()):
            ctk.CTkLabel(
                self.results_scroll,
                text="No results found.",
                font=("Arial", 16),
                text_color=COLORS['text_light']
            ).pack(pady=50)

    def create_section_header(self, title):
        """Create section header"""
        ctk.CTkLabel(
            self.results_scroll,
            text=title,
            font=("Arial Bold", 18),
            text_color=COLORS['primary'],
            anchor="w"
        ).pack(fill="x", pady=(20, 10))
        
    def create_result_card(self, title, subtitle, command):
        """Create a result card"""
        card = ctk.CTkButton(
            self.results_scroll,
            text="",
            fg_color="white",
            hover_color=COLORS['hover'],
            height=80,
            corner_radius=15,
            command=command if command else lambda: None
        )
        card.pack(fill="x", pady=5)
        
        # Content frame inside button (to allow custom layout)
        # Note: CTkButton doesn't support complex inner layout easily, 
        # so we just use the button itself as the container if possible, 
        # or place labels on top (but that blocks clicks).
        # Simpler approach: Use a Frame and bind click events.
        
        card.destroy() # Re-doing as Frame
        
        card = ctk.CTkFrame(
            self.results_scroll,
            fg_color="white",
            corner_radius=15,
            height=80
        )
        card.pack(fill="x", pady=5)
        card.pack_propagate(False)
        
        # Title
        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial Bold", 15),
            text_color=COLORS['text']
        ).place(x=20, y=15)
        
        # Subtitle
        ctk.CTkLabel(
            card,
            text=subtitle,
            font=("Arial", 13),
            text_color=COLORS['text_light']
        ).place(x=20, y=45)
        
        # Bind click
        if command:
            card.bind("<Button-1>", lambda e: command())
            for child in card.winfo_children():
                child.bind("<Button-1>", lambda e: command())
