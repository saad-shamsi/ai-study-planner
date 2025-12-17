"""
AI Chatbot View - Powered by Groq
Advanced AI assistant with study help features
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from database import db
from config import COLORS
from groq_service import groq_ai
import threading
from saved_plans_view import SavedPlansView
from markdown_utils import MarkdownParser

class ChatbotView:
    """AI Chatbot with Groq integration"""
    
    def __init__(self, parent, dashboard):
        self.parent = parent
        self.dashboard = dashboard
        self.user_id = dashboard.user['user_id']
        
        self.chat_history = []
        
        self.create_ui()
        self.load_chat_history()
    
    def create_ui(self):
        """Create chatbot interface"""
        
        # Main container
        main_frame = ctk.CTkFrame(
            self.parent,
            fg_color="transparent"
        )
        main_frame.pack(fill="both", expand=True, padx=35, pady=35)
        
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header Frame
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 25))
        
        # === RIGHT SIDE: Action Buttons ===
        # Packed first so they reserve space on the right
        btn_container = ctk.CTkFrame(header, fg_color="transparent")
        btn_container.pack(side="right", padx=(20, 0))
        
        ctk.CTkButton(
            btn_container,
            text="📚 Study Plan",
            font=("Arial Bold", 13),
            width=130,
            height=40,
            corner_radius=10,
            fg_color=COLORS['info'],
            hover_color="#1976D2",
            text_color="white",
            command=self.show_study_plan_generator
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_container,
            text="💾 Saved Plans",
            font=("Arial Bold", 13),
            width=130,
            height=40,
            corner_radius=10,
            fg_color=COLORS['secondary'],
            hover_color=COLORS['secondary'],
            text_color="white",
            command=self.show_saved_plans
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_container,
            text="🗑️ Clear Chat",
            font=("Arial Bold", 13),
            width=130,
            height=40,
            corner_radius=10,
            fg_color="#FF5252",
            hover_color="#E53935",
            text_color="white",
            command=self.clear_chat
        ).pack(side="left", padx=5)
        
        # === LEFT SIDE: Title & Info ===
        # Packed second to fill remaining space
        left_header = ctk.CTkFrame(header, fg_color="transparent")
        left_header.pack(side="left", fill="x", expand=True)
        
        # 1. Title
        title_frame = ctk.CTkFrame(left_header, fg_color="transparent")
        title_frame.pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="🤖 AI Study Assistant",
            font=("Arial Black", 34),
            text_color=COLORS['text']
        ).pack(side="left")
        
        # 2. AI Badge (Moved to new line to prevent cutting off)
        ai_badge = ctk.CTkFrame(
            left_header, # Parent is now left_header, not title_frame
            fg_color=COLORS['success'],
            corner_radius=8
        )
        ai_badge.pack(anchor="w", pady=(5, 0)) # Pack below title
        
        ctk.CTkLabel(
            ai_badge,
            text="⚡ Powered by Groq",
            font=("Arial Bold", 11),
            text_color="white"
        ).pack(padx=10, pady=4)
        
        # 3. Description
        ctk.CTkLabel(
            left_header,
            text="Your intelligent learning companion with AI superpowers",
            font=("Arial", 15),
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(8, 0))
        
        # Chat container
        chat_card = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS['card'], # Dark Card
            corner_radius=20,
            border_width=1,
            border_color=COLORS['border']
        )
        chat_card.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        
        chat_card.grid_rowconfigure(0, weight=1)
        chat_card.grid_columnconfigure(0, weight=1)
        
        # Chat display (scrollable)
        self.chat_display = ctk.CTkScrollableFrame(
            chat_card,
            fg_color="transparent"
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        
        # Input area
        input_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_container.grid(row=2, column=0, sticky="ew")
        
        input_container.grid_columnconfigure(0, weight=1)
        
        # Quick suggestions
        suggestions_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        suggestions_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        suggestions = [
            "💡 Explain a concept",
            "📝 Generate questions",
            "📊 Analyze my progress",
            "🎯 Study tips"
        ]
        
        for suggestion in suggestions:
            ctk.CTkButton(
                suggestions_frame,
                text=suggestion,
                font=("Segoe UI", 11),
                height=32,
                corner_radius=8,
                fg_color=COLORS['card'],
                hover_color=COLORS['hover'],
                text_color=COLORS['text'],
                command=lambda s=suggestion: self.use_suggestion(s)
            ).pack(side="left", padx=5)
        
        # Input box
        self.message_input = ctk.CTkTextbox(
            input_container,
            height=90,
            font=("Segoe UI", 14),
            fg_color=COLORS['card'], # Dark Input
            text_color=COLORS['text'],
            border_width=1,
            border_color=COLORS['border'],
            corner_radius=15
        )
        self.message_input.grid(row=1, column=0, sticky="ew", padx=(0, 15))
        
        # Send button
        self.send_button = ctk.CTkButton(
            input_container,
            text="Send ➤",
            font=("Arial Bold", 16),
            width=130,
            height=90,
            corner_radius=15,
            fg_color=COLORS['success'],
            hover_color="#388E3C",
            text_color="white",
            command=self.send_message
        )
        self.send_button.grid(row=1, column=1)
        
        # Bind Enter key
        self.message_input.bind('<Return>', self.handle_enter_key)
        
        # Show welcome
        self.show_welcome_message()
    
    def show_welcome_message(self):
        """Show AI welcome message"""
        welcome_text = f"""Hello {self.dashboard.user['full_name']}! 👋

