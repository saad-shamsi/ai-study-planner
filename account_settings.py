"""
Account Settings - Manage user account
Edit profile, change password, delete account, logout, export data
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from database import db
from config import COLORS
import re
import csv
import json
from datetime import datetime
from email_utils import generate_otp, send_otp_email
from otp_dialog import OTPVerificationDialog

class AccountSettings:
    """Account Settings View"""
    
    def __init__(self, parent, dashboard):
        self.parent = parent
        self.dashboard = dashboard
        self.user_id = dashboard.user['user_id']
        self.user = dashboard.user
        
        self.create_ui()
    
    def create_ui(self):
        """Create account settings interface"""
        
        # Main scrollable frame
        main_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color="transparent"
        )
        main_frame.pack(fill="both", expand=True, padx=35, pady=35)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(
            header,
            text="⚙️ Account Settings",
            font=("Arial Black", 34),
            text_color=COLORS['text']
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header,
            text="Manage your account information and preferences",
            font=("Arial", 15),
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 0))
        
        # Profile Card
        self.create_profile_card(main_frame)
        
        # Action Cards Grid
        actions_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        actions_container.pack(fill="x", pady=(0, 20))
        
        actions_container.grid_columnconfigure(0, weight=1)
        actions_container.grid_columnconfigure(1, weight=1)
        
        # Edit Account Info
        self.create_action_card(
            actions_container,
            "✏️ Edit Account Info",
            "Update your username, email, and full name",
            COLORS['info'],
            self.show_edit_account_dialog,
            row=0, col=0
        )
        
        # Change Password
        self.create_action_card(
            actions_container,
            "🔒 Change Password",
            "Update your account password",
            COLORS['warning'],
            self.show_change_password_dialog,
            row=0, col=1
        )
        
        # Data Export (New)
        self.create_action_card(
            actions_container,
            "📥 Export Data",
            "Download your study data as CSV",
            COLORS['primary'],
            self.export_data,
            row=1, col=0
        )
        
        # Logout
        self.create_action_card(
            actions_container,
            "🚪 Logout",
            "Sign out of your account",
            COLORS['secondary'],
            self.logout_account,
            row=1, col=1
        )
        
        # Danger Zone
        self.create_danger_zone(main_frame)
    
    def create_profile_card(self, parent):
        """Create profile information card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS['card'],
            corner_radius=20,
            border_width=1,
            border_color=COLORS['border']
        )
        card.pack(fill="x", pady=(0, 25))
        
        # Header
        ctk.CTkLabel(
            card,
            text="👤 Profile Information",
            font=("Arial Black", 20),
            text_color=COLORS['text']
        ).pack(pady=(25, 20), padx=25, anchor="w")
        
        # Info Grid
        info_container = ctk.CTkFrame(card, fg_color="transparent")
        info_container.pack(fill="x", padx=25, pady=(0, 25))
        
        info_items = [
            ("Full Name", self.user['full_name']),
            ("Username", self.user['username']),
            ("Email", self.user['email']),
            ("Student Level", self.user.get('student_level', 'N/A')),
            ("Account Created", self.user['created_at'].strftime("%B %d, %Y"))
        ]
        
        for label, value in info_items:
            row = ctk.CTkFrame(
                info_container,
                fg_color=COLORS['background'],
                corner_radius=12
            )
            row.pack(fill="x", pady=5)
            
            content = ctk.CTkFrame(row, fg_color="transparent")
            content.pack(fill="x", padx=20, pady=15)
            
            ctk.CTkLabel(
                content,
                text=label,
                font=("Arial Bold", 13),
                text_color=COLORS['text_light'],
                anchor="w",
                width=150
            ).pack(side="left")
            
            ctk.CTkLabel(
                content,
                text=value,
                font=("Arial", 13),
                text_color=COLORS['text'],
                anchor="w"
            ).pack(side="left", fill="x", expand=True)
    
    def create_action_card(self, parent, title, description, color, command, row, col):
        """Create action button card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS['card'],
            corner_radius=20,
            border_width=1,
            border_color=COLORS['border']
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Color bar
        color_bar = ctk.CTkFrame(
            card,
            height=6,
            fg_color=color,
            corner_radius=0
        )
        color_bar.pack(fill="x")
        
        # Content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=25)
        
        ctk.CTkLabel(
            content,
            text=title,
            font=("Arial Black", 18),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))
        
        ctk.CTkLabel(
            content,
            text=description,
            font=("Arial", 13),
            text_color=COLORS['text_light'],
            anchor="w",
            wraplength=280,
            justify="left"
        ).pack(anchor="w", pady=(0, 20))
        
        ctk.CTkButton(
            content,
            text="Open",
            font=("Arial Bold", 14),
            height=45,
            corner_radius=12,
            fg_color=color,
            hover_color=color,
            text_color="white",
            command=command
        ).pack(fill="x")
    
    def create_danger_zone(self, parent):
        """Create danger zone for account deletion"""
        danger_card = ctk.CTkFrame(
            parent,
            fg_color="#FF5252",
            corner_radius=20
        )
        danger_card.pack(fill="x", pady=(10, 0))
        
        content = ctk.CTkFrame(danger_card, fg_color="transparent")
        content.pack(fill="x", padx=25, pady=25)
        
        ctk.CTkLabel(
            content,
            text="⚠️ Danger Zone",
            font=("Arial Black", 20),
            text_color="white"
        ).pack(anchor="w", pady=(0, 10))
        
        ctk.CTkLabel(
            content,
            text="Once you delete your account, there is no going back. This action is permanent and unrecoverable.",
            font=("Arial", 13),
            text_color="white",
            anchor="w",
            wraplength=800,
            justify="left"
        ).pack(anchor="w", pady=(0, 15))
        
        ctk.CTkButton(
            content,
            text="🗑️ Delete Account Permanently",
            font=("Arial Bold", 14),
            height=50,
            width=300,
            corner_radius=12,
            fg_color="white",
            hover_color="#FFEBEE",
            text_color="#FF5252",
            command=self.delete_account
        ).pack(anchor="w")
    
    def show_edit_account_dialog(self):
        """Show edit account information dialog"""
        # Confirmation
        response = messagebox.askyesno(
            "Edit Account",
            "Do you want to edit your account information?",
            parent=self.parent
        )
        
        if not response:
            return
        
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Edit Account Information")
        dialog.geometry("600x650")
        dialog.configure(fg_color=COLORS['background'])
        dialog.grab_set()
        dialog.attributes('-topmost', True)
        
        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 300
        y = (dialog.winfo_screenheight() // 2) - 325
        dialog.geometry(f'600x650+{x}+{y}')
        
        # Content
        content = ctk.CTkFrame(dialog, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=40)
        
        ctk.CTkLabel(
            content,
            text="✏️ Edit Account Info",
            font=("Arial Black", 28),
            text_color=COLORS['text']
        ).pack(pady=(0, 30))
        
        # Full Name
        ctk.CTkLabel(
            content,
            text="Full Name",
            font=("Arial Bold", 13),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        fullname_entry = ctk.CTkEntry(
            content,
            height=50,
            font=("Arial", 14),
            fg_color=COLORS['background']
        )
        fullname_entry.insert(0, self.user['full_name'])
        fullname_entry.pack(fill="x", pady=(0, 15))
        
        # Username
        ctk.CTkLabel(
            content,
            text="Username",
            font=("Arial Bold", 13),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        username_entry = ctk.CTkEntry(
            content,
            height=50,
            font=("Arial", 14),
            fg_color=COLORS['background']
        )
        username_entry.insert(0, self.user['username'])
        username_entry.pack(fill="x", pady=(0, 15))
        
        # Email
        ctk.CTkLabel(
            content,
            text="Email",
            font=("Arial Bold", 13),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        email_entry = ctk.CTkEntry(
            content,
            height=50,
            font=("Arial", 14),
            fg_color=COLORS['background']
        )
        email_entry.insert(0, self.user['email'])
        email_entry.pack(fill="x", pady=(0, 15))
        
        # Warning (Fixed color issue)
        warning = ctk.CTkFrame(content, fg_color=COLORS['card'], border_color=COLORS['warning'], border_width=1, corner_radius=10)
        warning.pack(fill="x", pady=(10, 25))
        
        ctk.CTkLabel(
            warning,
            text="⚠️ Note: Changing username or email may affect your login credentials.",
            font=("Arial", 12),
            text_color=COLORS['text'],
            wraplength=500
        ).pack(padx=15, pady=12)
        
        # Buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=140,
            height=50,
            font=("Arial Bold", 14),
            fg_color=COLORS['text_light'],
            hover_color=COLORS['text_light'],
            command=dialog.destroy
        ).pack(side="left")
        
        def save_changes():
            new_fullname = fullname_entry.get().strip()
            new_username = username_entry.get().strip()
            new_email = email_entry.get().strip()
            
            if not all([new_fullname, new_username, new_email]):
                messagebox.showerror("Error", "All fields are required!", parent=dialog)
                return
            
            # Validate email
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', new_email):
                messagebox.showerror("Error", "Invalid email format!", parent=dialog)
                return
            
            # Check if username changed and exists
            if new_username != self.user['username']:
                if db.check_username_exists(new_username):
                    messagebox.showerror("Error", "Username already taken!", parent=dialog)
                    return
            
            # Check if email changed and exists
            if new_email != self.user['email']:
                if db.check_email_exists(new_email):
                    messagebox.showerror("Error", "Email already registered!", parent=dialog)
                    return
                
                # --- EMAIL OTP VERIFICATION ---
                otp = generate_otp()
                if send_otp_email(new_email, otp):
                    verified = False
                    
                    def on_verify(success):
                        nonlocal verified
                        verified = success
                        
                    # Show OTP dialog
                    OTPVerificationDialog(dialog, new_email, otp, on_verify).wait_window()
                    
                    if not verified:
                        messagebox.showwarning("Verification Cancelled", "Email verification failed or cancelled. Changes not saved.", parent=dialog)
                        return
                else:
                    messagebox.showerror("Error", "Failed to send verification email. Please check your internet connection.", parent=dialog)
                    return
                # ------------------------------
            
            # Update in database
            result = db.update_user_info(self.user_id, new_username, new_email, new_fullname)
            
            if result:
                messagebox.showinfo("Success", "Account information updated successfully!", parent=dialog)
                # Update dashboard user data
                self.dashboard.user['full_name'] = new_fullname
                self.dashboard.user['username'] = new_username
                self.dashboard.user['email'] = new_email
                dialog.destroy()
                # Refresh settings view
                self.dashboard.navigate_to('settings')
            else:
                messagebox.showerror("Error", "Failed to update account information!", parent=dialog)
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Save Changes",
            width=180,
            height=50,
            font=("Arial Bold", 14),
            fg_color=COLORS['success'],
            hover_color=COLORS['success'],
            command=save_changes
        ).pack(side="right")
    
    def show_change_password_dialog(self):
        """Show change password dialog"""
        # Confirmation
        response = messagebox.askyesno(
            "Change Password",
            "Do you want to change your password?",
            parent=self.parent
        )
        
        if not response:
            return
        
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Change Password")
        dialog.geometry("600x700") # Increased height for checklist
        dialog.configure(fg_color=COLORS['background'])
        dialog.grab_set()
        dialog.attributes('-topmost', True)
        
        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 300
        y = (dialog.winfo_screenheight() // 2) - 350
        dialog.geometry(f'600x700+{x}+{y}')
        
        # Content
        content = ctk.CTkFrame(dialog, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=40)
        
        ctk.CTkLabel(
            content,
            text="🔒 Change Password",
            font=("Arial Black", 28),
            text_color=COLORS['text']
        ).pack(pady=(0, 30))
        
        # Current Password
        ctk.CTkLabel(
            content,
            text="Current Password",
            font=("Arial Bold", 13),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        current_pass = ctk.CTkEntry(
            content,
            placeholder_text="Enter current password",
            height=50,
            font=("Arial", 14),
            show="●",
            fg_color=COLORS['background']
        )
        current_pass.pack(fill="x", pady=(0, 15))
        
        # New Password
        ctk.CTkLabel(
            content,
            text="New Password",
            font=("Arial Bold", 13),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        new_pass = ctk.CTkEntry(
            content,
            placeholder_text="Enter new password (min 8 characters)",
            height=50,
            font=("Arial", 14),
            show="●",
            fg_color=COLORS['background']
        )
        new_pass.pack(fill="x", pady=(0, 10))
        
        self.new_pass_entry = new_pass
        self.new_pass_entry.bind('<KeyRelease>', self.check_password_strength)
        
        # Password Strength UI
        self.create_password_requirements_ui(content)
        
        # Confirm New Password
        ctk.CTkLabel(
            content,
            text="Confirm New Password",
            font=("Arial Bold", 13),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        confirm_pass = ctk.CTkEntry(
            content,
            placeholder_text="Re-enter new password",
            height=50,
            font=("Arial", 14),
            show="●",
            fg_color=COLORS['background']
        )
        confirm_pass.pack(fill="x", pady=(0, 20))
        
        # Show passwords checkbox
        show_var = ctk.BooleanVar()
        
        def toggle_passwords():
            if show_var.get():
                current_pass.configure(show="")
                new_pass.configure(show="")
                confirm_pass.configure(show="")
            else:
                current_pass.configure(show="●")
                new_pass.configure(show="●")
                confirm_pass.configure(show="●")
        
        ctk.CTkCheckBox(
            content,
            text="Show passwords",
            variable=show_var,
            command=toggle_passwords,
            font=("Arial", 12),
            text_color=COLORS['text'],
            fg_color=COLORS['primary']
        ).pack(anchor="w", pady=(0, 25))
        
        # Buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=140,
            height=50,
            font=("Arial Bold", 14),
            fg_color=COLORS['text_light'],
            hover_color=COLORS['text_light'],
            command=dialog.destroy
        ).pack(side="left")
        
        def change_password():
            current = current_pass.get().strip()
            new = new_pass.get().strip()
            confirm = confirm_pass.get().strip()
            
            if not all([current, new, confirm]):
                messagebox.showerror("Error", "All fields are required!", parent=dialog)
                return
            
            # Verify current password
            if not db.verify_user(self.user['username'], current):
                messagebox.showerror("Error", "Current password is incorrect!", parent=dialog)
                return
            
            if not self.check_password_strength():
                messagebox.showerror("Error", "Password doesn't meet requirements!", parent=dialog)
                return
            
            if new != confirm:
                messagebox.showerror("Error", "New passwords don't match!", parent=dialog)
                return
            
            # Update password
            result = db.update_user_password(self.user_id, new)
            
            if result:
                messagebox.showinfo("Success", "Password changed successfully!", parent=dialog)
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to change password!", parent=dialog)
        
        ctk.CTkButton(
            btn_frame,
            text="🔒 Change Password",
            width=200,
            height=50,
            font=("Arial Bold", 14),
            fg_color=COLORS['warning'],
            hover_color=COLORS['warning'],
            command=change_password
        ).pack(side="right")
        
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
        if not hasattr(self, 'new_pass_entry'):
            return False
            
        password = self.new_pass_entry.get()
        
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
        if not hasattr(self, 'req_labels') or key not in self.req_labels:
            return
            
        label = self.req_labels[key]
        if valid:
            label.configure(text=label.cget("text").replace("○", "✓").replace("✕", "✓"), text_color=COLORS['success'])
        else:
            # Only switch back if it was valid before, or default
            txt = label.cget("text")
            if "✓" in txt:
                label.configure(text=txt.replace("✓", "○"), text_color=COLORS['text_light'])

    def export_data(self):
        """Export user data to CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Export Study Data"
        )
        
        if not filename:
            return
            
        try:
            # Gather data
            sessions = db.get_user_sessions(self.user_id) or []
            subjects = db.get_user_subjects(self.user_id) or []
            goals = db.get_user_goals(self.user_id) or []
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write Subjects
                writer.writerow(["--- SUBJECTS ---"])
                writer.writerow(["ID", "Name", "Code", "Created At"])
                for s in subjects:
                    writer.writerow([s['subject_id'], s['subject_name'], s['subject_code'], s['created_at']])
                
                writer.writerow([])
                
                # Write Sessions
                writer.writerow(["--- STUDY SESSIONS ---"])
                writer.writerow(["ID", "Subject", "Date", "Duration (mins)", "Notes"])
                for s in sessions:
                    writer.writerow([s['session_id'], s['subject_name'], s['session_date'], s['duration_minutes'], s['notes']])
                
                writer.writerow([])
                
                # Write Goals
                writer.writerow(["--- GOALS ---"])
                writer.writerow(["ID", "Subject", "Goal Type", "Target", "Status", "Deadline"])
                for g in goals:
                    writer.writerow([g['goal_id'], g.get('subject_name', 'General'), g['goal_type'], g['target_value'], g['status'], g['target_date']])
            
            messagebox.showinfo("Success", "Data exported successfully!", parent=self.parent)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}", parent=self.parent)

    def logout_account(self):
        """Logout from account"""
        response = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?",
            parent=self.parent
        )
        
        if response:
            self.dashboard.logout()
    
    def delete_account(self):
        """Delete account permanently"""
        # First confirmation
        response1 = messagebox.askyesno(
            "⚠️ Delete Account",
            "Are you sure you want to delete your account?\n\nThis action cannot be undone!",
            parent=self.parent,
            icon='warning'
        )
        
        if not response1:
            return
        
        # Second confirmation
        response2 = messagebox.askyesno(
            "⚠️ Final Confirmation",
            "This is your FINAL warning!\n\nDeleting your account will permanently remove:\n\n• All your subjects\n• All study sessions\n• All goals and progress\n• All saved data\n\nTHIS CANNOT BE RECOVERED!\n\nAre you absolutely sure?",
            parent=self.parent,
            icon='warning'
        )
        
        if not response2:
            return
        
        # Password verification dialog
        verify_dialog = ctk.CTkToplevel(self.parent)
        verify_dialog.title("Verify Password")
        verify_dialog.geometry("500x350")
        verify_dialog.configure(fg_color=COLORS['background'])
        verify_dialog.grab_set()
        verify_dialog.attributes('-topmost', True)
        
        # Center
        verify_dialog.update_idletasks()
        x = (verify_dialog.winfo_screenwidth() // 2) - 250
        y = (verify_dialog.winfo_screenheight() // 2) - 175
        verify_dialog.geometry(f'500x350+{x}+{y}')
        
        content = ctk.CTkFrame(verify_dialog, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=40)
        
        ctk.CTkLabel(
            content,
            text="⚠️",
            font=("Arial", 60)
        ).pack(pady=(0, 15))
        
        ctk.CTkLabel(
            content,
            text="Enter Password to Confirm",
            font=("Arial Black", 20),
            text_color=COLORS['text']
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            content,
            text="Enter your password to permanently delete your account",
            font=("Arial", 13),
            text_color=COLORS['text_light'],
            wraplength=400
        ).pack(pady=(0, 25))
        
        password_entry = ctk.CTkEntry(
            content,
            placeholder_text="Enter your password",
            height=50,
            font=("Arial", 14),
            show="●",
            fg_color=COLORS['background']
        )
        password_entry.pack(fill="x", pady=(0, 25))
        password_entry.focus_set()
        
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=120,
            height=50,
            font=("Arial Bold", 14),
            fg_color=COLORS['text_light'],
            hover_color=COLORS['text_light'],
            command=verify_dialog.destroy
        ).pack(side="left")
        
        def confirm_delete():
            password = password_entry.get().strip()
            
            if not password:
                messagebox.showerror("Error", "Please enter your password!", parent=verify_dialog)
                return
            
            # Verify password
            if not db.verify_user(self.user['username'], password):
                messagebox.showerror("Error", "Incorrect password!", parent=verify_dialog)
                return
            
            # Delete account from database
            result = db.delete_user_account(self.user_id)
            
            if result:
                verify_dialog.destroy()
                messagebox.showinfo(
                    "Account Deleted",
                    "Your account has been permanently deleted.\n\nGoodbye!",
                    parent=self.parent
                )
                
                # Logout and return to login
                root = self.dashboard.parent
                self.dashboard.destroy()
                root.deiconify()
            else:
                messagebox.showerror("Error", "Failed to delete account!", parent=verify_dialog)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Delete Forever",
            width=180,
            height=50,
            font=("Arial Bold", 14),
            fg_color="#FF5252",
            hover_color="#E53935",
            text_color="white",
            command=confirm_delete
        ).pack(side="right")