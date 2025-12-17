

# MySQL Database Configuration
# MySQL Database Configuration
DB_CONFIG = {
    'host': 'localhost',        
    'user': 'root',             
    'password': 'root', # Your password
    'database': 'pot800',  # <--- CHANGED THIS NAME
    'port': 3306,               
    'charset': 'utf8mb4',
    'use_unicode': True,
    'autocommit': False
}

# ... rest of the file remains the same ...

# Groq API Configuration (RECOMMENDED - Fast & Free)
GROQ_API_KEY = 'sk-XXXXXXXXXXXXXXXXXXXX'

  # Get from: https://console.groq.com
GROQ_MODEL = 'llama-3.3-70b-versatile'  # Fast & powerful model

# Email Configuration for 2FA
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',         # Default to Gmail
    'smtp_port': 587,                        # Standard TLS port
    'email_address': 'yourmail@gmail.com', 
    'email_password': 'your-app-password'   
}


# Application Settings
APP_NAME = "AI Powered Study Planner"
APP_VERSION = "2.0.0"

# UI Theme Colors (Light & Cozy)
# Premium Aurora Theme (Dark Mode)
COLORS = {
    'background': "#0F172A",      # Deep Midnight Slate
    'sidebar': "#1E293B",         # Lighter Slate
    'card': "#1E293B",            # Matching Sidebar
    'primary': '#38BDF8',         # Aurora Cyan
    'secondary': '#818CF8',       # Aurora Purple
    'success': '#34D399',         # Aurora Green
    'warning': '#fbbf24',         # Warm Amber
    'info': '#60A5FA',            # Soft Blue
    'text': '#F8FAFC',            # Off-white
    'text_light': '#94A3B8',      # Slate Gray
    'hover': '#334155',           # Hover State
    'border': '#334155'           # Subtle Border
}
QSS_STYLE = """
QWidget {
    background-color: #F5F7FA;
    color: #2D3748;
    font-size: 14px;
}

QPushButton {
    background-color: #6C63FF;
    padding: 8px;
    border-radius: 6px;
    color: white;
}

QPushButton:hover {
    background-color: #574CD8;
}
"""