I'm your AI Study Assistant powered by Groq's lightning-fast AI. I can help you with:

📚 **Concept Explanations** - Ask me to explain any topic
✏️ **Study Plans** - Generate personalized study schedules
📝 **Practice Questions** - Get custom practice problems
🎯 **Study Tips** - Learn effective study strategies
📊 **Progress Analysis** - Understand your study patterns
💡 **Homework Help** - Get guidance on assignments

**Try asking me:**
- "Explain photosynthesis in simple terms"
- "Generate 5 math practice questions"
- "Give me tips for studying physics"
- "Create a study plan for my exams"

How can I help you today?"""
        
        self.add_message("assistant", welcome_text)
    
    def use_suggestion(self, suggestion):
        """Use quick suggestion"""
        prompts = {
            "💡 Explain a concept": "Can you explain a concept to me? I need help understanding...",
            "📝 Generate questions": "Can you generate some practice questions for...",
            "📊 Analyze my progress": "Can you analyze my study progress and give recommendations?",
            "🎯 Study tips": "What are some effective study tips for..."
        }
        
        self.message_input.delete("1.0", "end")
        self.message_input.insert("1.0", prompts.get(suggestion, suggestion))
        self.message_input.focus()
    
    def load_chat_history(self):
        """Load chat history"""
        history = db.get_chat_history(self.user_id, limit=20)
        
        for chat in history:
            self.add_message("user", chat['message'], save=False)
            if chat['response']:
                self.add_message("assistant", chat['response'], save=False)
    
    def add_message(self, role, text, save=True):
        """Add message to chat"""
        
        message_frame = ctk.CTkFrame(
            self.chat_display,
            fg_color="transparent"
        )
        message_frame.pack(fill="x", pady=8, padx=10)
        
        if role == "user":
            # User message (right)
            bubble = ctk.CTkFrame(
                message_frame,
                fg_color=COLORS['primary'],
                corner_radius=18
            )
            bubble.pack(side="right", padx=(80, 0))
            
            ctk.CTkLabel(
                bubble,
                text=text,
                font=("Arial", 14),
                text_color="white",
                wraplength=550,
                justify="left"
            ).pack(padx=20, pady=15)
            
        else:
            # Assistant message (left)
            bubble = ctk.CTkFrame(
                message_frame,
                fg_color=COLORS['background'],
                corner_radius=18
            )
            bubble.pack(side="left", padx=(0, 80))
            
            content_frame = ctk.CTkFrame(bubble, fg_color="transparent")
            content_frame.pack(padx=20, pady=15)
            
            # Bot icon
            icon_bg = ctk.CTkFrame(
                content_frame,
                fg_color=COLORS['success'],
                corner_radius=30,
                width=40,
                height=40
            )
            icon_bg.pack(side="left", padx=(0, 12))
            icon_bg.pack_propagate(False)
            
            ctk.CTkLabel(
                icon_bg,
                text="🤖",
                font=("Arial", 22)
            ).place(relx=0.5, rely=0.5, anchor="center")
            
            # Message text (using Textbox for Markdown)
            message_box = ctk.CTkTextbox(
                content_frame,
                font=("Arial", 14),
                text_color=COLORS['text'],
                width=550,
                height=100, # Initial height, will auto-adjust
                fg_color="transparent",
                wrap="word"
            )
            message_box.pack(side="left")
            
            # Apply Markdown
            parser = MarkdownParser(message_box)
            parser.parse_and_insert(text)
            
            # Disable editing
            message_box.configure(state="disabled")
            
            # Auto-adjust height (approximate)
            num_lines = text.count('\n') + (len(text) // 60) + 2
            message_box.configure(height=min(num_lines * 25, 500))
        
        # Scroll to bottom
        self.chat_display._parent_canvas.yview_moveto(1.0)
        
        # Save history
        if save and role == "user":
            self.chat_history.append({"role": "user", "content": text})
    
    def handle_enter_key(self, event):
        """Handle Enter key"""
        if event.state & 0x0001:  # Shift+Enter
            return
        else:
            self.send_message()
            return "break"
    
    def send_message(self):
        """Send message to AI"""
        message = self.message_input.get("1.0", "end").strip()
        
        if not message:
            return
        
        # Clear input
        self.message_input.delete("1.0", "end")
        
        # Add user message
        self.add_message("user", message)
        
        # Show typing indicator
        self.send_button.configure(state="disabled", text="Thinking...")
        
        # Get AI response in thread
        def get_response():
            response = self.get_ai_response(message)
            
            # UPDATE: Use self.parent.after instead of self.after
            # This fixes the error because self.parent is the Widget
            self.parent.after(0, lambda: self.add_message("assistant", response))
            self.parent.after(0, lambda: db.save_chat_message(self.user_id, message, response))
            self.parent.after(0, lambda: self.send_button.configure(state="normal", text="Send ➤"))
        
        threading.Thread(target=get_response, daemon=True).start()
    
    def get_ai_response(self, message):
        """Get response from Groq AI with full context"""
        
        # 1. Fetch Context
        context = db.get_user_context(self.user_id)
        
        # 2. Build detailed system prompt
        system_prompt = f"""You are a personalized AI Study Assistant for {context['name']} ({context['level']}).

