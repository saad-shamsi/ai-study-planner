import customtkinter as ctk
from config import COLORS

class OTPVerificationDialog(ctk.CTkToplevel):
    """
    Dialog for verifying OTP.
    Blocks the main window until verified or cancelled.
    """
    def __init__(self, parent, email, expected_otp, on_verify=None):
        super().__init__(parent)
        self.parent = parent
        self.email = email
        self.expected_otp = expected_otp
        self.on_verify = on_verify # Callback function(bool)
        self.verified = False
        
        self.title("Verify Email - AI Study Planner")
        self.configure(fg_color=COLORS['background'])
        
        # Geometry
        self.geometry("400x350")
        self.resizable(False, False)
        
        # Center relative to screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 350) // 2
        self.geometry(f"+{x}+{y}")
        
        self.transient(parent)
        self.grab_set()
        
        self.create_ui()
        
    def create_ui(self):
        # Icon
        ctk.CTkLabel(
            self,
            text="🔒",
            font=("Segoe UI", 48)
        ).pack(pady=(20, 10))
        
        # Title
        ctk.CTkLabel(
            self,
            text="Two-Factor Authentication",
            font=("Segoe UI Display", 20, "bold"),
            text_color=COLORS['text']
        ).pack()
        
        # Message
        ctk.CTkLabel(
            self,
            text=f"We sent a code to\n{self.email}",
            font=("Segoe UI", 14),
            text_color=COLORS['text_light'],
            anchor="center",
            justify="center"
        ).pack(pady=(5, 20))
        
        # Code Input
        self.code_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter 6-digit code",
            width=200,
            height=40,
            font=("Segoe UI", 16, "bold"),
            justify="center",
            fg_color=COLORS['hover'],
            border_color=COLORS['border'],
            text_color=COLORS['text']
        )
        self.code_entry.pack(pady=(0, 20))
        self.code_entry.focus()
        
        # Verify Button
        self.verify_btn = ctk.CTkButton(
            self,
            text="Verify",
            command=self.verify,
            width=200,
            height=40,
            font=("Segoe UI Bold", 14),
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            text_color=COLORS['background']
        )
        self.verify_btn.pack(pady=(0, 10))
        
        # Cancel Button
        ctk.CTkButton(
            self,
            text="Cancel",
            command=self.cancel,
            width=200,
            height=30,
            font=("Segoe UI", 13),
            fg_color="transparent",
            hover_color=COLORS['hover'],
            text_color=COLORS['text_light']
        ).pack()
        
        self.bind('<Return>', lambda e: self.verify())

    def verify(self):
        entered_code = self.code_entry.get().strip()
        
        if entered_code == self.expected_otp:
            self.verified = True
            if self.on_verify:
                self.on_verify(True)
            self.destroy()
        else:
            self.code_entry.configure(border_color=COLORS['warning'])
            # Shake animation or error text could be added here
            
    def cancel(self):
        self.verified = False
        if self.on_verify:
            self.on_verify(False)
        self.destroy()
