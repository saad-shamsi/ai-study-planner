"""
Subjects Manager - Premium Aurora Theme
Add, Edit, Delete subjects with proper database integration
"""

import customtkinter as ctk
from tkinter import messagebox
from database import db
from config import COLORS


class SubjectsManager:
    """Manage subjects - Premium Aurora Theme"""
    
    def __init__(self, parent, dashboard):
        self.parent = parent
        self.dashboard = dashboard
        self.user_id = dashboard.user['user_id']
        
        # Colorful subject colors (Vibrant Palette)
        self.colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A",
            "#98D8C8", "#6C63FF", "#BB8FCE", "#85C1E2",
            "#F8B88B", "#A3E4D7", "#FF9AA2", "#C7CEEA"
        ]
        
        self.create_ui()
        self.load_subjects()
    
    def create_ui(self):
        """Create subjects interface"""
        
        # Main scrollable frame
        main_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color="transparent"
        )
        main_frame.pack(fill="both", expand=True, padx=35, pady=35)
        
        # Header with LARGE Add button
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 30))
        
        # Left: Title
        left_header = ctk.CTkFrame(header, fg_color="transparent")
        left_header.pack(side="left")
        
        ctk.CTkLabel(
            left_header,
            text="📖 My Subjects",
            font=("Segoe UI Display", 34, "bold"),
            text_color=COLORS['text']
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            left_header,
            text="Manage your subjects and organize your studies",
            font=("Segoe UI", 15),
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 0))
        
        # Right: PROMINENT Add Button
        add_btn = ctk.CTkButton(
            header,
            text="➕  Add New Subject",
            font=("Segoe UI Bold", 18),
            width=240,
            height=60,
            corner_radius=15,
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            text_color="white",
            command=self.show_add_subject_dialog
        )
        add_btn.pack(side="right", padx=20)
        
        # Info message (using card color)
        info_frame = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS['card'],
            corner_radius=12,
            border_width=1,
            border_color=COLORS['secondary']
        )
        info_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            info_frame,
            text="💡 Tip: Add subjects to start organizing your study sessions!",
            font=("Segoe UI Bold", 13),
            text_color=COLORS['primary']
        ).pack(pady=12, padx=20)
        
        # Subjects grid container
        self.subjects_container = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        self.subjects_container.pack(fill="both", expand=True)
    
    def load_subjects(self):
        """Load and display subjects"""
        print(f"[DEBUG] Loading subjects for user_id: {self.user_id}")
        
        # Clear existing
        for widget in self.subjects_container.winfo_children():
            widget.destroy()
        
        subjects = db.get_user_subjects(self.user_id)
        print(f"[DEBUG] Found {len(subjects) if subjects else 0} subjects")
        
        if not subjects:
            # Empty state
            empty_container = ctk.CTkFrame(
                self.subjects_container,
                fg_color=COLORS['card'],
                corner_radius=20,
                border_width=1,
                border_color=COLORS['border']
            )
            empty_container.pack(fill="both", expand=True, pady=20)
            
            ctk.CTkLabel(
                empty_container,
                text="📚",
                font=("Segoe UI", 100)
            ).pack(pady=(60, 20))
            
            ctk.CTkLabel(
                empty_container,
                text="No Subjects Yet",
                font=("Segoe UI Display", 28, "bold"),
                text_color=COLORS['text']
            ).pack()
            
            ctk.CTkLabel(
                empty_container,
                text="Click the 'Add New Subject' button above to get started!",
                font=("Segoe UI", 16),
                text_color=COLORS['text_light']
            ).pack(pady=(10, 30))
            
            ctk.CTkButton(
                empty_container,
                text="➕ Add Your First Subject",
                font=("Segoe UI Bold", 16),
                width=280,
                height=55,
                corner_radius=12,
                fg_color=COLORS['success'],
                hover_color="#388E3C",
                text_color="white",
                command=self.show_add_subject_dialog
            ).pack(pady=(0, 60))
            
            return
        
        # Display subjects in 3-column grid
        row = 0
        col = 0
        
        for subject in subjects:
            card = self.create_subject_card(subject)
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        # Configure grid columns
        for i in range(3):
            self.subjects_container.grid_columnconfigure(i, weight=1)
    
    def create_subject_card(self, subject):
        """Create beautiful subject card"""
        card = ctk.CTkFrame(
            self.subjects_container,
            fg_color=COLORS['card'],
            corner_radius=20,
            border_width=1,
            border_color=COLORS['border']
        )
        
        # Colored header bar
        header_bar = ctk.CTkFrame(
            card,
            height=8,
            fg_color=subject['color_code'],
            corner_radius=0
        )
        header_bar.pack(fill="x")
        
        # Icon circle
        icon_container = ctk.CTkFrame(
            card,
            fg_color=COLORS['background'], # Dark background for icon
            corner_radius=50,
            width=80,
            height=80,
            border_width=2,
            border_color=subject['color_code']
        )
        icon_container.pack(pady=(25, 15))
        icon_container.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_container,
            text="📖",
            font=("Segoe UI", 40)
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Subject name
        ctk.CTkLabel(
            card,
            text=subject['subject_name'],
            font=("Segoe UI Display", 20, "bold"),
            text_color=COLORS['text'],
            wraplength=220
        ).pack(pady=(0, 5), padx=20)
        
        # Subject code
        if subject['subject_code']:
            code_frame = ctk.CTkFrame(
                card,
                fg_color=COLORS['background'],
                corner_radius=8
            )
            code_frame.pack(pady=(5, 15))
            
            ctk.CTkLabel(
                code_frame,
                text=subject['subject_code'],
                font=("Segoe UI Bold", 12),
                text_color=subject['color_code']
            ).pack(padx=15, pady=6)
        
        # Stats
        stats_frame = ctk.CTkFrame(
            card,
            fg_color=COLORS['background'],
            corner_radius=10
        )
        stats_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkLabel(
            stats_frame,
            text="0 Sessions • 0 Hours Studied", # TODO: Real stats?
            font=("Segoe UI", 12),
            text_color=COLORS['text_light']
        ).pack(pady=10)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        ctk.CTkButton(
            btn_frame,
            text="✏️ Edit",
            font=("Segoe UI Bold", 13),
            width=100,
            height=40,
            corner_radius=10,
            fg_color=COLORS['info'],
            hover_color=COLORS['primary'],
            text_color="white",
            command=lambda s=subject: self.show_edit_subject_dialog(s)
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Delete",
            font=("Segoe UI Bold", 13),
            width=100,
            height=40,
            corner_radius=10,
            fg_color="#EF4444", # Red
            hover_color="#DC2626",
            text_color="white",
            command=lambda s=subject: self.delete_subject(s)
        ).pack(side="right", padx=(5, 0))
        
        return card
    
    def show_add_subject_dialog(self):
        """Show add subject dialog - Dark Theme"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Add New Subject")
        dialog.geometry("600x600")
        dialog.resizable(False, False)
        dialog.configure(fg_color=COLORS['background'])
        
        # Make it stay on top
        dialog.attributes('-topmost', True)
        dialog.grab_set()
        dialog.focus_force()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 300
        y = (dialog.winfo_screenheight() // 2) - 300
        dialog.geometry(f'600x600+{x}+{y}')
        
        # Content
        content = ctk.CTkFrame(dialog, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Title
        ctk.CTkLabel(
            content,
            text="➕ Add New Subject",
            font=("Segoe UI Display", 28, "bold"),
            text_color=COLORS['text']
        ).pack(pady=(0, 30))
        
        # Subject name
        ctk.CTkLabel(
            content,
            text="Subject Name *",
            font=("Segoe UI Bold", 14),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        name_entry = ctk.CTkEntry(
            content,
            placeholder_text="e.g., Mathematics, Physics, History",
            height=55,
            font=("Segoe UI", 15),
            fg_color=COLORS['card'],
            border_width=1,
            border_color=COLORS['border'],
            text_color=COLORS['text']
        )
        name_entry.pack(fill="x", pady=(0, 20))
        name_entry.focus_set()
        
        # Subject code
        ctk.CTkLabel(
            content,
            text="Subject Code (Optional)",
            font=("Segoe UI Bold", 14),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        code_entry = ctk.CTkEntry(
            content,
            placeholder_text="e.g., MATH101, PHY201",
            height=55,
            font=("Segoe UI", 15),
            fg_color=COLORS['card'],
            border_width=1,
            border_color=COLORS['border'],
            text_color=COLORS['text']
        )
        code_entry.pack(fill="x", pady=(0, 25))
        
        # Color picker
        ctk.CTkLabel(
            content,
            text="Choose a Color",
            font=("Segoe UI Bold", 14),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 15))
        
        color_frame = ctk.CTkFrame(content, fg_color="transparent")
        color_frame.pack(fill="x", pady=(0, 30))
        
        selected_color = {"value": self.colors[0]}
        
        def select_color(color):
            selected_color["value"] = color
            for btn in color_buttons:
                if btn.cget("fg_color") == color:
                    btn.configure(border_width=4, border_color=COLORS['text'])
                else:
                    btn.configure(border_width=0)
        
        color_buttons = []
        for i, color in enumerate(self.colors):
            btn = ctk.CTkButton(
                color_frame,
                text="",
                width=55,
                height=55,
                corner_radius=12,
                fg_color=color,
                hover_color=color,
                border_width=4 if i == 0 else 0,
                border_color=COLORS['text'] if i == 0 else None,
                command=lambda c=color: select_color(c)
            )
            btn.grid(row=i//6, column=i%6, padx=5, pady=5)
            color_buttons.append(btn)
        
        # Buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(15, 0))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=140,
            height=50,
            font=("Segoe UI Bold", 15),
            fg_color=COLORS['card'],
            hover_color=COLORS['hover'],
            text_color=COLORS['text'],
            command=dialog.destroy
        ).pack(side="left")
        
        def save_subject():
            name = name_entry.get().strip()
            code = code_entry.get().strip()
            
            if not name:
                messagebox.showerror(
                    "Validation Error",
                    "Please enter subject name!",
                    parent=dialog
                )
                return
            
            # Save to database
            try:
                result = db.add_subject(
                    self.user_id,
                    name,
                    code if code else None,
                    selected_color["value"]
                )
                
                if result:
                    messagebox.showinfo(
                        "Success! 🎉",
                        f"Subject '{name}' added successfully!",
                        parent=dialog
                    )
                    dialog.destroy()
                    self.load_subjects()
                    self.dashboard.refresh_data()
                else:
                    messagebox.showerror(
                        "Database Error",
                        "Failed to add subject. Please try again.",
                        parent=dialog
                    )
            except Exception as e:
                print(f"[ERROR] Exception: {e}")
                messagebox.showerror(
                    "Error",
                    f"An error occurred: {str(e)}",
                    parent=dialog
                )
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="➕ Add Subject",
            width=200,
            height=50,
            font=("Segoe UI Bold", 15),
            fg_color=COLORS['success'],
            hover_color="#388E3C",
            text_color="white",
            command=save_subject
        )
        save_btn.pack(side="right")
        
        # Bind Enter key
        dialog.bind('<Return>', lambda e: save_subject())
    
    def show_edit_subject_dialog(self, subject):
        """Show edit subject dialog - Dark Theme"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Edit Subject")
        dialog.geometry("600x600")
        dialog.resizable(False, False)
        dialog.configure(fg_color=COLORS['background'])
        dialog.attributes('-topmost', True)
        dialog.grab_set()
        
        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 300
        y = (dialog.winfo_screenheight() // 2) - 300
        dialog.geometry(f'600x600+{x}+{y}')
        
        content = ctk.CTkFrame(dialog, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=40)
        
        ctk.CTkLabel(
            content,
            text="✏️ Edit Subject",
            font=("Segoe UI Display", 28, "bold"),
            text_color=COLORS['text']
        ).pack(pady=(0, 30))
        
        ctk.CTkLabel(
            content,
            text="Subject Name *",
            font=("Segoe UI Bold", 14),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        name_entry = ctk.CTkEntry(
            content,
            height=55,
            font=("Segoe UI", 15),
            fg_color=COLORS['card'],
            border_width=1,
            border_color=COLORS['border'],
            text_color=COLORS['text']
        )
        name_entry.insert(0, subject['subject_name'])
        name_entry.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            content,
            text="Subject Code (Optional)",
            font=("Segoe UI Bold", 14),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        code_entry = ctk.CTkEntry(
            content,
            height=55,
            font=("Segoe UI", 15),
            fg_color=COLORS['card'],
            border_width=1,
            border_color=COLORS['border'],
            text_color=COLORS['text']
        )
        if subject['subject_code']:
            code_entry.insert(0, subject['subject_code'])
        code_entry.pack(fill="x", pady=(0, 25))
        
        ctk.CTkLabel(
            content,
            text="Choose a Color",
            font=("Segoe UI Bold", 14),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 15))
        
        color_frame = ctk.CTkFrame(content, fg_color="transparent")
        color_frame.pack(fill="x", pady=(0, 30))
        
        selected_color = {"value": subject['color_code']}
        
        def select_color(color):
            selected_color["value"] = color
            for btn in color_buttons:
                if btn.cget("fg_color") == color:
                    btn.configure(border_width=4, border_color=COLORS['text'])
                else:
                    btn.configure(border_width=0)
        
        color_buttons = []
        for i, color in enumerate(self.colors):
            btn = ctk.CTkButton(
                color_frame,
                text="",
                width=55,
                height=55,
                corner_radius=12,
                fg_color=color,
                hover_color=color,
                border_width=4 if color == subject['color_code'] else 0,
                border_color=COLORS['text'] if color == subject['color_code'] else None,
                command=lambda c=color: select_color(c)
            )
            btn.grid(row=i//6, column=i%6, padx=5, pady=5)
            color_buttons.append(btn)
        
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(15, 0))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=140,
            height=50,
            font=("Segoe UI Bold", 15),
            fg_color=COLORS['card'],
            hover_color=COLORS['hover'],
            text_color=COLORS['text'],
            command=dialog.destroy
        ).pack(side="left")
        
        def update_subject():
            name = name_entry.get().strip()
            code = code_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Please enter subject name!", parent=dialog)
                return
            
            result = db.update_subject(
                subject['subject_id'],
                name,
                code if code else None,
                selected_color["value"]
            )
            
            if result:
                messagebox.showinfo("Success", "Subject updated!", parent=dialog)
                dialog.destroy()
                self.load_subjects()
                self.dashboard.refresh_data()
            else:
                messagebox.showerror("Error", "Failed to update!", parent=dialog)
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Update Subject",
            width=200,
            height=50,
            font=("Segoe UI Bold", 15),
            fg_color=COLORS['info'],
            hover_color="#1976D2",
            text_color="white",
            command=update_subject
        ).pack(side="right")
    
    def delete_subject(self, subject):
        """Delete subject"""
        response = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{subject['subject_name']}'?\n\nThis will also delete all related study sessions!",
            parent=self.parent
        )
        
        if response:
            result = db.delete_subject(subject['subject_id'])
            if result:
                messagebox.showinfo("Success", "Subject deleted successfully!")
                self.load_subjects()
                self.dashboard.refresh_data()
            else:
                messagebox.showerror("Error", "Failed to delete subject!")