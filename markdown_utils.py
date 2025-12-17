"""
Markdown Utility for CustomTkinter
Parses basic Markdown syntax and applies tags to CTkTextbox
"""

import re

class MarkdownParser:
    """Parses Markdown text and applies formatting to CTkTextbox"""
    
    def __init__(self, textbox):
        self.textbox = textbox
        self.setup_tags()
        
    def setup_tags(self):
        """Configure text tags for formatting"""
        # Access underlying tkinter widget to bypass CTk restriction on 'font' tag
        target = self.textbox._textbox if hasattr(self.textbox, '_textbox') else self.textbox
        
        # Headers - Use Aurora Primary/Secondary colors or White
        target.tag_config("h1", font=("Segoe UI Display", 26, "bold"), foreground="#F8FAFC")
        target.tag_config("h2", font=("Segoe UI Display", 22, "bold"), foreground="#38BDF8") # Cyan
        target.tag_config("h3", font=("Segoe UI Display", 18, "bold"), foreground="#818CF8") # Purple
        
        # Text styles
        target.tag_config("bold", font=("Segoe UI", 14, "bold"), foreground="#F8FAFC")
        target.tag_config("italic", font=("Segoe UI", 14, "italic"), foreground="#CBD5E1")
        # Code block - Darker slate background, Pink/Cyan text
        target.tag_config("code", font=("Consolas", 12), background="#1E293B", foreground="#F472B6")
        
        # Lists
        target.tag_config("bullet", lmargin1=20, lmargin2=30, foreground="#E2E8F0")
        
    def parse_and_insert(self, text):
        """Parse markdown and insert into textbox"""
        lines = text.split('\n')
        
        for line in lines:
            # Headers
            if line.startswith('# '):
                self.textbox.insert("end", line[2:] + "\n", "h1")
            elif line.startswith('## '):
                self.textbox.insert("end", line[3:] + "\n", "h2")
            elif line.startswith('### '):
                self.textbox.insert("end", line[4:] + "\n", "h3")
                
            # Bullet points
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                content = line.strip()[2:]
                self.insert_formatted_line("• " + content + "\n", "bullet")
                
            # Numbered lists
            elif re.match(r'^\d+\.', line.strip()):
                self.insert_formatted_line(line + "\n", "bullet")
                
            # Normal text
            else:
                self.insert_formatted_line(line + "\n")
                
    def insert_formatted_line(self, text, base_tag=None):
        """Insert line with inline formatting (bold, italic, code)"""
        
        # Split by bold markers (**text**)
        parts = re.split(r'(\*\*.*?\*\*)', text)
        
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                # Bold text
                clean_text = part[2:-2]
                self.textbox.insert("end", clean_text, ("bold", base_tag) if base_tag else "bold")
            else:
                # Check for italic (*text*)
                sub_parts = re.split(r'(\*.*?\*)', part)
                for sub_part in sub_parts:
                    if sub_part.startswith('*') and sub_part.endswith('*') and len(sub_part) > 2:
                        clean_text = sub_part[1:-1]
                        self.textbox.insert("end", clean_text, ("italic", base_tag) if base_tag else "italic")
                    else:
                        # Check for code (`text`)
                        code_parts = re.split(r'(`.*?`)', sub_part)
                        for code_part in code_parts:
                            if code_part.startswith('`') and code_part.endswith('`'):
                                clean_text = code_part[1:-1]
                                self.textbox.insert("end", clean_text, ("code", base_tag) if base_tag else "code")
                            else:
                                if code_part:
                                    self.textbox.insert("end", code_part, base_tag if base_tag else None)
