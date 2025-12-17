from database import db
from datetime import datetime

def check_recent_reminders():
    print("🔍 Checking last 10 reminders in DB...")
    reminders = db.execute_query(
        "SELECT reminder_id, message, reminder_time, status, created_at FROM reminders ORDER BY reminder_id DESC LIMIT 10",
        fetch=True
    )
    
    if reminders:
        for r in reminders:
            print(f"[{r['reminder_id']}] Time: {r['reminder_time']} | Status: {r['status']} | Msg: {r['message'][:50]}...")
    else:
        print("❌ No reminders found.")

    print("\n🔍 Checking DB Time vs Python Time...")
    db_time = db.execute_query("SELECT NOW() as db_now", fetch=True)[0]['db_now']
    py_time = datetime.now()
    print(f"DB Time: {db_time}")
    print(f"Py Time: {py_time}")

if __name__ == "__main__":
    check_recent_reminders()
