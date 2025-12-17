import customtkinter as ctk
from tkinter import messagebox
from database import db
from signup import SignupWindow
from dashboard import Dashboard
from config import COLORS
from email_utils import generate_otp, send_otp_email
from otp_dialog import OTPVerificationDialog
import json
import os

CREDENTIALS_FILE = "credentials.json"


class LoginWindow(ctk.CTk):
    """Professional Premium Login Window - Aurora Theme"""
    
    def __init__(self):
        super().__init__()
        
        # Set DARK mode for Aurora Theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # Window configuration
        self.title("AI Study Planner - Login")
        self.configure(fg_color=COLORS['background'])
        
        # Center window dynamically
        self.center_window()
        
        # Create UI
        self.create_ui()
        
        # Load saved credentials
        self.load_credentials()
    
    def center_window(self):
        """Dynamically adjust size to 85% width and 85% height of screen"""
        self.update_idletasks()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Use 85% of screen size (Balanced fit)
        width = int(screen_width * 0.85)
        height = int(screen_height * 0.85)
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.minsize(900, 600)

    def create_ui(self):
        """Create the login interface with adjusted spacing"""
        
        # Main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # ============ LEFT SIDE - Welcome Section (Brand Color) ============
        left_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS['primary'], # Aurora Cyan
            corner_radius=0
        )
        left_frame.grid(row=0, column=0, sticky="nsew")
        
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        
        left_content = ctk.CTkFrame(left_frame, fg_color="transparent")
        left_content.grid(row=0, column=0)
        
        # Illustration/Icon
        icon_container = ctk.CTkFrame(
            left_content,
            fg_color=COLORS['background'], # Dark contrast
            corner_radius=30,
            width=140,
            height=140
        )
        icon_container.pack(pady=(0, 20))
        icon_container.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_container,
            text="📚",
            font=("Segoe UI", 80)
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # App title
        ctk.CTkLabel(
            left_content,
            text="AI Study Planner",
            font=("Segoe UI Display", 32, "bold"),
            text_color=COLORS['background']
        ).pack(pady=(0, 10))
        
        # Tagline
        ctk.CTkLabel(
            left_content,
            text="Your Smart Learning Companion",
            font=("Segoe UI", 16),
            text_color=COLORS['background']
        ).pack(pady=(0, 30))
        
        # Features
        features = [
            "✓ Organize your subjects efficiently",
            "✓ Track study time & progress",
            "✓ Set goals & achieve them",
            "✓ AI-powered study assistance",
        ]
        
        for feature in features:
            feature_frame = ctk.CTkFrame(
                left_content,
                fg_color=COLORS['card'], # Semi-transparent dark
                corner_radius=10
            )
            feature_frame.pack(fill="x", pady=4, padx=40)
            
            ctk.CTkLabel(
                feature_frame,
                text=feature,
                font=("Segoe UI", 13),
                text_color=COLORS['text'], # Fixed contrast on dark card
                anchor="w"
            ).pack(padx=15, pady=10, anchor="w")
        
        # ============ RIGHT SIDE - Login Form (Dark Card) ============
        right_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS['card'], # Dark Slate
            corner_radius=0
        )
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Login Content Container
        login_content = ctk.CTkFrame(right_frame, fg_color="transparent")
        login_content.grid(row=0, column=0, padx=40, pady=20)
        
        # Welcome text
        ctk.CTkLabel(
            login_content,
            text="Welcome Back! 👋",
            font=("Segoe UI Display", 32, "bold"),
            text_color=COLORS['text']
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            login_content,
            text="Please login to continue",
            font=("Segoe UI", 14),
            text_color=COLORS['text_light']
        ).pack(pady=(0, 30))
        
        # Username field
        ctk.CTkLabel(
            login_content,
            text="Username",
            font=("Segoe UI Bold", 13),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            login_content,
            placeholder_text="Enter your username",
            width=350,
            height=45,
            font=("Segoe UI", 14),
            corner_radius=12,
            border_width=1,
            border_color=COLORS['border'],
            fg_color=COLORS['hover'], # Slightly lighter dark
            text_color=COLORS['text']
        )
        self.username_entry.pack(pady=(0, 15))
        
        # Password field
        ctk.CTkLabel(
            login_content,
            text="Password",
            font=("Segoe UI Bold", 13),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            login_content,
            placeholder_text="Enter your password",
            width=350,
            height=45,
            font=("Segoe UI", 14),
            show="●",
            corner_radius=12,
            border_width=1,
            border_color=COLORS['border'],
            fg_color=COLORS['hover'],
            text_color=COLORS['text']
        )
        self.password_entry.pack(pady=(0, 10))
        
        # Options row
        options_frame = ctk.CTkFrame(login_content, fg_color="transparent")
        options_frame.pack(fill="x", pady=(0, 25))
        
        self.show_password_var = ctk.BooleanVar()
        ctk.CTkCheckBox(
            options_frame,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password,
            font=("Segoe UI", 12),
            text_color=COLORS['text_light'],
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            border_color=COLORS['text_light']
        ).pack(side="left")

        # Remember Me
        self.remember_me_var = ctk.BooleanVar()
        ctk.CTkCheckBox(
            options_frame,
            text="Remember Me",
            variable=self.remember_me_var,
            font=("Segoe UI", 12),
            text_color=COLORS['text_light'],
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            border_color=COLORS['text_light']
        ).pack(side="right")
        
        # Login button
        self.login_button = ctk.CTkButton(
            login_content,
            text="Login",
            command=self.handle_login,
            width=350,
            height=50,
            font=("Segoe UI Bold", 16),
            corner_radius=12,
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            text_color=COLORS['background'] # Dark text on bright button
        )
        self.login_button.pack(pady=(0, 20))
        
        # Divider
        divider_frame = ctk.CTkFrame(login_content, fg_color="transparent")
        divider_frame.pack(fill="x", pady=15)
        
        ctk.CTkFrame(
            divider_frame,
            height=1,
            fg_color=COLORS['border']
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            divider_frame,
            text="OR",
            font=("Segoe UI Bold", 12),
            text_color=COLORS['text_light']
        ).pack(side="left")
        
        ctk.CTkFrame(
            divider_frame,
            height=1,
            fg_color=COLORS['border']
        ).pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Signup section
        signup_frame = ctk.CTkFrame(login_content, fg_color="transparent")
        signup_frame.pack()
        
        ctk.CTkLabel(
            signup_frame,
            text="Don't have an account?",
            font=("Segoe UI", 14),
            text_color=COLORS['text_light']
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkButton(
            signup_frame,
            text="Sign Up",
            command=self.open_signup,
            font=("Segoe UI Bold", 14),
            text_color=COLORS['primary'],
            fg_color="transparent",
            hover_color=COLORS['hover'],
            width=80,
            height=30
        ).pack(side="left")
        
        # Bind Enter key
        self.bind('<Return>', lambda e: self.handle_login())
    
    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="●")
    
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields!", parent=self)
            return
        
        self.login_button.configure(state="disabled", text="Logging in...")
        self.update()
        
        user = db.verify_user(username, password)
        
        if user:
            # ============ 2FA: LOGIN VERIFICATION ============
            # Get user email
            user_email = user['email']
            
            self.login_button.configure(text="Sending OTP...")
            self.update()
            
            otp = generate_otp()
            if send_otp_email(user_email, otp):
                 self.login_button.configure(text="Verifying...")
                 
                 is_verified = False
                 def on_verify(result):
                     nonlocal is_verified
                     is_verified = result
                 
                 OTPVerificationDialog(self, user_email, otp, on_verify).wait_window()
                 
                 if not is_verified:
                     self.login_button.configure(state="normal", text="Login")
                     messagebox.showerror("Verification Failed", "2FA failed or cancelled.", parent=self)
                     return
            else:
                 self.login_button.configure(state="normal", text="Login")
                 messagebox.showerror("Error", "Failed to send 2FA Code.", parent=self)
                 return
            # =================================================

            # Save credentials if "Remember Me" is checked
            if self.remember_me_var.get():
                self.save_credentials(username, password)
            else:
                self.clear_credentials()

            # --- UPDATE STREAK ---
            new_streak = db.update_login_streak(user['user_id'])
            
            # --- START SERVICES ---
            # NOTE: Notification service is started inside Dashboard if needed, 
            # but usually it's better to verify logic there.
            
            # Show Toast if streak increased
            if new_streak > 1:
                from plyer import notification
                notification.notify(
                    title="🔥 Streak Maintained!",
                    message=f"You are on a {new_streak} day streak! Keep it up!",
                    app_name="AI Study Planner",
                    timeout=5
                )

            self.open_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid username or password!", parent=self)
            self.login_button.configure(state="normal", text="Login")
    
    def open_dashboard(self, user):
        """Hides login and opens dashboard cleanly"""
        # 1. Hide the login window immediately
        self.withdraw()
        
        # 2. Reset login fields (for security if they logout later)
        self.password_entry.delete(0, 'end')
        self.login_button.configure(state="normal", text="Login")
        
        # 3. Create and show Dashboard
        # We pass 'self' as parent so Dashboard can call self.deiconify() on logout
        dashboard = Dashboard(user, self)
        
        # 4. Force focus to new window
        dashboard.focus_force()
        dashboard.lift()
    
    def open_signup(self):
        self.withdraw()
        signup = SignupWindow(self)

    def save_credentials(self, username, password):
        """Save credentials to local file"""
        try:
            data = {"username": username, "password": password}
            with open(CREDENTIALS_FILE, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving credentials: {e}")

    def load_credentials(self):
        """Load credentials if they exist"""
        if os.path.exists(CREDENTIALS_FILE):
            try:
                with open(CREDENTIALS_FILE, "r") as f:
                    data = json.load(f)
                    if "username" in data and "password" in data:
                        self.username_entry.insert(0, data["username"])
                        self.password_entry.insert(0, data["password"])
                        self.remember_me_var.set(True)
            except Exception as e:
                print(f"Error loading credentials: {e}")

    def clear_credentials(self):
        """Clear saved credentials"""
        if os.path.exists(CREDENTIALS_FILE):
            try:
                os.remove(CREDENTIALS_FILE)
            except Exception as e:
                print(f"Error clearing credentials: {e}")

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()