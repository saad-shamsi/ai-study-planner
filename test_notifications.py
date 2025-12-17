from database import db
from datetime import datetime, timedelta
import time
from plyer import notification

def test_db_reminder_hook():
    print("🧪 Testing Database Reminder Hook...")
    user_id = 1 # Assuming user 1 exists
    
    # 1. Add Session 5 mins from now
    now = datetime.now()
    future_time = now + timedelta(minutes=6) # 6 mins from now, so 5 mins before is +1 min
    
    session_date = future_time.date()
    start_time = future_time.strftime("%H:%M")
    end_time = (future_time + timedelta(hours=1)).strftime("%H:%M")
    
    print(f"Adding session for {session_date} {start_time}")
    db.add_study_session(user_id, 1, session_date, start_time, end_time, 60, "Test Notification Session")
    
    # 2. Check Reminders
    print("Checking reminders...")
    # Since reminder is for 5 mins BEFORE session, it should be at T+1 min.
    # get_pending_reminders checks if reminder_time <= NOW(). 
    # Reminder time is T+1 min, so NOW it is NOT pending yet.
    
    # Let's manually check the table
    entry = db.execute_query("SELECT * FROM reminders WHERE message LIKE '%Test Notification Session%' ORDER BY reminder_id DESC LIMIT 1", fetch=True)
    
    if entry:
        print(f"✅ Reminder created successfully: {entry[0]['reminder_time']}")
        
        # Verify time: should be roughly 1 min from now (5 min before 6 min future)
        rem_time = entry[0]['reminder_time']
        diff = rem_time - now
        print(f"Reminder scheduled in: {diff}")
    else:
        print("❌ Reminder NOT created!")

def test_plyer():
    print("\n🔔 Testing System Notification...")
    try:
        notification.notify(
            title="Test Notification",
            message="This is a test from the verification script.",
            app_name="AI Study Planner",
            timeout=5
        )
        print("✅ Notification sent to system.")
    except Exception as e:
        print(f"❌ Notification failed: {e}")

if __name__ == "__main__":
    test_db_reminder_hook()
    test_plyer()
