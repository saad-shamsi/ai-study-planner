"""
Saved Plans View - View history of AI Generated Plans
"""

import customtkinter as ctk
from tkinter import messagebox
from database import db
from config import COLORS

class SavedPlansView(ctk.CTkToplevel):
    """Window to view saved study plans"""
    
    def __init__(self, parent, dashboard):
        super().__init__(parent)
        self.dashboard = dashboard
        self.user_id = dashboard.user['user_id']
        
        # Window setup
        self.title("Saved Study Plans")
        self.geometry("900x700")
        self.configure(fg_color="white")
        
        # Make this window modal (focus stays here)
        self.attributes('-topmost', True)
        self.grab_set()
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 450
        y = (self.winfo_screenheight() // 2) - 350
        self.geometry(f'900x700+{x}+{y}')
        
        self.create_ui()
        self.load_plans()
        
    def create_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=COLORS['secondary'], corner_radius=0)
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="💾 Your Saved Study Plans",
            font=("Arial Black", 22),
            text_color="white"
        ).pack(pady=20)
        
        # Main Content Scrollable
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
    def load_plans(self):
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        plans = db.get_saved_ai_plans(self.user_id)
        
        if not plans:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No saved plans yet.",
                font=("Arial", 16),
                text_color=COLORS['text_light']
            ).pack(pady=50)
            return
            
        for plan in plans:
            self.create_plan_card(plan)
            
    def create_plan_card(self, plan):
        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=COLORS['background'],
            corner_radius=15
        )
        card.pack(fill="x", pady=10)
        
        # Header of card (Date)
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=10)
        
        date_str = plan['created_at'].strftime("%B %d, %Y - %I:%M %p")
        
        ctk.CTkLabel(
            header_frame,
            text=f"📅 Generated on: {date_str}",
            font=("Arial Bold", 14),
            text_color=COLORS['text']
        ).pack(side="left")
        
        # Preview Text
        preview_text = plan['plan_content'][:150].replace('\n', ' ') + "..."
        
        ctk.CTkLabel(
            card,
            text=preview_text,
            font=("Arial", 12),
            text_color=COLORS['text_light'],
            anchor="w",
            wraplength=800
        ).pack(fill="x", padx=15, pady=(0, 10))
        
        # Actions
        action_frame = ctk.CTkFrame(card, fg_color="transparent")
        action_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # View
        ctk.CTkButton(
            action_frame,
            text="👁️ View Full Plan",
            font=("Arial Bold", 12),
            height=35,
            width=120,
            fg_color=COLORS['primary'],
            command=lambda: self.view_full_plan(plan['plan_content'])
        ).pack(side="left", padx=5)
        
        # Edit (NEW)
        ctk.CTkButton(
            action_frame,
            text="✏️ Edit",
            font=("Arial Bold", 12),
            height=35,
            width=80,
            fg_color=COLORS['warning'],
            hover_color="#F57C00",
            command=lambda: self.edit_plan(plan)
        ).pack(side="left", padx=5)
        
        # Copy
        ctk.CTkButton(
            action_frame,
            text="📋 Copy",
            font=("Arial Bold", 12),
            height=35,
            width=80,
            fg_color=COLORS['info'],
            command=lambda: self.copy_text(plan['plan_content'])
        ).pack(side="left", padx=5)
        
        # Delete
        ctk.CTkButton(
            action_frame,
            text="🗑️ Delete",
            font=("Arial Bold", 12),
            height=35,
            width=80,
            fg_color="#FF5252",
            hover_color="#E53935",
            command=lambda: self.delete_plan(plan['plan_id'])
        ).pack(side="left", padx=5)

    def delete_plan(self, plan_id):
        confirm = messagebox.askyesno("Delete Plan", "Are you sure you want to delete this study plan?", parent=self)
        if confirm:
            result = db.delete_saved_plan(plan_id)
            if result:
                messagebox.showinfo("Success", "Plan deleted successfully.", parent=self)
                self.load_plans()
            else:
                messagebox.showerror("Error", "Failed to delete plan.", parent=self)

    def edit_plan(self, plan):
        """Open a window to edit the plan"""
        # Create persistent window reference
        self.editor = ctk.CTkToplevel(self)
        self.editor.title("Edit Study Plan")
        self.editor.geometry("900x800")
        self.editor.configure(fg_color="white")
        self.editor.attributes('-topmost', True)
        self.editor.grab_set()
        
        # Center
        self.editor.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 450
        y = (self.winfo_screenheight() // 2) - 400
        self.editor.geometry(f'900x800+{x}+{y}')
        
        # Title
        ctk.CTkLabel(
            self.editor,
            text="✏️ Edit Your Plan",
            font=("Arial Black", 20),
            text_color=COLORS['text']
        ).pack(pady=20)
        
        # Text Editor
        text_editor = ctk.CTkTextbox(self.editor, font=("Arial", 14), wrap="word")
        text_editor.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        text_editor.insert("1.0", plan['plan_content'])
        
        # Save Button
        def save_changes():
            new_content = text_editor.get("1.0", "end").strip()
            if not new_content:
                messagebox.showwarning("Empty", "Plan cannot be empty!", parent=self.editor)
                return
            
            db.update_saved_plan(plan['plan_id'], new_content)
            messagebox.showinfo("Success", "Plan updated successfully!", parent=self.editor)
            self.editor.destroy()
            self.load_plans()
            
        ctk.CTkButton(
            self.editor,
            text="💾 Save Changes",
            font=("Arial Bold", 16),
            height=50,
            fg_color=COLORS['success'],
            hover_color="#388E3C",
            command=save_changes
        ).pack(fill="x", padx=20, pady=20)

    def view_full_plan(self, text):
        # Close existing viewer if open
        if hasattr(self, 'viewer') and self.viewer.winfo_exists():
            self.viewer.destroy()

        # Open a detail viewer (Use self.viewer to prevent garbage collection)
        self.viewer = ctk.CTkToplevel(self)
        self.viewer.title("View Plan")
        self.viewer.geometry("800x600")
        self.viewer.configure(fg_color="white")
        
        # Keep on top
        self.viewer.attributes('-topmost', True)
        self.viewer.grab_set()
        
        # Center
        self.viewer.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 400
        y = (self.winfo_screenheight() // 2) - 300
        self.viewer.geometry(f'800x600+{x}+{y}')
        
        txt = ctk.CTkTextbox(self.viewer, font=("Arial", 14), wrap="word")
        txt.pack(fill="both", expand=True, padx=20, pady=20)
        txt.insert("1.0", text)
        txt.configure(state="disabled")
        
    def copy_text(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Copied", "Plan copied to clipboard!", parent=self)