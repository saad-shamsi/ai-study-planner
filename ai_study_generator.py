"""
AI Study Plan Generator - Powered by Groq
Premium Aurora Theme
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from database import db
from config import COLORS
from groq_service import groq_ai
from markdown_utils import MarkdownParser # Import Markdown Parser
import threading


class StudyPlanGenerator(ctk.CTkToplevel):
    """AI-powered study plan generator - Premium Edition"""
    
    def __init__(self, parent, dashboard):
        super().__init__(parent)
        
        self.dashboard = dashboard
        self.user_id = dashboard.user['user_id']
        
        # Window setup
        self.title("AI Study Plan Generator")
        self.geometry("900x750")
        self.configure(fg_color=COLORS['background'])
        self.grab_set()
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 450
        y = (self.winfo_screenheight() // 2) - 375
        self.geometry(f'900x750+{x}+{y}')
        
        self.create_ui()
    
    def create_ui(self):
        """Create generator UI"""
        
        # Main container
        main_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Header
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(
            header_frame,
            text="AI Study Plan Generator",
            font=("Segoe UI Display", 28, "bold"),
            text_color=COLORS['text']
        ).pack()
        
        ctk.CTkLabel(
            header_frame,
            text="Get a personalized study schedule powered by AI",
            font=("Segoe UI", 14),
            text_color=COLORS['text_light']
        ).pack()
        
        # Form section
        form_card = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS['card'],
            corner_radius=15,
            border_width=1,
            border_color=COLORS['border']
        )
        form_card.pack(fill="x", pady=(0, 20))
        
        form_content = ctk.CTkFrame(form_card, fg_color="transparent")
        form_content.pack(padx=30, pady=30)
        
        # Select subjects
        ctk.CTkLabel(
            form_content,
            text="📚 Select Subjects",
            font=("Segoe UI Bold", 16),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(0, 15))
        
        subjects = db.get_user_subjects(self.user_id) or []
        
        if not subjects:
            ctk.CTkLabel(
                form_content,
                text="⚠️ No subjects found. Please add subjects first!",
                font=("Segoe UI", 13),
                text_color=COLORS['warning']
            ).pack(pady=20)
            
            ctk.CTkButton(
                form_content,
                text="Go to Subjects",
                fg_color=COLORS['primary'],
                text_color=COLORS['background'],
                command=self.destroy
            ).pack()
            return
        
        # Subject checkboxes
        self.subject_vars = {}
        subjects_grid = ctk.CTkFrame(form_content, fg_color="transparent")
        subjects_grid.pack(fill="x", pady=(0, 20))
        
        for i, subject in enumerate(subjects):
            var = ctk.BooleanVar(value=True)
            self.subject_vars[subject['subject_name']] = var
            
            # Using colored checkbox logic if suitable, or standard theme
            checkbox = ctk.CTkCheckBox(
                subjects_grid,
                text=subject['subject_name'],
                variable=var,
                font=("Segoe UI", 13),
                fg_color=COLORS['primary'],
                hover_color=COLORS['secondary'],
                border_color=COLORS['text_light'],
                text_color=COLORS['text']
            )
            checkbox.grid(row=i//3, column=i%3, padx=10, pady=5, sticky="w")
        
        # Study hours per day
        ctk.CTkLabel(
            form_content,
            text="⏰ Study Hours Per Day",
            font=("Segoe UI Bold", 16),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(20, 10))
        
        self.hours_slider = ctk.CTkSlider(
            form_content,
            from_=1,
            to=8,
            number_of_steps=7,
            width=400,
            button_color=COLORS['primary'],
            progress_color=COLORS['primary']
        )
        self.hours_slider.set(3)
        self.hours_slider.pack(pady=(0, 5))
        
        self.hours_label = ctk.CTkLabel(
            form_content,
            text="3 hours per day",
            font=("Segoe UI Bold", 14),
            text_color=COLORS['primary']
        )
        self.hours_label.pack()
        
        self.hours_slider.configure(command=self.update_hours_label)
        
        # Exam/Target date
        ctk.CTkLabel(
            form_content,
            text="📅 Target/Exam Date (Optional)",
            font=("Segoe UI Bold", 16),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(20, 10))
        
        self.date_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="YYYY-MM-DD",
            height=45,
            font=("Segoe UI", 13),
            fg_color=COLORS['background'],
            border_color=COLORS['border'],
            text_color=COLORS['text']
        )
        self.date_entry.pack(fill="x")
        
        # Current level
        ctk.CTkLabel(
            form_content,
            text="📊 Your Current Level",
            font=("Segoe UI Bold", 16),
            text_color=COLORS['text'],
            anchor="w"
        ).pack(fill="x", pady=(20, 10))
        
        self.level_var = ctk.StringVar(value="intermediate")
        
        level_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        level_frame.pack(fill="x")
        
        levels = [
            ("🌱 Beginner", "beginner"),
            ("📚 Intermediate", "intermediate"),
            ("🎓 Advanced", "advanced")
        ]
        
        for text, value in levels:
            ctk.CTkRadioButton(
                level_frame,
                text=text,
                variable=self.level_var,
                value=value,
                font=("Segoe UI", 13),
                fg_color=COLORS['primary'],
                hover_color=COLORS['primary'],
                text_color=COLORS['text']
            ).pack(side="left", padx=10)
        
        # Generate button
        self.generate_btn = ctk.CTkButton(
            main_frame,
            text="✨ Generate AI Plan",
            font=("Segoe UI Bold", 16),
            height=55,
            width=300,
            corner_radius=12,
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            text_color=COLORS['background'],
            command=self.generate_plan
        )
        self.generate_btn.pack(fill="x", pady=(0, 20), padx=20)
        
        # Status Label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=("Segoe UI", 14),
            text_color=COLORS['text_light']
        )
        self.status_label.pack(pady=10)
    
    def update_hours_label(self, value):
        """Update hours label"""
        hours = int(float(value))
        self.hours_label.configure(text=f"{hours} hours per day")
    
    def generate_plan(self):
        """Generate AI study plan"""
        
        # Get selected subjects
        selected_subjects = [
            name for name, var in self.subject_vars.items() if var.get()
        ]
        
        if not selected_subjects:
            messagebox.showerror(
                "No Subjects",
                "Please select at least one subject!",
                parent=self
            )
            return
        
        # Get parameters
        hours = int(self.hours_slider.get())
        target_date = self.date_entry.get().strip() or "Not specified"
        level = self.level_var.get()
        
        # Disable button
        self.generate_btn.configure(
            state="disabled",
            text="🤖 Generating with AI..."
        )
        self.status_label.configure(text="⏳ Creating your personalized plan...")
        
        # Generate in thread
        def generate():
            plan = groq_ai.generate_study_plan(
                subjects=selected_subjects,
                study_hours_per_day=hours,
                exam_date=target_date,
                current_level=level
            )
            
            # Update UI in main thread
            self.after(0, lambda: self.open_plan_result_window(plan))
            self.after(0, lambda: self.generate_btn.configure(
                state="normal",
                text="✨ Generate AI Plan"
            ))
            self.after(0, lambda: self.status_label.configure(text=""))
        
        threading.Thread(target=generate, daemon=True).start()
    
    def open_plan_result_window(self, plan):
        """Open the result in a NEW window"""
        self.destroy() # Close the generator form
        result_window = PlanResultWindow(self.dashboard, plan)

class PlanResultWindow(ctk.CTkToplevel):
    """Window to display the generated plan cleanly with Markdown"""
    
    def __init__(self, dashboard, plan_text):
        super().__init__()
        self.dashboard = dashboard
        self.plan_text = plan_text
        self.user_id = dashboard.user['user_id']
        
        # Window setup
        self.title("Your AI Study Plan")
        self.geometry("900x800")
        self.configure(fg_color=COLORS['background'])
        self.grab_set()
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 450
        y = (self.winfo_screenheight() // 2) - 400
        self.geometry(f'900x800+{x}+{y}')
        
        self.create_ui()
        
    def create_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=COLORS['primary'], corner_radius=0)
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="✅ Your Personalized Study Plan",
            font=("Segoe UI Display", 22, "bold"),
            text_color=COLORS['background']
        ).pack(pady=20)

        # Content Area 
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.text_area = ctk.CTkTextbox(
            content_frame,
            font=("Segoe UI", 14),
            wrap="word",
            fg_color=COLORS['card'],
            text_color=COLORS['text'],
            border_width=1,
            border_color=COLORS['border'],
            corner_radius=15
        )
        self.text_area.pack(fill="both", expand=True)
        
        # Render Markdown
        parser = MarkdownParser(self.text_area)
        parser.parse_and_insert(self.plan_text)
        
        self.text_area.configure(state="disabled") # Read-only
        
        # Action Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Generate New
        ctk.CTkButton(
            btn_frame,
            text="🔄 New Plan",
            font=("Segoe UI Bold", 14),
            height=45,
            width=160,
            corner_radius=10,
            fg_color=COLORS['secondary'],
            hover_color=COLORS['primary'],
            text_color=COLORS['background'],
            command=self.generate_new
        ).pack(side="left", padx=5)
        
        # Copy
        ctk.CTkButton(
            btn_frame,
            text="📋 Copy",
            font=("Segoe UI Bold", 14),
            height=45,
            width=120,
            corner_radius=10,
            fg_color=COLORS['card'],
            hover_color=COLORS['hover'],
            text_color=COLORS['text'],
            command=self.copy_plan
        ).pack(side="left", padx=5)
        
        # Save Plan
        ctk.CTkButton(
            btn_frame,
            text="💾 Save",
            font=("Segoe UI Bold", 14),
            height=45,
            width=120,
            corner_radius=10,
            fg_color=COLORS['card'],
            hover_color=COLORS['hover'],
            text_color=COLORS['text'],
            command=self.save_plan
        ).pack(side="left", padx=5)
        
        # Done
        ctk.CTkButton(
            btn_frame,
            text="✅ Done",
            font=("Segoe UI Bold", 14),
            height=45,
            width=120,
            corner_radius=10,
            fg_color=COLORS['success'],
            hover_color='#10B981', # Slightly darker Emerald
            text_color=COLORS['background'],
            command=self.destroy
        ).pack(side="right", padx=5)

    def generate_new(self):
        self.destroy()
        from ai_study_generator import StudyPlanGenerator
        StudyPlanGenerator(self.master, self.dashboard)

    def copy_plan(self):
        self.clipboard_clear()
        self.clipboard_append(self.plan_text)
        messagebox.showinfo("Copied", "Plan copied to clipboard!", parent=self)

    def save_plan(self):
        try:
            db.save_ai_plan(self.user_id, self.plan_text)
            messagebox.showinfo("Saved", "Study plan saved successfully!\nYou can view it in Saved Plans.", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save plan: {e}", parent=self)