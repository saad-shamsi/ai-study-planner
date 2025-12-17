
from database import db
from config import DB_CONFIG

# Test Connection
print("Testing DB Connection...")
print(db.test_connection())

# Test User
print("\nTesting User Fetch...")
user = db.verify_user("saad", "root") # Assuming user is Saad based on screenshot, pass is hardcoded from context or we can fetch any user
if not user:
    # Try to find any user if saad doesn't exist
    print("User 'saad' not found with password 'root', trying to fetch any user...")
    users = db.execute_query("SELECT * FROM users LIMIT 1", fetch=True)
    if users:
        user = users[0]
        print(f"Found user: {user['username']}")
    else:
        print("No users found!")
        exit()

# Test Chat History
print(f"\nTesting Chat History for user {user['user_id']}...")
try:
    history = db.get_chat_history(user['user_id'])
    print(f"Chat history retrieved. Count: {len(history)}")
    for chat in history:
        print(f"- {chat['message'][:20]}...")
except Exception as e:
    print(f"FAILED to get chat history: {e}")

# Test Groq
from groq_service import groq_ai
print(f"\nGroq Available: {groq_ai.is_available}")
