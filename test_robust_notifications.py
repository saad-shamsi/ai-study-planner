from database import db
from datetime import datetime, timedelta
import time

def test_robust_reminders():
    print("\n🧪 Testing Robust Reminders...")
    user_id = 1
    
    # 1. Add Session for 1 hour from now (Using AM/PM format)
    now = datetime.now()
    start_dt = now + timedelta(minutes=60)
    session_date = start_dt.date()
    
    # Convert to AM/PM format (e.g., 04:30 PM)
    start_time = start_dt.strftime("%I:%M %p")
    end_time = (start_dt + timedelta(minutes=60)).strftime("%I:%M %p")
    
    print(f"Adding session: {session_date} {start_time}")
    db.add_study_session(user_id, 1, session_date, start_time, end_time, 60, "Robust Test Session")
    
    # 2. Check Reminders
    # We expect 3 reminders created recently for this message
    reminders = db.execute_query(
        "SELECT * FROM reminders WHERE message LIKE '%Robust Test Session%' ORDER BY reminder_id DESC LIMIT 3", 
        fetch=True
    )
    
    if len(reminders) == 3:
        print("✅ Success: 3 Reminders created!")
        for r in reminders:
            print(f" - {r['reminder_time']}: {r['message']}")
    else:
        print(f"❌ Failed: Found {len(reminders)} reminders")

def test_social_notification():
    print("\n🧪 Testing Social Notification...")
    user_id = 1
    
    # Attempt to generate
    db.check_and_generate_social_notification(user_id)
    
    # Check if created
    # Note: It might fail if no other users or if you are top student, but code should run without error
    reminders = db.execute_query(
        "SELECT * FROM reminders WHERE message LIKE '%studied for%' ORDER BY reminder_id DESC LIMIT 1",
        fetch=True
    )
    
    if reminders:
        print(f"✅ Social Reminder created: {reminders[0]['message']}")
    else:
        print("ℹ️ No social reminder created (might be top student or no data)")

if __name__ == "__main__":
    test_robust_reminders()
    test_social_notification()
