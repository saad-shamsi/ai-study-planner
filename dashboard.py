"""
Complete Professional Dashboard - Modern Theme (Design Only Updated)
Beautiful color scheme and fonts - Same functionality
"""
import sys 
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from database import db
from config import COLORS
from enhanced_home_aesthetic import EnhancedHomeView
from home_view_modren import ModernHomeView
from notification_service import NotificationService
# New Imports for Notification System
from notification_view import NotificationView
import pystray
from PIL import Image
import threading
import os

# Premium Aurora Theme (Dark Mode)
MODERN_COLORS = {
    'background': "#0F172A",      # Deep Midnight Slate
    'sidebar': "#1E293B",         # Lighter Slate
    'card': "#1E293B",            # Matching Sidebar
    'primary': '#38BDF8',         # Aurora Cyan
    'secondary': '#818CF8',       # Aurora Purple
    'success': '#34D399',         # Aurora Green
    'warning': '#fbbf24',         # Warm Amber
    'info': '#60A5FA',            # Soft Blue
    'text': '#F8FAFC',            # Off-white
    'text_light': '#94A3B8',      # Slate Gray
    'hover': '#334155',           # Hover State
    'border': '#334155'           # Subtle Border
}


class Dashboard(ctk.CTkToplevel):
    """Professional dashboard with modern design"""
    
    def __init__(self, user, parent):
        super().__init__(parent)
        
        self.user = user
        self.parent = parent
        self.current_page = "home"
        
        # Set Dark mode
        ctk.set_appearance_mode("Dark")
        
        # Window configuration
        self.title(f"AI Study Planner - {user['full_name']}")
        self.geometry("1400x850")
        self.state('zoomed')
        self.configure(fg_color=MODERN_COLORS['background'])
        
        # Handle close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Load data
        self.load_user_data()
        
        # Create UI
        self.create_ui()
        
        # Show home
        self.show_home()

        # Start Notification Service
        self.notification_service = NotificationService(self)
        self.notification_service.start(self.user['user_id'])
    
    def load_user_data(self):
        """Load user data"""
        self.subjects = db.get_user_subjects(self.user['user_id']) or []
        self.sessions = db.get_user_sessions(self.user['user_id'], limit=10) or []
        self.goals = db.get_user_goals(self.user['user_id']) or []
        self.total_study_time = db.get_total_study_time(self.user['user_id'])
    
    def create_ui(self):
        """Create dashboard UI"""
        
        # Main layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # ============ SIDEBAR ============
        self.create_sidebar()
        
        # ============ MAIN CONTENT ============
        self.main_container = ctk.CTkFrame(
            self,
            fg_color=MODERN_COLORS['background'],
            corner_radius=0
        )
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
    
    def create_sidebar(self):
        """Create navigation sidebar with modern design"""
        self.sidebar = ctk.CTkFrame(
            self,
            width=280,
            fg_color=MODERN_COLORS['sidebar'],
            corner_radius=0,
            border_width=1,
            border_color=MODERN_COLORS['border']
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Logo section
        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent",
            height=80
        )
        logo_frame.pack(pady=(25, 20), padx=25, fill="x")
        
        ctk.CTkLabel(
            logo_frame,
            text="AI Study Planner",
            font=("Segoe UI Display", 24, "bold"),
            text_color=MODERN_COLORS['text']
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            logo_frame,
            text="PREMIUM EDITION",
            font=("Segoe UI", 10, "bold"),
            text_color=MODERN_COLORS['secondary']
        ).pack(anchor="w")
        
        # User profile
        profile_card = ctk.CTkFrame(
            self.sidebar,
            fg_color=MODERN_COLORS['hover'],
            corner_radius=12,
            border_width=1,
            border_color=MODERN_COLORS['border']
        )
        profile_card.pack(pady=(0, 25), padx=20, fill="x")
        
        profile_content = ctk.CTkFrame(profile_card, fg_color="transparent")
        profile_content.pack(fill="x", padx=15, pady=12)
        
        # Avatar
        avatar = ctk.CTkFrame(
            profile_content,
            width=45,
            height=45,
            fg_color=MODERN_COLORS['primary'],
            corner_radius=23
        )
        avatar.pack(side="left")
        
        ctk.CTkLabel(
            avatar,
            text=self.user['full_name'][0].upper(),
            font=("Segoe UI", 18, "bold"),
            text_color=MODERN_COLORS['background']
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Profile text
        text_frame = ctk.CTkFrame(profile_content, fg_color="transparent")
        text_frame.pack(side="left", padx=12)
        
        ctk.CTkLabel(
            text_frame,
            text=self.user['full_name'],
            font=("Segoe UI", 14, "bold"),
            text_color=MODERN_COLORS['text'],
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            text_frame,
            text="Pro Member",
            font=("Segoe UI", 11),
            text_color=MODERN_COLORS['success'],
            anchor="w"
        ).pack(anchor="w")
        
        # Navigation
        nav_items = [
            ("🏠", "Dashboard", "home"),
            ("📚", "My Subjects", "subjects"),
            ("📅", "Study Planner", "planner"),
            ("📊", "Analytics", "analytics"),
            ("🤖", "AI Assistant", "chatbot"),
            ("🏆", "Leaderboard", "leaderboard"),
            ("🔔", "Notifications", "notifications"),
            ("⚙️", "Settings", "settings"),
        ]
        
        ctk.CTkLabel(
            self.sidebar,
            text="MENU",
            font=("Segoe UI", 11, "bold"),
            text_color=MODERN_COLORS['text_light']
        ).pack(pady=(10, 10), padx=25, anchor="w")
        
        self.nav_buttons = {}
        
        for icon, text, page in nav_items:
            # Active/Inactive colors will be handled in navigate_to
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{icon}  {text}",
                font=("Segoe UI", 13),
                height=45,
                corner_radius=8,
                fg_color="transparent",
                hover_color=MODERN_COLORS['hover'],
                text_color=MODERN_COLORS['text_light'],
                anchor="w",
                command=lambda p=page: self.navigate_to(p)
            )
            btn.pack(pady=3, padx=20, fill="x")
            self.nav_buttons[page] = btn
            
        # Initial Badge Update
        self.update_notification_badge()
        
        # Spacer
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(expand=True)
        
        # Logout button
        ctk.CTkButton(
            self.sidebar,
            text="🚪  Logout",
            font=("Segoe UI", 13),
            height=45,
            corner_radius=8,
            fg_color="#ef4444", # Red
            hover_color="#dc2626",
            text_color="white",
            command=self.logout
        ).pack(pady=20, padx=20, fill="x")
    
    def handle_search(self, event=None):
        """Handle search input"""
        query = self.search_entry.get().strip()
        if query:
            self.show_search(query)
            self.search_entry.delete(0, 'end')

    def navigate_to(self, page):
        """Navigate between pages"""
        self.current_page = page
        
        # Update nav button colors - modern style
        for btn_page, btn in self.nav_buttons.items():
            if btn_page == page:
                btn.configure(
                    fg_color=MODERN_COLORS['card'],
                    text_color=MODERN_COLORS['primary'],
                    font=("Segoe UI", 13, "bold")
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=MODERN_COLORS['text'],
                    font=("Segoe UI", 13)
                )
        
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Show page
        if page == "home":
            self.show_home()
        elif page == "subjects":
            self.show_subjects()
        elif page == "planner":
            self.show_planner()
        elif page == "analytics":
            self.show_analytics()
        elif page == "chatbot":
            self.show_chatbot()
        elif page == "leaderboard": # New
            self.show_leaderboard()
        elif page == "notifications":
            self.show_notifications()
        elif page == "settings":
            self.show_settings()
    
    def show_home(self):
        """Show home page"""
        from home_view import HomeView
        HomeView(self.main_container, self)
    
    def show_subjects(self):
        """Show subjects page"""
        from subjects_manager import SubjectsManager
        SubjectsManager(self.main_container, self)
    
    def show_planner(self):
        """Show planner page"""
        from study_planner import StudyPlanner
        StudyPlanner(self.main_container, self)
    
    def show_analytics(self):
        """Show analytics page"""
        from analytics_view import AnalyticsView
        AnalyticsView(self.main_container, self)
    
    def show_chatbot(self):
        """Show chatbot page"""
        from chatbot_view import ChatbotView
        ChatbotView(self.main_container, self)

    def show_leaderboard(self):
        """Show leaderboard page"""
        from leaderboard_view import LeaderboardView
        LeaderboardView(self.main_container, self)

    def show_notifications(self):
        """Show notifications page"""
        NotificationView(self.main_container, self)

    def show_search(self, query):
        """Show search results"""
        from search_view import SearchView
        # Clear container first
        for widget in self.main_container.winfo_children():
            widget.destroy()
        SearchView(self.main_container, self, query)
    
    def refresh_data(self):
        """Refresh user data"""
        self.load_user_data()
    
    def show_settings(self):
        """Show account settings page"""
        from account_settings import AccountSettings
        AccountSettings(self.main_container, self)
    
    def start_tour(self):
        """Start interactive tour (Placeholder)"""
        messagebox.showinfo("Welcome!", "Welcome to your new AI Study Planner! Explore the sidebar to get started.")

    def logout(self):
        """Logout"""
        response = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?",
            parent=self
        )
        if response:
            # Stop notification service
            if hasattr(self, 'notification_service'):
                self.notification_service.stop()

            self.destroy()
            self.parent.deiconify()
            if hasattr(self.parent, 'username_entry'):
                self.parent.username_entry.delete(0, 'end')
                self.parent.password_entry.delete(0, 'end')
    
    def on_closing(self):
        """Handle window close (X button)"""
        response = messagebox.askyesnocancel(
            "Minimize to Tray?",
            "Run in background to receive notifications?\n\nYES = Minimize to Tray\nNO = Exit Application"
        )
        
        if response is None: # Cancel
            return
            
        if response: # Yes -> Minimize
            self.minimize_to_tray()
        else: # No -> Exit
            self.quit_completely()

    def minimize_to_tray(self):
        """Minimize window to system tray"""
        self.withdraw()
        # Run tray icon in separate thread
        threading.Thread(target=self.create_tray, daemon=True).start()

    def create_tray(self):
        """Create system tray icon"""
        # Create a simple icon
        try:
            image = Image.open("dashboard.jpg")
            image = image.resize((64, 64))
        except:
            image = Image.new('RGB', (64, 64), color=(56, 189, 248))
            
        menu = pystray.Menu(
            pystray.MenuItem("Show AI Study Planner", self.restore_from_tray, default=True),
            pystray.MenuItem("Exit", self.quit_from_tray)
        )
        
        self.tray_icon = pystray.Icon("AI Study Planner", image, "AI Study Planner", menu)
        self.tray_icon.run()

    def restore_from_tray(self, icon, item):
        """Restore window from tray"""
        icon.stop()
        self.after(0, self.restore_window)

    def restore_window(self):
        self.deiconify()
        self.state('zoomed')
        self.lift()
        self.focus_force()

    def quit_from_tray(self, icon, item):
        """Quit from tray"""
        icon.stop()
        self.after(0, self.quit_completely)

    def quit_completely(self):
        """Exit application completely"""
        if hasattr(self, 'notification_service'):
            self.notification_service.stop()
        self.destroy()
        self.parent.destroy()
        sys.exit(0)


    def update_notification_badge(self):
        """Update notification badge count"""
        try:
            count = db.count_unread_notifications(self.user['user_id'])
            btn = self.nav_buttons.get('notifications')
            
            if btn:
                if count > 0:
                    btn.configure(
                        text=f"🔔  Notifications ({count})",
                        text_color="#ef4444", # Red for unread
                        font=("Segoe UI", 13, "bold")
                    )
                else:
                    btn.configure(
                        text=f"🔔  Notifications",
                        text_color=MODERN_COLORS['text_light'],
                        font=("Segoe UI", 13)
                    )
        except Exception as e:
            print(f"Error updating badge: {e}")

# Export modern colors for other modules to use
def get_modern_colors():
    """Get modern color scheme"""
    return MODERN_COLORS