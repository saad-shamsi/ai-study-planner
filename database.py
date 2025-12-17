"""
Database Manager for AI Study Planner (MySQL Version)
Handles all database operations using MySQL.
"""

import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime, date, timedelta
from config import DB_CONFIG

class DatabaseManager:
    """Manages all database operations for the Study Planner using MySQL"""
    
    def __init__(self):
        """Initialize database connection check"""
        self.test_connection()
        self.check_schema_updates()
        
    def check_schema_updates(self):
        """Ensure new columns exist in existing database"""
        try:
            # Check last_login
            check = "SHOW COLUMNS FROM users LIKE 'last_login'"
            if not self.execute_query(check, fetch=True):
                print("🔧 Migrating: Adding 'last_login' to users...")
                self.execute_query("ALTER TABLE users ADD COLUMN last_login DATE")
                
            # Check current_streak    
            check = "SHOW COLUMNS FROM users LIKE 'current_streak'"
            if not self.execute_query(check, fetch=True):
                print("🔧 Migrating: Adding 'current_streak' to users...")
                self.execute_query("ALTER TABLE users ADD COLUMN current_streak INT DEFAULT 0")
                
        except Exception as e:
            print(f"⚠️ Schema Update Check Failed: {e}")
    
    def get_connection(self):
        """Get a connection to the MySQL database"""
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except Error as e:
            print(f"❌ Error connecting to database: {e}")
            return None
    
    def execute_query(self, query, params=None, fetch=False):
        """
        Execute a SQL query with parameters using MySQL Connector
        """
        connection = self.get_connection()
        if not connection:
            return None
        
        cursor = None
        try:
            # Return results as dictionaries
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.lastrowid
                
        except Error as e:
            print(f"❌ Database Error: {e}")
            # print(f"Query: {query}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    # ==================== USER MANAGEMENT ====================
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, email, password, full_name, student_level="University"):
        password_hash = self.hash_password(password)
        query = """
            INSERT INTO users (username, email, password_hash, full_name, student_level)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (username, email, password_hash, full_name, student_level))
    
    def verify_user(self, username, password):
        password_hash = self.hash_password(password)
        query = """
            SELECT user_id, username, email, full_name, student_level, created_at
            FROM users
            WHERE username = %s AND password_hash = %s
        """
        result = self.execute_query(query, (username, password_hash), fetch=True)
        return result[0] if result else None
    
    def check_username_exists(self, username):
        query = "SELECT COUNT(*) as count FROM users WHERE username = %s"
        result = self.execute_query(query, (username,), fetch=True)
        return result[0]['count'] > 0 if result else False
    
    def check_email_exists(self, email):
        query = "SELECT COUNT(*) as count FROM users WHERE email = %s"
        result = self.execute_query(query, (email,), fetch=True)
        return result[0]['count'] > 0 if result else False
    
    def get_user_by_id(self, user_id):
        query = """
            SELECT user_id, username, email, full_name, student_level, created_at
            FROM users WHERE user_id = %s
        """
        result = self.execute_query(query, (user_id,), fetch=True)
        return result[0] if result else None
    
    # ==================== SUBJECT MANAGEMENT ====================
    
    def add_subject(self, user_id, subject_name, subject_code=None, color_code='#3498db'):
        query = """
            INSERT INTO subjects (user_id, subject_name, subject_code, color_code)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (user_id, subject_name, subject_code, color_code))
    
    def get_user_subjects(self, user_id):
        query = """
            SELECT subject_id, subject_name, subject_code, color_code, created_at
            FROM subjects
            WHERE user_id = %s
            ORDER BY created_at DESC
        """
        return self.execute_query(query, (user_id,), fetch=True)
    
    def update_subject(self, subject_id, subject_name, subject_code=None, color_code=None):
        query = """
            UPDATE subjects
            SET subject_name = %s, subject_code = %s, color_code = %s
            WHERE subject_id = %s
        """
        return self.execute_query(query, (subject_name, subject_code, color_code, subject_id))
    
    def delete_subject(self, subject_id):
        query = "DELETE FROM subjects WHERE subject_id = %s"
        return self.execute_query(query, (subject_id,))
    
    # ==================== STUDY SESSIONS ====================
    
    def add_study_session(self, user_id, subject_id, session_date, start_time, 
                         end_time, duration_minutes, topics_covered, notes=''):
        # 1. Add Session
        query = """
            INSERT INTO study_sessions 
            (user_id, subject_id, session_date, start_time, end_time, 
             duration_minutes, topics_covered, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        result = self.execute_query(query, (user_id, subject_id, session_date, 
                                     start_time, end_time, duration_minutes, 
                                     topics_covered, notes))
        
        # 2. Add ROBUST Reminders
        try:
            dt_str = f"{session_date} {start_time}"
            # Try parsing with AM/PM first, then fallback to 24-hour
            try:
                start_dt = datetime.strptime(dt_str, "%Y-%m-%d %I:%M %p")
            except ValueError:
                start_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
                
            end_dt = start_dt + timedelta(minutes=duration_minutes)
            
            reminders = [
                # A. 15 Mins Before (Preparation)
                (start_dt - timedelta(minutes=15), f"🚀 Get Ready! Study session '{topics_covered}' starts in 15 mins."),
                
                # B. At Start Time (Action)
                (start_dt, f"⏰ It's Time! Start studying '{topics_covered}' now."),
                
                # C. After Session (Accountability)
                (end_dt + timedelta(minutes=5), f"✅ Did you finish '{topics_covered}'? Don't forget to review your notes!")
            ]
            
            for rem_time, msg in reminders:
                self.add_reminder(user_id, msg, rem_time)
                
        except Exception as e:
            print(f"⚠️ Reminder Error: {e}")
            
        return result
    
    def get_user_sessions(self, user_id, limit=None):
        query = """
            SELECT s.*, sub.subject_name, sub.color_code
            FROM study_sessions s
            JOIN subjects sub ON s.subject_id = sub.subject_id
            WHERE s.user_id = %s
            ORDER BY s.session_date DESC, s.start_time DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        return self.execute_query(query, (user_id,), fetch=True)
    
    def get_sessions_by_date_range(self, user_id, start_date, end_date):
        query = """
            SELECT s.*, sub.subject_name, sub.color_code
            FROM study_sessions s
            JOIN subjects sub ON s.subject_id = sub.subject_id
            WHERE s.user_id = %s AND s.session_date BETWEEN %s AND %s
            ORDER BY s.session_date, s.start_time
        """
        return self.execute_query(query, (user_id, start_date, end_date), fetch=True)
    
    def delete_session(self, session_id):
        query = "DELETE FROM study_sessions WHERE session_id = %s"
        return self.execute_query(query, (session_id,))
    
    # ==================== STUDY GOALS ====================
    
    def add_goal(self, user_id, goal_title, subject_id=None, goal_description='',
                 target_date=None, priority='medium'):
        # 1. Add Goal
        query = """
            INSERT INTO study_goals 
            (user_id, subject_id, goal_title, goal_description, target_date, priority)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        result = self.execute_query(query, (user_id, subject_id, goal_title, 
                                     goal_description, target_date, priority))
        # 2. Add Reminder
        if target_date:
            try:
                target_dt = datetime.strptime(str(target_date), "%Y-%m-%d")
                reminder_time = target_dt.replace(hour=9, minute=0, second=0)
                self.add_reminder(user_id, f"Goal Deadline: {goal_title}", reminder_time)
            except Exception as e:
                print(f"Reminder Error: {e}")
        return result
    
    def get_user_goals(self, user_id, status=None):
        if status:
            query = """
                SELECT g.*, s.subject_name, s.color_code
                FROM study_goals g
                LEFT JOIN subjects s ON g.subject_id = s.subject_id
                WHERE g.user_id = %s AND g.status = %s
                ORDER BY g.priority DESC, g.target_date
            """
            return self.execute_query(query, (user_id, status), fetch=True)
        else:
            query = """
                SELECT g.*, s.subject_name, s.color_code
                FROM study_goals g
                LEFT JOIN subjects s ON g.subject_id = s.subject_id
                WHERE g.user_id = %s
                ORDER BY g.status, g.priority DESC, g.target_date
            """
            return self.execute_query(query, (user_id,), fetch=True)
    
    def update_goal_status(self, goal_id, status):
        completed_at = datetime.now() if status == 'completed' else None
        query = """
            UPDATE study_goals
            SET status = %s, completed_at = %s
            WHERE goal_id = %s
        """
        return self.execute_query(query, (status, completed_at, goal_id))
    
    def delete_goal(self, goal_id):
        query = "DELETE FROM study_goals WHERE goal_id = %s"
        return self.execute_query(query, (goal_id,))
    
    # ==================== ANALYTICS ====================
    
    def get_total_study_time(self, user_id, start_date=None, end_date=None):
        if start_date and end_date:
            query = """
                SELECT SUM(duration_minutes) as total_minutes
                FROM study_sessions
                WHERE user_id = %s AND session_date BETWEEN %s AND %s
            """
            result = self.execute_query(query, (user_id, start_date, end_date), fetch=True)
        else:
            query = """
                SELECT SUM(duration_minutes) as total_minutes
                FROM study_sessions
                WHERE user_id = %s
            """
            result = self.execute_query(query, (user_id,), fetch=True)
        
        return result[0]['total_minutes'] if result and result[0]['total_minutes'] else 0
    
    def get_subject_wise_time(self, user_id):
        query = """
            SELECT s.subject_name, s.color_code, 
                   SUM(ss.duration_minutes) as total_minutes,
                   COUNT(ss.session_id) as session_count
            FROM study_sessions ss
            JOIN subjects s ON ss.subject_id = s.subject_id
            WHERE ss.user_id = %s
            GROUP BY s.subject_id
            ORDER BY total_minutes DESC
        """
        return self.execute_query(query, (user_id,), fetch=True)
    
    def get_daily_study_stats(self, user_id, days=7):
        query = """
            SELECT session_date, SUM(duration_minutes) as total_minutes
            FROM study_sessions
            WHERE user_id = %s AND session_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            GROUP BY session_date
            ORDER BY session_date
        """
        return self.execute_query(query, (user_id, days), fetch=True)
    
    # ==================== CHAT HISTORY ====================
    
    def save_chat_message(self, user_id, message, response):
        query = """
            INSERT INTO chat_history (user_id, message, response)
            VALUES (%s, %s, %s)
        """
        return self.execute_query(query, (user_id, message, response))
    
    def get_chat_history(self, user_id, limit=50):
        query = """
            SELECT message, response, timestamp
            FROM chat_history
            WHERE user_id = %s
            ORDER BY timestamp DESC
            LIMIT %s
        """
        result = self.execute_query(query, (user_id, limit), fetch=True)
        return list(reversed(result)) if result else []
    
    def clear_chat_history(self, user_id):
        query = "DELETE FROM chat_history WHERE user_id = %s"
        return self.execute_query(query, (user_id,))
    
    # ==================== MOOD TRACKER ====================
    
    def add_mood(self, user_id, mood_type, notes=''):
        today = datetime.now().date()
        query = """
            INSERT INTO mood_tracker (user_id, mood_type, mood_date, notes)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE mood_type = %s, notes = %s
        """
        return self.execute_query(query, (user_id, mood_type, today, notes, mood_type, notes))
    
    def get_user_moods(self, user_id, days=30):
        query = """
            SELECT mood_type, mood_date, notes
            FROM mood_tracker
            WHERE user_id = %s AND mood_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            ORDER BY mood_date DESC
        """
        return self.execute_query(query, (user_id, days), fetch=True)
    
    def get_today_mood(self, user_id):
        today = datetime.now().date()
        query = """
            SELECT mood_type, notes FROM mood_tracker
            WHERE user_id = %s AND mood_date = %s
        """
        result = self.execute_query(query, (user_id, today), fetch=True)
        return result[0] if result else None
    
    # ==================== STUDY STREAK ====================
    
    def update_streak(self, user_id, studied=True):
        today = datetime.now().date()
        query = """
            INSERT INTO study_streaks (user_id, streak_date, studied, flower_level)
            VALUES (%s, %s, %s, 1)
            ON DUPLICATE KEY UPDATE studied = %s, flower_level = flower_level + 1
        """
        return self.execute_query(query, (user_id, today, studied, studied))
    
    def get_current_streak(self, user_id):
        """Get current streak from users table"""
        query = "SELECT current_streak FROM users WHERE user_id = %s"
        result = self.execute_query(query, (user_id,), fetch=True)
        
        if result and result[0]['current_streak'] is not None:
            return result[0]['current_streak']
        return 0 

    def update_login_streak(self, user_id):
        """Build addictive streak: Called on Login"""
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        # 1. Get last streak info
        query = "SELECT last_login, current_streak FROM users WHERE user_id = %s"
        user = self.execute_query(query, (user_id,), fetch=True)[0]
        
        last_login = user['last_login']
        current_streak = user['current_streak']
        
        # 2. Update logic
        new_streak = current_streak
        
        if last_login == today:
            pass # Already logged in today, no change
        elif last_login == yesterday:
            new_streak += 1 # Continued streak!
        else:
            new_streak = 1 # Broken streak (or first login) :(
            
        # 3. Save
        # Also log to study_streaks table for graph
        self.execute_query(
            "UPDATE users SET last_login = %s, current_streak = %s WHERE user_id = %s",
            (today, new_streak, user_id)
        )
        
        # Ensure entry in study_streaks for today
        self.execute_query(
            "INSERT IGNORE INTO study_streaks (user_id, streak_date, studied) VALUES (%s, %s, 0)",
            (user_id, today)
        )
        
        return new_streak

    def check_streak_risk(self, user_id):
        """Check if streak is at risk (no login for 20h)"""
        query = "SELECT last_login, current_streak FROM users WHERE user_id = %s"
        result = self.execute_query(query, (user_id,), fetch=True)
        
        if not result or not result[0]['last_login']:
            return None
            
        last_login = result[0]['last_login']
        # Ensure last_login is date object
        if isinstance(last_login, datetime):
            last_login = last_login.date()
            
        today = date.today()
        
        # If last login was yesterday (streak active but not extended today)
        if last_login == today - timedelta(days=1):
            # Check time: If it's past 8 PM (20:00)
            now = datetime.now()
            if now.hour >= 20: 
                # Check if we already warned today
                check_query = """
                    SELECT * FROM notifications 
                    WHERE user_id = %s 
                    AND notification_type = 'streak_warning' 
                    AND DATE(created_at) = %s
                """
                existing = self.execute_query(check_query, (user_id, today), fetch=True)
                
                if not existing:
                    # Create Warning Notification
                    message = f"🔥 Streak Risk! You have {24 - now.hour} hours left to login and save your {result[0]['current_streak']} day streak!"
                    self.add_notification(user_id, message, "high", "streak_warning")
                    return {'message': message, 'priority': 'high'}
                    
        return None
    
    def get_streak_garden(self, user_id, days=30):
        query = """
            SELECT streak_date, studied, flower_level
            FROM study_streaks
            WHERE user_id = %s AND streak_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            ORDER BY streak_date
        """
        return self.execute_query(query, (user_id, days), fetch=True)
    
    # ==================== STUDY PET ====================
    
    def get_or_create_pet(self, user_id):
        query = "SELECT * FROM study_pet WHERE user_id = %s"
        result = self.execute_query(query, (user_id,), fetch=True)
        
        if result:
            return result[0]
        else:
            create_query = """
                INSERT INTO study_pet (user_id, pet_name, happiness_level, energy_level)
                VALUES (%s, 'Studdy', 50, 50)
            """
            self.execute_query(create_query, (user_id,))
            return self.get_or_create_pet(user_id)
    
    def update_pet_status(self, user_id, happiness_change=0, energy_change=0, claps=0):
        query = """
            UPDATE study_pet
            SET happiness_level = GREATEST(0, LEAST(100, happiness_level + %s)),
                energy_level = GREATEST(0, LEAST(100, energy_level + %s)),
                total_claps = total_claps + %s,
                last_interaction = CURRENT_TIMESTAMP
            WHERE user_id = %s
        """
        # Note: MySQL uses GREATEST/LEAST vs SQLite distinct MAX/MIN usage often, 
        # but the logic 'MAX(0, MIN(100, ...))' works in MySQL too usually.
        # But wait, SQLite has MAX/MIN scalar functions? 
        # In MySQL, MAX() is aggregate, GREATEST() is scalar.
        # The original code likely came from MySQL and was compatible or I should use GREATEST/LEAST.
        # Let's use GREATEST/LEAST for safety in MySQL.
        return self.execute_query(query, (happiness_change, energy_change, claps, user_id))
    
    # ==================== POMODORO ====================
    
    def add_pomodoro_session(self, user_id, subject_id, completed_cycles, total_minutes):
        today = datetime.now().date()
        query = """
            INSERT INTO pomodoro_sessions 
            (user_id, subject_id, session_date, total_cycles, completed_cycles, total_focus_minutes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (user_id, subject_id, today, completed_cycles, completed_cycles, total_minutes))
    
    def get_pomodoro_stats(self, user_id, days=7):
        query = """
            SELECT session_date, SUM(completed_cycles) as total_cycles, 
                   SUM(total_focus_minutes) as total_minutes
            FROM pomodoro_sessions
            WHERE user_id = %s AND session_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            GROUP BY session_date
            ORDER BY session_date
        """
        return self.execute_query(query, (user_id, days), fetch=True)
    
    # ==================== NOTIFICATIONS ====================
    
    def add_notification(self, user_id, notification_type, message, priority='medium'):
        query = """
            INSERT INTO notifications (user_id, notification_type, message, priority)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (user_id, notification_type, message, priority))
    
    def get_notifications(self, user_id, limit=50):
        query = """
            SELECT * FROM notifications
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """
        return self.execute_query(query, (user_id, limit), fetch=True)

    def delete_notification(self, notification_id):
        query = "DELETE FROM notifications WHERE notification_id = %s"
        return self.execute_query(query, (notification_id,))
        
    def count_unread_notifications(self, user_id):
        query = "SELECT COUNT(*) as count FROM notifications WHERE user_id = %s AND is_read = 0"
        result = self.execute_query(query, (user_id,), fetch=True)
        return result[0]['count'] if result else 0
    
    def mark_notification_read(self, notification_id):
        query = "UPDATE notifications SET is_read = 1 WHERE notification_id = %s"
        return self.execute_query(query, (notification_id,))
    
    # ==================== QUICK NOTES ====================
    
    def add_note(self, user_id, title, content, subject_id=None):
        query = """
            INSERT INTO quick_notes (user_id, subject_id, note_title, note_content)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (user_id, subject_id, title, content))
    
    def get_user_notes(self, user_id):
        query = """
            SELECT n.*, s.subject_name
            FROM quick_notes n
            LEFT JOIN subjects s ON n.subject_id = s.subject_id
            WHERE n.user_id = %s
            ORDER BY n.is_pinned DESC, n.created_at DESC
        """
        return self.execute_query(query, (user_id,), fetch=True)
    
    def delete_note(self, note_id):
        query = "DELETE FROM quick_notes WHERE note_id = %s"
        return self.execute_query(query, (note_id,))
    
    # ==================== MOTIVATIONAL QUOTES ====================
    
    def get_random_quote(self):
        query = "SELECT * FROM motivational_quotes ORDER BY RAND() LIMIT 1"
        result = self.execute_query(query, fetch=True)
        return result[0] if result else None
    
    # ==================== SAVED STUDY PLANS ====================

    def save_ai_plan(self, user_id, plan_content):
        query = """
            INSERT INTO saved_study_plans (user_id, plan_content)
            VALUES (%s, %s)
        """
        return self.execute_query(query, (user_id, plan_content))

    def get_saved_ai_plans(self, user_id):
        query = """
            SELECT plan_id, plan_content, created_at
            FROM saved_study_plans
            WHERE user_id = %s
            ORDER BY created_at DESC
        """
        return self.execute_query(query, (user_id,), fetch=True)

    def delete_saved_plan(self, plan_id):
        query = "DELETE FROM saved_study_plans WHERE plan_id = %s"
        return self.execute_query(query, (plan_id,))

    def update_saved_plan(self, plan_id, new_content):
        query = "UPDATE saved_study_plans SET plan_content = %s WHERE plan_id = %s"
        return self.execute_query(query, (new_content, plan_id))

    # ==================== WEEKLY REPORTS ====================
    
    def generate_weekly_report(self, user_id):
        from datetime import datetime, timedelta
        
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        # Get weekly stats
        sessions = self.get_sessions_by_date_range(user_id, week_start, week_end) or []
        total_minutes = sum(s['duration_minutes'] for s in sessions)
        total_hours = total_minutes / 60
        
        # Subject performance
        subject_stats = {}
        for session in sessions:
            subj = session['subject_name']
            if subj not in subject_stats:
                subject_stats[subj] = 0
            subject_stats[subj] += session['duration_minutes']
        
        strongest = max(subject_stats, key=subject_stats.get) if subject_stats else 'N/A'
        weakest = min(subject_stats, key=subject_stats.get) if subject_stats else 'N/A'
        
        # Productivity score (0-100)
        expected_hours = 7 * 2  # 2 hours per day
        productivity_score = min(100, int((total_hours / expected_hours) * 100))
        
        query = """
            INSERT INTO weekly_reports 
            (user_id, week_start_date, week_end_date, total_study_hours, 
             total_sessions, productivity_score, strongest_subject, weakest_subject)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.execute_query(query, (user_id, week_start, week_end, total_hours, 
                                   len(sessions), productivity_score, strongest, weakest))
        
        return {
            'week_start': week_start,
            'week_end': week_end,
            'total_hours': total_hours,
            'total_sessions': len(sessions),
            'productivity_score': productivity_score,
            'strongest_subject': strongest,
            'weakest_subject': weakest,
            'subject_breakdown': subject_stats
        }
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def test_connection(self):
        try:
            connection = self.get_connection()
            if connection:
                print("✅ Database connection successful!")
                connection.close()
                return True
            else:
                print("❌ Database connection failed!")
                return False
        except Error as e:
            print(f"❌ Connection test failed: {e}")
            return False
    
    # ==================== REMINDERS ====================

    def add_reminder(self, user_id, message, reminder_time):
        query = """
            INSERT INTO reminders (user_id, message, reminder_time)
            VALUES (%s, %s, %s)
        """
        return self.execute_query(query, (user_id, message, reminder_time))

    def get_pending_reminders(self, user_id):
        # MySQL NOW()
        query = """
            SELECT * FROM reminders 
            WHERE user_id = %s AND status = 'pending' AND reminder_time <= NOW()
        """
        return self.execute_query(query, (user_id,), fetch=True)

    def mark_reminder_sent(self, reminder_id):
        query = "UPDATE reminders SET status = 'sent' WHERE reminder_id = %s"
        return self.execute_query(query, (reminder_id,))

    # ==================== SOCIAL / LEADERBOARD ====================

    def get_leaderboard(self, limit=10):
        query = """
            SELECT u.username, u.full_name, u.student_level,
                   COALESCE(SUM(s.duration_minutes), 0) as total_minutes
            FROM users u
            LEFT JOIN study_sessions s ON u.user_id = s.user_id
            GROUP BY u.user_id
            ORDER BY total_minutes DESC
            LIMIT %s
        """
        return self.execute_query(query, (limit,), fetch=True)

    # ==================== SOCIAL NOTIFICATIONS ====================

    def check_and_generate_social_notification(self, user_id):
        """Generate a motivational notification based on leaderboard stats"""
        # 1. Check if we already sent one recently (e.g., today)
        query_check = """
            SELECT COUNT(*) as count FROM notifications 
            WHERE user_id = %s 
            AND notification_type = 'social' 
            AND created_at >= CURDATE()
        """
        result = self.execute_query(query_check, (user_id,), fetch=True)
        if result and result[0]['count'] > 0:
            return # Already sent one today

        # 2. Get Top Student Stats
        leaders = self.get_leaderboard(limit=1)
        if not leaders:
            return

        top_student = leaders[0]
        if top_student['username'] == self.get_user_by_id(user_id)['username']:
             return # You are the top student!

        # 3. Create Message
        top_name = top_student['full_name'].split()[0] # First name
        top_minutes = int(top_student['total_minutes'])
        
        msg = f"🔥 {top_name} has studied for {top_minutes} mins today! Catch up!"
        
        # 4. Insert as immediate system notification/reminder
        # We insert into 'reminders' so it triggers a toast, OR notifications table?
        # The user requested an "alert", so reminder table is best for immediate toast.
        
        self.add_reminder(user_id, msg, datetime.now() + timedelta(seconds=10))
        
        # Log it in notifications table too for history
        self.add_notification(user_id, 'social', msg, 'high')

    # ==================== GLOBAL SEARCH ====================

    def search_everything(self, user_id, search_term):
        results = {}
        search_term = f"%{search_term}%"

        query_sub = "SELECT * FROM subjects WHERE user_id = %s AND subject_name LIKE %s"
        results['subjects'] = self.execute_query(query_sub, (user_id, search_term), fetch=True)

        query_notes = "SELECT * FROM quick_notes WHERE user_id = %s AND (note_title LIKE %s OR note_content LIKE %s)"
        results['notes'] = self.execute_query(query_notes, (user_id, search_term, search_term), fetch=True)

        query_chat = "SELECT * FROM chat_history WHERE user_id = %s AND (message LIKE %s OR response LIKE %s)"
        results['chat'] = self.execute_query(query_chat, (user_id, search_term, search_term), fetch=True)

        return results

    # ==================== ACCOUNT MANAGEMENT ====================

    def update_user_info(self, user_id, new_username, new_email, new_fullname):
        query = """
            UPDATE users
            SET username = %s, email = %s, full_name = %s
            WHERE user_id = %s
        """
        return self.execute_query(query, (new_username, new_email, new_fullname, user_id))

    def update_user_password(self, user_id, new_password):
        password_hash = self.hash_password(new_password)
        query = """
            UPDATE users
            SET password_hash = %s
            WHERE user_id = %s
        """
        return self.execute_query(query, (password_hash, user_id))

    def delete_user_account(self, user_id):
        query = "DELETE FROM users WHERE user_id = %s"
        return self.execute_query(query, (user_id,))

    # ==================== AI CONTEXT ====================

    def get_user_context(self, user_id):
        """Aggregate all user data for AI context"""
        context = {}
        
        # 1. User Profile
        user = self.get_user_by_id(user_id)
        if user:
            context['name'] = user['full_name']
            context['level'] = user.get('student_level', 'University')
            
        # 2. Subjects & Difficulty
        subjects = self.get_user_subjects(user_id) or []
        context['subjects'] = [
            f"{s['subject_name']} ({s.get('difficulty', 'Medium')})" 
            for s in subjects
        ]
        
        # 3. Study Stats
        sessions = self.get_user_sessions(user_id) or []
        total_mins = sum(s['duration_minutes'] for s in sessions)
        context['total_hours'] = round(total_mins / 60, 1)
        context['total_sessions'] = len(sessions)
        
        # Recent activity (Last 7 days)
        # We can calculate this from sessions list easily in python
        from datetime import datetime, timedelta
        one_week_ago = datetime.now().date() - timedelta(days=7)
        recent_mins = sum(
            s['duration_minutes'] for s in sessions 
            if isinstance(s['session_date'], str) or s['session_date'] >= one_week_ago
        )
        context['recent_hours'] = round(recent_mins / 60, 1)
        
        # 4. Weak/Strong Areas
        if sessions:
            subject_time = {}
            for s in sessions:
                name = s['subject_name']
                subject_time[name] = subject_time.get(name, 0) + s['duration_minutes']
            
            context['strongest_subject'] = max(subject_time, key=subject_time.get)
            context['weakest_subject'] = min(subject_time, key=subject_time.get)
        else:
            context['strongest_subject'] = "None yet"
            context['weakest_subject'] = "None yet"
            
        # 5. Goals
        goals = self.get_user_goals(user_id) or []
        active_goals = [
            f"{g['goal_type']} for {g.get('subject_name', 'General')}: {g['current_value']}/{g['target_value']}"
            for g in goals if g['status'] == 'active'
        ]
        context['goals'] = active_goals
        
        return context


# Create a global database instance
db = DatabaseManager()


# ==================== TEST FUNCTIONS ====================

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🧪 TESTING DATABASE MANAGER (MySQL)")
    print("="*50 + "\n")
    
    # Test connection
    print("1. Testing Connection...")
    db.test_connection()
    
    print("\n" + "="*50 + "\n")