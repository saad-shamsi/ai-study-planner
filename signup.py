import customtkinter as ctk
from tkinter import messagebox
import re
from database import db
from config import COLORS
from email_utils import generate_otp, send_otp_email
from otp_dialog import OTPVerificationDialog

class SignupWindow(ctk.CTkToplevel):
    """Professional Premium Signup Window - Aurora Theme"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        
        # Set DARK mode
        ctk.set_appearance_mode("Dark")
        
        # Window configuration
        self.title("AI Study Planner - Sign Up")
        self.configure(fg_color=COLORS['background'])
        
        # 1. ENABLE RESIZING
        self.resizable(True, True)
        
        # 2. Dynamic Size
        self.center_window()
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Create UI
        self.create_ui()
    
    def center_window(self):
        """Dynamically adjust size to 85% width and 90% height of screen"""
        self.update_idletasks()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Use 85% width and 90% height so it fits comfortably
        width = int(screen_width * 0.85)
        height = int(screen_height * 0.90)
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Set a minimum size
        self.minsize(900, 650)
    
    def create_ui(self):
        """Create signup interface (Compact Layout)"""
        
        # Main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # ============ LEFT SIDE (Brand Color) ============
        left_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS['secondary'], # Aurora Purple
            corner_radius=0
        )
        left_frame.grid(row=0, column=0, sticky="nsew")
        
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        
        left_content = ctk.CTkFrame(left_frame, fg_color="transparent")
        left_content.grid(row=0, column=0, padx=30)
        
        # Icon
        icon_container = ctk.CTkFrame(
            left_content,
            fg_color=COLORS['background'],
            corner_radius=30,
            width=120,
            height=120
        )
        icon_container.pack(pady=(0, 20))
        icon_container.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_container,
            text="🎓",
            font=("Segoe UI", 70)
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        ctk.CTkLabel(
            left_content,
            text="Join Us Today!",
            font=("Segoe UI Display", 32, "bold"),
            text_color=COLORS['background']
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            left_content,
            text="Start Your Learning Journey",
            font=("Segoe UI", 16),
            text_color=COLORS['background']
        ).pack(pady=(0, 25))
        
        # Benefits
        benefits = [
            ("📊", "Track Your Progress", "Monitor study time"),
            ("🎯", "Set Smart Goals", "Achieve targets"),
            ("🤖", "AI Assistant", "Personalized help"),
            ("📱", "Easy to Use", "Clean interface"),
        ]
        
        for icon, title, desc in benefits:
            card = ctk.CTkFrame(
                left_content,
                fg_color=COLORS['card'],
                corner_radius=10
            )
            card.pack(fill="x", pady=5)
            
            content_frame = ctk.CTkFrame(card, fg_color="transparent")
            content_frame.pack(fill="x", padx=15, pady=10)
            
            ctk.CTkLabel(
                content_frame,
                text=icon,
                font=("Segoe UI", 24)
            ).pack(side="left", padx=(0, 10))
            
            text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(
                text_frame,
                text=title,
                font=("Segoe UI Bold", 13),
                text_color=COLORS['background'], # Dark text on purple bg? Wait purple is bg.
                # Actually left frame is secondary (Purple). Card is dark (background).
                # So text inside card should be white/light.
                # Wait, card fg_color is background (Dark).
                # So text should be White.
                # "text_color=COLORS['secondary']" in original was correct for light theme.
                # Here we need light text.
            ).configure(text_color=COLORS['text']) # Set to OFF-WHITE
            ctk.CTkLabel(
                text_frame,
                text=title,
                font=("Segoe UI Bold", 13),
                text_color="#F8FAFC", # Explicit white
                anchor="w"
            ).pack(anchor="w", fill="x")
            
            ctk.CTkLabel(
                text_frame,
                text=desc,
                font=("Segoe UI", 11),
                text_color="#CBD5E1", # Light gray
                anchor="w"
            ).pack(anchor="w", fill="x")
        
        # ============ RIGHT SIDE - Form (Dark Card) ============
        right_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS['card'],
            corner_radius=0
        )
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollable form
        form_scroll = ctk.CTkScrollableFrame(
            right_frame,
            fg_color="transparent"
        )
        form_scroll.grid(row=0, column=0, padx=40, pady=20, sticky="nsew")
        
        # Header
        ctk.CTkLabel(
            form_scroll,
            text="Create Account ✨",
            font=("Segoe UI Display", 28, "bold"),
            text_color=COLORS['text']
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            form_scroll,
            text="Fill in your details to get started",
            font=("Segoe UI", 13),
            text_color=COLORS['text_light']
        ).pack(pady=(0, 20))
        
        # Full Name
        self.create_input(form_scroll, "Full Name", "Enter your full name", False)
        self.fullname_entry = self.current_entry
        
        # Username
        self.create_input(form_scroll, "Username", "Choose a username", False)
        self.username_entry = self.current_entry
        
        # Email
        self.create_input(form_scroll, "Email", "Enter your email", False)
        self.email_entry = self.current_entry
        
        # Student Level
        ctk.CTkLabel(
            form_scroll,
            text="Student Level",
            font=("Segoe UI Bold", 13),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 4))
        
        self.level_var = ctk.StringVar(value="University")
        self.level_combo = ctk.CTkComboBox(
            form_scroll,
            values=["High School", "University", "Masters/PhD", "Self-Learner"],
            variable=self.level_var,
            width=350,
            height=45,
            font=("Segoe UI", 14),
            corner_radius=12,
            border_width=1,
            border_color=COLORS['border'],
            fg_color=COLORS['hover'],
            text_color=COLORS['text'],
            dropdown_font=("Segoe UI", 13),
            button_color=COLORS['primary']
        )
        self.level_combo.pack(pady=(0, 12))
        
        # Password
        self.create_input(form_scroll, "Password", "Create password (min 8 chars)", True)
        self.password_entry = self.current_entry
        self.password_entry.bind('<KeyRelease>', self.check_password_strength)
        
        # Add visual requirements checklist
        self.create_password_requirements_ui(form_scroll)
        
        # Confirm Password
        self.create_input(form_scroll, "Confirm Password", "Re-enter password", True, last=True)
        self.confirm_entry = self.current_entry
        
        # Show password
        self.show_pass_var = ctk.BooleanVar()
        ctk.CTkCheckBox(
            form_scroll,
            text="Show passwords",
            variable=self.show_pass_var,
            command=self.toggle_passwords,
            font=("Segoe UI", 12),
            text_color=COLORS['text_light'],
            fg_color=COLORS['secondary'],
            hover_color=COLORS['secondary'],
            border_color=COLORS['text_light']
        ).pack(pady=(0, 15), anchor="w")
        
        # Terms
        self.terms_var = ctk.BooleanVar()
        ctk.CTkCheckBox(
            form_scroll,
            text="I agree to Terms of Service and Privacy Policy",
            variable=self.terms_var,
            font=("Segoe UI", 12),
            text_color=COLORS['text_light'],
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary'],
            border_color=COLORS['text_light']
        ).pack(pady=(0, 20), anchor="w")
        
        # Signup button
        self.signup_button = ctk.CTkButton(
            form_scroll,
            text="Create Account",
            command=self.handle_signup,
            width=350,
            height=50,
            font=("Segoe UI Bold", 16),
            corner_radius=12,
            fg_color=COLORS['secondary'],
            hover_color=COLORS['primary'],
            text_color=COLORS['background']
        )
        self.signup_button.pack(pady=(0, 20))
        
        # Back to login
        back_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")
        back_frame.pack(pady=(0, 20))
        
        ctk.CTkLabel(
            back_frame,
            text="Already have an account?",
            font=("Segoe UI", 13),
            text_color=COLORS['text_light']
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            back_frame,
            text="Login",
            command=self.back_to_login,
            font=("Segoe UI Bold", 13),
            text_color=COLORS['primary'],
            fg_color="transparent",
            hover_color=COLORS['hover'],
            width=60,
            height=30
        ).pack(side="left")
    
    def create_input(self, parent, label, placeholder, is_password, last=False):
        """Create input field - Compact"""
        ctk.CTkLabel(
            parent,
            text=label,
            font=("Segoe UI Bold", 13),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 4))
        
        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            width=350,
            height=45, # Reduced height
            font=("Segoe UI", 14),
            corner_radius=12,
            border_width=1,
            border_color=COLORS['border'],
            fg_color=COLORS['hover'],
            text_color=COLORS['text'],
            show="●" if is_password else ""
        )
        entry.pack(pady=(0, 12 if not last else 10))
        self.current_entry = entry

    def create_password_requirements_ui(self, parent):
        """Create visual password requirements checklist"""
        self.req_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.req_frame.pack(fill="x", pady=(0, 15))
        
        self.req_labels = {}
        requirements = {
            "length": "Min 8 characters",
            "upper": "At least 1 Uppercase (A-Z)",
            "special": "At least 1 Special (!@#$)"
        }
        
        for key, text in requirements.items():
            label = ctk.CTkLabel(
                self.req_frame,
                text=f"○ {text}",
                font=("Segoe UI", 11),
                text_color=COLORS['text_light'],
                anchor="w"
            )
            label.pack(anchor="w")
            self.req_labels[key] = label
            
    def check_password_strength(self, event=None):
        """Real-time password validation"""
        password = self.password_entry.get()
        
        # 1. Check Length
        if len(password) >= 8:
            self.update_req_label("length", True)
            v_len = True
        else:
            self.update_req_label("length", False)
            v_len = False
            
        # 2. Check Uppercase
        if re.search(r"[A-Z]", password):
            self.update_req_label("upper", True)
            v_upper = True
        else:
            self.update_req_label("upper", False)
            v_upper = False
            
        # 3. Check Special Char
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            self.update_req_label("special", True)
            v_special = True
        else:
            self.update_req_label("special", False)
            v_special = False
            
        return v_len and v_upper and v_special

    def update_req_label(self, key, valid):
        """Update label color and icon"""
        label = self.req_labels[key]
        if valid:
            label.configure(text=label.cget("text").replace("○", "✓").replace("✕", "✓"), text_color=COLORS['success'])
        else:
            # Only switch back if it was valid before, or default
            txt = label.cget("text")
            if "✓" in txt:
                label.configure(text=txt.replace("✓", "○"), text_color=COLORS['text_light'])

    def toggle_passwords(self):
        """Toggle password visibility"""
        if self.show_pass_var.get():
            self.password_entry.configure(show="")
            self.confirm_entry.configure(show="")
        else:
            self.password_entry.configure(show="●")
            self.confirm_entry.configure(show="●")
    
    def validate_email(self, email):
        """Validate email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def handle_signup(self):
        """Handle signup"""
        fullname = self.fullname_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        student_level = self.level_var.get()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        
        # Validation
        if not all([fullname, username, email, password, confirm]):
            messagebox.showerror("Error", "Please fill all fields!", parent=self)
            return
        
        if not self.terms_var.get():
            messagebox.showerror("Error", "Please agree to terms!", parent=self)
            return
        
        if len(username) < 3:
            messagebox.showerror("Error", "Username too short!", parent=self)
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email!", parent=self)
            return
        
        if not self.check_password_strength():
            messagebox.showerror("Error", "Password does not meet requirements!", parent=self)
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords don't match!", parent=self)
            return
        
        if db.check_username_exists(username):
            messagebox.showerror("Error", "Username taken!", parent=self)
            return
        
        if db.check_email_exists(email):
            messagebox.showerror("Error", "Email already registered!", parent=self)
            return

        # ============ 2FA: EMAIL VERIFICATION ============
        self.signup_button.configure(state="disabled", text="Sending OTP...")
        self.update()

        otp = generate_otp()
        if send_otp_email(email, otp):
             # Open Dialog
             self.signup_button.configure(text="Verifying...")
             
             is_verified = False
             
             def on_verify(result):
                 nonlocal is_verified
                 is_verified = result
             
             # Block user until verified or cancelled
             OTPVerificationDialog(self, email, otp, on_verify).wait_window()
             
             if not is_verified:
                 self.signup_button.configure(state="normal", text="Create Account")
                 messagebox.showerror("Verification Failed", "Email verification failed or cancelled.", parent=self)
                 return
        else:
             self.signup_button.configure(state="normal", text="Create Account")
             messagebox.showerror("Error", "Failed to send OTP. Check internet or email settings.", parent=self)
             return
        # =================================================
        
        # Create user
        self.signup_button.configure(state="disabled", text="Creating...")
        self.update()
        
        user_id = db.create_user(username, email, password, fullname, student_level)
        
        if user_id:
            messagebox.showinfo(
                "Success",
                f"Welcome {fullname}!\nAccount verified and created successfully.",
                parent=self
            )
            self.back_to_login()
        else:
            messagebox.showerror("Error", "Failed to create account!", parent=self)
            self.signup_button.configure(state="normal", text="Create Account")
    
    def back_to_login(self):
        """Back to login"""
        self.destroy()
        self.parent.deiconify()
    
    # This part allows you to run 'python signup.py' to test the design safely
if __name__ == "__main__":
    # Create a dummy root window so the popup has something to attach to
    root = ctk.CTk()
    root.withdraw() # Hide the ugly root window
    
    app = SignupWindow(root)
    app.protocol("WM_DELETE_WINDOW", root.destroy) # Close everything when X is clicked
    root.mainloop()
if __name__ == "__main__":
    # Create a dummy root window so the popup has something to attach to
    root = ctk.CTk()
    root.withdraw() # Hide the ugly root window
    
    app = SignupWindow(root)
    app.protocol("WM_DELETE_WINDOW", root.destroy) # Close everything when X is clicked
    root.mainloop()