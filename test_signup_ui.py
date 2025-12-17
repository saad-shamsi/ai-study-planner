import customtkinter as ctk
from signup import SignupWindow
import unittest

class TestSignupLogic(unittest.TestCase):
    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.app = SignupWindow(self.root)
        self.app.withdraw() # Don't show

    def test_widgets_exist(self):
        print("\n🖥️ Checking Widgets...")
        self.assertIsNotNone(self.app.password_entry)
        self.assertIsNotNone(self.app.req_frame)
        self.assertTrue(len(self.app.req_labels) == 3)
        print("✅ UI Components created successfully")

    def test_password_logic(self):
        print("\n🔐 Testing Password Validation Logic...")
        
        # 1. Too short
        self.app.password_entry.insert(0, "Short1!")
        self.assertFalse(self.app.check_password_strength())
        print("✅ Detected short password")
        
        # 2. No Upper
        self.app.password_entry.delete(0, 'end')
        self.app.password_entry.insert(0, "longpassword1!")
        self.assertFalse(self.app.check_password_strength())
        print("✅ Detected missing uppercase")

        # 3. No Special
        self.app.password_entry.delete(0, 'end')
        self.app.password_entry.insert(0, "LongPassword123")
        self.assertFalse(self.app.check_password_strength())
        print("✅ Detected missing special char")

        # 4. Valid
        self.app.password_entry.delete(0, 'end')
        self.app.password_entry.insert(0, "GoodPass1!")
        self.assertTrue(self.app.check_password_strength())
        print("✅ Accepted valid password")

    def tearDown(self):
        self.app.destroy()
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