YOUR CONTEXT:
- Total Study Time: {context['total_hours']} hrs ({context['recent_hours']} hrs this week)
- Total Sessions: {context['total_sessions']}
- Strongest Subject: {context['strongest_subject']}
- Weakest Subject: {context['weakest_subject']} (Needs attention)

SUBJECTS & DIFFICULTY:
{', '.join(context['subjects'])}

ACTIVE GOALS:
{chr(10).join(['- ' + g for g in context['goals']]) if context['goals'] else 'No active goals.'}

INSTRUCTIONS:
- Use this context to give personalized advice.
- If they ask about their stats, use the numbers above.
- If they ask for a plan, focus on their weakest subject.
- Be encouraging, concise, and use Markdown (bold, lists) for clarity.
"""
        
        # 3. Build messages
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.chat_history[-10:])  # Last 10 messages for conversation flow
        messages.append({"role": "user", "content": message})
        
        # 4. Get AI response
        try:
            response = groq_ai.chat(messages, temperature=0.7, max_tokens=1024)
            
            # Add to history
            self.chat_history.append({"role": "assistant", "content": response})
            return response
            
        except Exception as e:
            return f"❌ Error connecting to AI: {str(e)}"
    
    def show_study_plan_generator(self):
        """Show study plan generator dialog"""
        from ai_study_generator import StudyPlanGenerator
        generator = StudyPlanGenerator(self.parent, self.dashboard)

    def show_saved_plans(self):
        """Show saved plans"""
        SavedPlansView(self.parent, self.dashboard)
    
    def clear_chat(self):
        """Clear chat history"""
        response = messagebox.askyesno(
            "Clear Chat",
            "Clear entire chat history?",
            parent=self.parent
        )
        
        if response:
            db.clear_chat_history(self.user_id)
            
            for widget in self.chat_display.winfo_children():
                widget.destroy()
            
            self.chat_history = []
            
            self.show_welcome_message()
            
            messagebox.showinfo("Success", "Chat cleared!", parent=self.parent)