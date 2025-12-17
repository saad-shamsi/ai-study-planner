"""
Study Planner - Premium Aurora Theme
Fullscreen enabled, Time Picker enabled, Calendar/Visibility changes reverted.
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date, timedelta
from database import db
from config import COLORS

# ==================== CUSTOM DIALOGS ====================

class TimePickerDialog(ctk.CTkToplevel):
    """A custom dialog to pick time (HH:MM AM/PM) - Dark Theme"""
    def __init__(self, parent, title="Select Time", initial_time="12:00 PM", callback=None):
        super().__init__(parent)
        self.callback = callback
        self.title(title)
        self.geometry("340x250")
        self.resizable(False, False)
        
        # Ensure it stays on top
        self.attributes('-topmost', True)
        self.lift()
        self.focus_force()
        self.grab_set()
        
        # Center the window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 170
        y = (self.winfo_screenheight() // 2) - 125
        self.geometry(f"+{x}+{y}")
        self.configure(fg_color=COLORS['background'])

        # Parse initial time
        h_val, m_val, p_val = "12", "00", "PM"
        if initial_time and ":" in initial_time:
            try:
                dt = datetime.strptime(initial_time, "%I:%M %p")
                h_val, m_val, p_val = dt.strftime("%I"), dt.strftime("%M"), dt.strftime("%p")
            except ValueError:
                pass

        # Title
        ctk.CTkLabel(self, text=title, font=("Segoe UI Display", 18, "bold"), text_color=COLORS['text']).pack(pady=20)

        # Time Selection Frame
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=10)

        # Hours
        self.hour_var = ctk.StringVar(value=h_val)
        hours = [f"{i:02d}" for i in range(1, 13)]
        self.hour_menu = ctk.CTkOptionMenu(
            frame, values=hours, variable=self.hour_var, 
            width=70, height=40, font=("Segoe UI", 16),
            fg_color=COLORS['primary'], button_color=COLORS['primary'], text_color="white"
        )
        self.hour_menu.pack(side="left", padx=2)

        ctk.CTkLabel(frame, text=":", font=("Segoe UI", 20), text_color=COLORS['text']).pack(side="left", padx=2)

        # Minutes
        self.minute_var = ctk.StringVar(value=m_val)
        minutes = [f"{i:02d}" for i in range(0, 60, 5)]
        self.minute_menu = ctk.CTkOptionMenu(
            frame, values=minutes, variable=self.minute_var, 
            width=70, height=40, font=("Segoe UI", 16),
            fg_color=COLORS['primary'], button_color=COLORS['primary'], text_color="white"
        )
        self.minute_menu.pack(side="left", padx=2)

        # AM/PM
        self.period_var = ctk.StringVar(value=p_val)
        periods = ["AM", "PM"]
        self.period_menu = ctk.CTkOptionMenu(
            frame, values=periods, variable=self.period_var, 
            width=70, height=40, font=("Segoe UI", 16),
            fg_color=COLORS['secondary'], button_color=COLORS['secondary'], text_color="white"
        )
        self.period_menu.pack(side="left", padx=(10, 2))

        # Confirm Button
        ctk.CTkButton(
            self, text="Confirm", font=("Segoe UI Bold", 14),
            fg_color=COLORS['success'], hover_color="#388E3C",
            text_color="white",
            command=self.confirm
        ).pack(pady=20)

    def confirm(self):
        time_str = f"{self.hour_var.get()}:{self.minute_var.get()} {self.period_var.get()}"
        if self.callback:
            self.callback(time_str)
        self.destroy()


# ==================== MAIN CLASS ====================

class StudyPlanner:
    """Study planner with Premium Aurora Theme"""
    
    def __init__(self, parent, dashboard):
        self.parent = parent
        self.dashboard = dashboard
        self.user_id = dashboard.user['user_id']
        self.current_filter = "all"
        self.create_ui()
    
    def create_ui(self):
        """Create planner interface"""
        # Main container
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=35, pady=35)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 25))
        
        left_header = ctk.CTkFrame(header, fg_color="transparent")
        left_header.pack(side="left")
        ctk.CTkLabel(left_header, text="📅 Study Planner", font=("Segoe UI Display", 34, "bold"), text_color=COLORS['text']).pack(anchor="w")
        ctk.CTkLabel(left_header, text="Track your study sessions and manage your time", font=("Segoe UI", 15), text_color=COLORS['text_light']).pack(anchor="w", pady=(5, 0))
        
        # Add Session Button
        ctk.CTkButton(
            header, text="➕  Add Study Session", font=("Segoe UI Bold", 16),
            width=220, height=55, corner_radius=15,
            fg_color=COLORS['success'], hover_color="#388E3C", text_color="white",
            command=self.show_add_session_dialog
        ).pack(side="right", padx=20)
        
        # Sessions Card
        sessions_card = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS['card'],
            corner_radius=20,
            border_width=1,
            border_color=COLORS['border']
        )
        sessions_card.grid(row=1, column=0, sticky="nsew", padx=(0, 15))
        
        card_header = ctk.CTkFrame(sessions_card, fg_color="transparent")
        card_header.pack(fill="x", padx=25, pady=(25, 20))
        ctk.CTkLabel(card_header, text="📝 Study Sessions", font=("Segoe UI Display", 20, "bold"), text_color=COLORS['text']).pack(side="left")
        
        # Filter Buttons
        filter_frame = ctk.CTkFrame(card_header, fg_color="transparent")
        filter_frame.pack(side="right")
        
        self.btn_all = ctk.CTkButton(
            filter_frame, text="All", font=("Segoe UI Bold", 12), width=70, height=35, corner_radius=10,
            fg_color=COLORS['primary'], text_color="white", command=lambda: self.set_filter("all")
        )
        self.btn_all.pack(side="left", padx=3)
        
        self.btn_today = ctk.CTkButton(
            filter_frame, text="Today", font=("Segoe UI Bold", 12), width=70, height=35, corner_radius=10,
            fg_color=COLORS['background'], text_color=COLORS['text'], command=lambda: self.set_filter("today")
        )
        self.btn_today.pack(side="left", padx=3)
        
        self.btn_week = ctk.CTkButton(
            filter_frame, text="Week", font=("Segoe UI Bold", 12), width=70, height=35, corner_radius=10,
            fg_color=COLORS['background'], text_color=COLORS['text'], command=lambda: self.set_filter("week")
        )
        self.btn_week.pack(side="left", padx=3)
        
        # List
        self.sessions_list = ctk.CTkScrollableFrame(sessions_card, fg_color="transparent")
        self.sessions_list.pack(fill="both", expand=True, padx=25, pady=(0, 25))
        self.load_sessions()
        
        # Right Column (Stats)
        right_column = ctk.CTkFrame(main_frame, fg_color="transparent")
        right_column.grid(row=1, column=1, sticky="nsew")
        
        stats_card = ctk.CTkFrame(
            right_column,
            fg_color=COLORS['card'],
            corner_radius=20,
            border_width=1,
            border_color=COLORS['border']
        )
        stats_card.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(stats_card, text="📊 This Week", font=("Segoe UI Display", 18, "bold"), text_color=COLORS['text']).pack(pady=(25, 20), padx=25, anchor="w")
        
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        week_sessions = db.get_sessions_by_date_range(self.user_id, week_start, week_end) or []
        total_time = sum(s['duration_minutes'] for s in week_sessions)
        
        week_stats = [
            ("📚", "Sessions", len(week_sessions), COLORS['info']),
            ("⏱️", "Total Time", f"{total_time // 60}h {total_time % 60}m", COLORS['success']),
            ("📈", "Avg/Day", f"{total_time // 7}m", COLORS['warning']),
        ]
        
        for icon, label, value, color in week_stats:
            stat_row = ctk.CTkFrame(stats_card, fg_color=COLORS['background'], corner_radius=12)
            stat_row.pack(fill="x", padx=25, pady=5)
            content = ctk.CTkFrame(stat_row, fg_color="transparent")
            content.pack(fill="x", padx=15, pady=12)
            icon_bg = ctk.CTkFrame(content, fg_color=color, corner_radius=10, width=45, height=45)
            icon_bg.pack(side="left")
            icon_bg.pack_propagate(False)
            ctk.CTkLabel(icon_bg, text=icon, font=("Segoe UI", 22)).place(relx=0.5, rely=0.5, anchor="center")
            text_frame = ctk.CTkFrame(content, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True, padx=15)
            ctk.CTkLabel(text_frame, text=label, font=("Segoe UI", 12), text_color=COLORS['text_light'], anchor="w").pack(anchor="w")
            ctk.CTkLabel(text_frame, text=str(value), font=("Segoe UI Bold", 18), text_color=COLORS['text'], anchor="w").pack(anchor="w")
        
        ctk.CTkFrame(stats_card, fg_color="transparent", height=15).pack()
        
        motivation_card = ctk.CTkFrame(right_column, fg_color=COLORS['success'], corner_radius=20)
        motivation_card.pack(fill="x")
        ctk.CTkLabel(motivation_card, text="🎯", font=("Segoe UI", 50)).pack(pady=(25, 15))
        ctk.CTkLabel(motivation_card, text="Keep Going!", font=("Segoe UI Display", 20, "bold"), text_color="white").pack()
        ctk.CTkLabel(motivation_card, text="Every study session\nbrings you closer to your goals!", font=("Segoe UI", 14), text_color="white", justify="center").pack(pady=(10, 25))

    def set_filter(self, filter_type):
        self.current_filter = filter_type
        self.update_filter_buttons()
        self.load_sessions()

    def update_filter_buttons(self):
        default_fg = COLORS['background']
        default_text = COLORS['text']
        self.btn_all.configure(fg_color=default_fg, text_color=default_text)
        self.btn_today.configure(fg_color=default_fg, text_color=default_text)
        self.btn_week.configure(fg_color=default_fg, text_color=default_text)
        
        if self.current_filter == 'all':
            self.btn_all.configure(fg_color=COLORS['primary'], text_color="white")
        elif self.current_filter == 'today':
            self.btn_today.configure(fg_color=COLORS['primary'], text_color="white")
        elif self.current_filter == 'week':
            self.btn_week.configure(fg_color=COLORS['primary'], text_color="white")

    def load_sessions(self):
        for widget in self.sessions_list.winfo_children():
            widget.destroy()
        
        all_sessions = db.get_user_sessions(self.user_id, limit=100)
        sessions = []
        if all_sessions:
            if self.current_filter == 'all':
                sessions = all_sessions
            elif self.current_filter == 'today':
                sessions = [s for s in all_sessions if s['session_date'] == date.today()]
            elif self.current_filter == 'week':
                today = date.today()
                start_week = today - timedelta(days=today.weekday())
                end_week = start_week + timedelta(days=6)
                sessions = [s for s in all_sessions if start_week <= s['session_date'] <= end_week]
        
        if not sessions:
            empty_frame = ctk.CTkFrame(self.sessions_list, fg_color=COLORS['background'], corner_radius=15, border_width=1, border_color=COLORS['border'])
            empty_frame.pack(fill="both", expand=True, pady=50)
            ctk.CTkLabel(empty_frame, text="📝", font=("Segoe UI", 80)).pack(pady=(40, 20))
            ctk.CTkLabel(empty_frame, text="No Study Sessions Found", font=("Segoe UI Display", 22, "bold"), text_color=COLORS['text']).pack()
            ctk.CTkLabel(empty_frame, text="Change the filter or add a new session!", font=("Segoe UI", 14), text_color=COLORS['text_light']).pack(pady=(10, 40))
            return
        
        current_date = None
        for session in sessions:
            session_date = session['session_date']
            if current_date != session_date:
                current_date = session_date
                date_frame = ctk.CTkFrame(self.sessions_list, fg_color="transparent")
                date_frame.pack(fill="x", pady=(15, 10))
                date_text = "Today" if session_date == date.today() else "Yesterday" if session_date == date.today() - timedelta(days=1) else session_date.strftime("%B %d, %Y")
                ctk.CTkLabel(date_frame, text=date_text, font=("Segoe UI Bold", 14), text_color=COLORS['text']).pack(side="left")
            
            session_card = ctk.CTkFrame(self.sessions_list, fg_color=COLORS['background'], corner_radius=12, border_width=1, border_color=COLORS['border'])
            session_card.pack(fill="x", pady=5)
            ctk.CTkFrame(session_card, width=5, fg_color=session['color_code']).pack(side="left", fill="y")
            content = ctk.CTkFrame(session_card, fg_color="transparent")
            content.pack(side="left", fill="both", expand=True, padx=15, pady=12)
            ctk.CTkLabel(content, text=session['subject_name'], font=("Segoe UI Bold", 15), text_color=COLORS['text'], anchor="w").pack(anchor="w")
            time_info = f"{session['start_time']} - {session['end_time']}" if session['start_time'] else "Time not recorded"
            ctk.CTkLabel(content, text=time_info, font=("Segoe UI", 12), text_color=COLORS['text_light'], anchor="w").pack(anchor="w", pady=(3, 0))
            duration_badge = ctk.CTkFrame(session_card, fg_color=session['color_code'], corner_radius=10)
            duration_badge.pack(side="right", padx=12)
            ctk.CTkLabel(duration_badge, text=f"{session['duration_minutes']} min", font=("Segoe UI Bold", 12), text_color="white").pack(padx=15, pady=8)
            ctk.CTkButton(session_card, text="🗑️", width=40, height=40, corner_radius=10, fg_color="transparent", hover_color="#FF5252", text_color=COLORS['text_light'], command=lambda s=session: self.delete_session(s)).pack(side="right", padx=5)

    def delete_session(self, session):
        if messagebox.askyesno("Confirm", "Delete this session?", parent=self.parent):
            if db.delete_session(session['session_id']):
                self.load_sessions()
                self.dashboard.refresh_data()

    def show_add_session_dialog(self):
        """Show add session dialog - Fullscreen, Time Picker (No Calendar)"""
        subjects = db.get_user_subjects(self.user_id)
        if not subjects:
            messagebox.showwarning("No Subjects", "Please add subjects first!", parent=self.parent)
            return
        
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Add Study Session")
        dialog.after(10, lambda: dialog.state('zoomed'))
        dialog.configure(fg_color=COLORS['background'])
        dialog.grab_set()
        
        content = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=45, pady=40)
        
        ctk.CTkLabel(content, text="➕ Add Study Session", font=("Segoe UI Display", 28, "bold"), text_color=COLORS['text']).pack(pady=(0, 30))
        
        # Subject
        ctk.CTkLabel(content, text="Select Subject *", font=("Segoe UI Bold", 13), text_color=COLORS['text'], anchor="w").pack(fill="x", pady=(0, 8))
        subject_var = ctk.StringVar(value=subjects[0]['subject_name'])
        ctk.CTkOptionMenu(content, variable=subject_var, values=[s['subject_name'] for s in subjects], height=50, font=("Segoe UI", 14), fg_color=COLORS['card'], button_color=COLORS['primary'], text_color=COLORS['text'], dropdown_fg_color=COLORS['card'], dropdown_text_color=COLORS['text']).pack(fill="x", pady=(0, 20))
        
        # Date (Standard Text)
        ctk.CTkLabel(content, text="Session Date *", font=("Segoe UI Bold", 13), text_color=COLORS['text'], anchor="w").pack(fill="x", pady=(0, 8))
        date_entry = ctk.CTkEntry(content, placeholder_text="YYYY-MM-DD", height=50, font=("Segoe UI", 14), fg_color=COLORS['card'], border_width=1, border_color=COLORS['border'], text_color=COLORS['text'])
        date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        date_entry.pack(fill="x", pady=(0, 20))
        
        # Time Helper
        def open_time_picker(entry_widget, title):
            current_val = entry_widget.get()
            entry_widget.configure(state="disabled")
            def on_time_picked(time_str):
                entry_widget.configure(state="normal")
                entry_widget.delete(0, "end")
                entry_widget.insert(0, time_str)
            def on_close(): entry_widget.configure(state="normal")
            picker = TimePickerDialog(dialog, title=title, initial_time=current_val, callback=on_time_picked)
            picker.protocol("WM_DELETE_WINDOW", lambda: [on_close(), picker.destroy()])

        # Time Inputs
        time_container = ctk.CTkFrame(content, fg_color="transparent")
        time_container.pack(fill="x", pady=(0, 20))
        time_container.grid_columnconfigure(0, weight=1)
        time_container.grid_columnconfigure(1, weight=1)

        start_frame = ctk.CTkFrame(time_container, fg_color="transparent")
        start_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        ctk.CTkLabel(start_frame, text="Start Time *", font=("Segoe UI Bold", 13), text_color=COLORS['text'], anchor="w").pack(fill="x", pady=(0, 8))
        start_entry = ctk.CTkEntry(start_frame, placeholder_text="02:00 PM", height=50, font=("Segoe UI", 14), fg_color=COLORS['card'], border_width=1, border_color=COLORS['border'], text_color=COLORS['text'])
        start_entry.pack(fill="x")
        start_entry.bind("<Button-1>", lambda e: open_time_picker(start_entry, "Start Time"))

        end_frame = ctk.CTkFrame(time_container, fg_color="transparent")
        end_frame.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        ctk.CTkLabel(end_frame, text="End Time *", font=("Segoe UI Bold", 13), text_color=COLORS['text'], anchor="w").pack(fill="x", pady=(0, 8))
        end_entry = ctk.CTkEntry(end_frame, placeholder_text="04:00 PM", height=50, font=("Segoe UI", 14), fg_color=COLORS['card'], border_width=1, border_color=COLORS['border'], text_color=COLORS['text'])
        end_entry.pack(fill="x")
        end_entry.bind("<Button-1>", lambda e: open_time_picker(end_entry, "End Time"))
        
        # Topics & Notes
        ctk.CTkLabel(content, text="Topics Covered *", font=("Segoe UI Bold", 13), text_color=COLORS['text'], anchor="w").pack(fill="x", pady=(0, 8))
        topics_entry = ctk.CTkEntry(content, placeholder_text="e.g., Algebra", height=50, font=("Segoe UI", 14), fg_color=COLORS['card'], border_width=1, border_color=COLORS['border'], text_color=COLORS['text'])
        topics_entry.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(content, text="Notes (Optional)", font=("Segoe UI Bold", 13), text_color=COLORS['text'], anchor="w").pack(fill="x", pady=(0, 8))
        notes_text = ctk.CTkTextbox(content, height=150, font=("Segoe UI", 13), fg_color=COLORS['card'], border_width=1, border_color=COLORS['border'], text_color=COLORS['text'])
        notes_text.pack(fill="x", pady=(0, 30))
        
        # Buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x")
        ctk.CTkButton(btn_frame, text="Cancel", width=140, height=50, font=("Segoe UI Bold", 14), fg_color=COLORS['card'], hover_color=COLORS['hover'], text_color=COLORS['text'], command=dialog.destroy).pack(side="left")
        
        def save_session():
            subject_name = subject_var.get()
            session_date = date_entry.get().strip()
            start_time = start_entry.get().strip()
            end_time = end_entry.get().strip()
            topics = topics_entry.get().strip()
            notes = notes_text.get("1.0", "end").strip()
            
            if not all([subject_name, session_date, start_time, end_time, topics]):
                messagebox.showerror("Error", "Please fill all required fields!", parent=dialog)
                return
            
            try:
                session_date_obj = datetime.strptime(session_date, "%Y-%m-%d").date()
                start_time_obj = datetime.strptime(start_time, "%I:%M %p").time()
                end_time_obj = datetime.strptime(end_time, "%I:%M %p").time()
                start_datetime = datetime.combine(session_date_obj, start_time_obj)
                end_datetime = datetime.combine(session_date_obj, end_time_obj)
                
                if end_datetime <= start_datetime:
                     messagebox.showerror("Error", "End time must be after start time!", parent=dialog)
                     return

                duration = int((end_datetime - start_datetime).total_seconds() / 60)
                subject = next((s for s in subjects if s['subject_name'] == subject_name), None)
                result = db.add_study_session(self.user_id, subject['subject_id'], session_date_obj, start_time, end_time, duration, topics, notes)
                
                if result:
                    messagebox.showinfo("Success", "Study session added successfully!", parent=dialog)
                    dialog.destroy()
                    self.load_sessions()
                    self.dashboard.refresh_data()
                else:
                    messagebox.showerror("Error", "Failed to add session!", parent=dialog)
            
            except ValueError:
                messagebox.showerror("Error", "Invalid date/time format!", parent=dialog)
        
        ctk.CTkButton(btn_frame, text="Add Session", width=180, height=50, font=("Segoe UI Bold", 14), fg_color=COLORS['success'], hover_color="#388E3C", text_color="white", command=save_session).pack(side="right")