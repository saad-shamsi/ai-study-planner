"""
Main Entry Point
Runs database setup automatically and then launches the app.
"""

import customtkinter as ctk
import sys
import os

# --- SMOOTH ANIMATION & HIGH DPI FIX ---
try:
    from ctypes import windll
    # This enables High DPI awareness on Windows, making scrolling and animations smoother
    windll.shcore.SetProcessDpiAwareness(1) 
except Exception:
    pass
# ---------------------------------------

# Import modules
from setup_database import setup_new_database
from login import LoginWindow

def main():
    print("------------------------------------------------")
    print("🚀 STARTING AI STUDY PLANNER")
    print("------------------------------------------------")

    # 1. Initialize Database
    print("🔄 Checking Database System...")
    try:
        setup_new_database()
        print("✅ Database System: ONLINE")
    except Exception as e:
        print(f"❌ Database Error: {e}")
        print("   Please check if MySQL is running!")
        return

    # 2. Launch Application
    print("✨ Launching Interface...")
    try:
        # Optional: Set a slightly higher scaling for better visibility on modern screens
        # ctk.set_widget_scaling(1.1) 
        
        app = LoginWindow()
        app.mainloop()
    except Exception as e:
        print(f"❌ Application Error: {e}")

if __name__ == "__main__":
    main()