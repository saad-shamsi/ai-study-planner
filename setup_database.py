import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def setup_new_database():
    new_db_name = DB_CONFIG['database']
    print(f"🚀 SETTING UP NEW DATABASE: {new_db_name}")
    
    # 1. Connect to MySQL Server (Root)
    server_config = DB_CONFIG.copy()
    if 'database' in server_config:
        del server_config['database']
        
    try:
        conn = mysql.connector.connect(**server_config)
        cursor = conn.cursor()
        
        # 2. Create the NEW Database (Safe create)
        print(f"✨  Creating database '{new_db_name}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        # 3. Switch to the new database
        cursor.execute(f"USE {new_db_name}")
        
        # 4. Create Tables (The Fresh Structure)
        tables = [
            """CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                student_level VARCHAR(50) DEFAULT 'University',
                last_login DATE,
                current_streak INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS subjects (
                subject_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                subject_name VARCHAR(100) NOT NULL,
                subject_code VARCHAR(50),
                color_code VARCHAR(20) DEFAULT '#3498db',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS study_sessions (
                session_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                subject_id INT NOT NULL,
                session_date DATE NOT NULL,
                start_time VARCHAR(10),
                end_time VARCHAR(10),
                duration_minutes INT DEFAULT 0,
                topics_covered TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS study_goals (
                goal_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                subject_id INT,
                goal_title VARCHAR(255) NOT NULL,
                goal_description TEXT,
                status ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
                priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
                target_date DATE,
                completed_at DATETIME,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE SET NULL
            )""",
            """CREATE TABLE IF NOT EXISTS mood_tracker (
                mood_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                mood_type VARCHAR(50) NOT NULL,
                mood_date DATE NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE KEY unique_daily_mood (user_id, mood_date)
            )""",
            """CREATE TABLE IF NOT EXISTS study_streaks (
                streak_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                streak_date DATE NOT NULL,
                studied BOOLEAN DEFAULT FALSE,
                flower_level INT DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE KEY unique_daily_streak (user_id, streak_date)
            )""",
            """CREATE TABLE IF NOT EXISTS study_pet (
                pet_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                pet_name VARCHAR(50) DEFAULT 'Studdy',
                happiness_level INT DEFAULT 50,
                energy_level INT DEFAULT 50,
                total_claps INT DEFAULT 0,
                last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS pomodoro_sessions (
                pomodoro_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                subject_id INT,
                session_date DATE NOT NULL,
                total_cycles INT DEFAULT 0,
                completed_cycles INT DEFAULT 0,
                total_focus_minutes INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS notifications (
                notification_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                notification_type VARCHAR(50),
                message TEXT,
                priority VARCHAR(20) DEFAULT 'medium',
                is_read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS quick_notes (
                note_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                subject_id INT,
                note_title VARCHAR(255),
                note_content TEXT,
                is_pinned BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE SET NULL
            )""",
            """CREATE TABLE IF NOT EXISTS chat_history (
                chat_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                message TEXT,
                response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS weekly_reports (
                report_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                week_start_date DATE,
                week_end_date DATE,
                total_study_hours FLOAT DEFAULT 0,
                total_sessions INT DEFAULT 0,
                productivity_score INT DEFAULT 0,
                strongest_subject VARCHAR(100),
                weakest_subject VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS motivational_quotes (
                quote_id INT AUTO_INCREMENT PRIMARY KEY,
                quote_text TEXT NOT NULL,
                author VARCHAR(100) DEFAULT 'Unknown'
            )""",
            """CREATE TABLE IF NOT EXISTS saved_study_plans (
                plan_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                plan_content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS reminders (
                reminder_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                message TEXT,
                reminder_time DATETIME,
                status ENUM('pending', 'sent') DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )"""
        ]

        print("⚙️  Building Tables...")
        for sql in tables:
            cursor.execute(sql)
            
        # 5. Migration: Add student_level if missing
        try:
            cursor.execute("SELECT student_level FROM users LIMIT 1")
            cursor.fetchall() # Consume result if exists
        except Error:
            print("🔄 Migrating: Adding student_level column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN student_level VARCHAR(50) DEFAULT 'University'")
            
        # Seed Data (Only if empty)
        cursor.execute("SELECT COUNT(*) FROM motivational_quotes")
        if cursor.fetchone()[0] == 0:
            print("🌱  Adding Quotes...")
            quotes = [
                ("The secret of getting ahead is getting started.", "Mark Twain"),
                ("It always seems impossible until it's done.", "Nelson Mandela")
            ]
            cursor.executemany("INSERT INTO motivational_quotes (quote_text, author) VALUES (%s, %s)", quotes)
            conn.commit()
        
        print(f"\n✅  SUCCESS! New Database '{new_db_name}' is ready.")
        
    except Error as e:
        print(f"\n❌  MySQL Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_new_database()