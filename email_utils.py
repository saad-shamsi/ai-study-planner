import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_CONFIG

def generate_otp(length=6):
    """Generate a numeric OTP of specified length."""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(to_email, otp):
    """
    Send an OTP email to the specified address.
    
    Args:
        to_email (str): The recipient's email address.
        otp (str): The One-Time Password to send.
        
    Returns:
        bool: True if sent successfully, False otherwise.
    """
    sender_email = EMAIL_CONFIG['email_address']
    sender_password = EMAIL_CONFIG['email_password']
    smtp_server = EMAIL_CONFIG['smtp_server']
    smtp_port = EMAIL_CONFIG['smtp_port']
    
    # 1. Check if user has configured credentials
    if "YOUR_EMAIL" in sender_email or "YOUR_APP_PASSWORD" in sender_password:
        print("❌ ERROR: Email credentials not configured in config.py")
        return False

    message = MIMEMultipart()
    message["From"] = f"AI Study Planner <{sender_email}>"
    message["To"] = to_email
    message["Subject"] = "Your Verification Code - AI Study Planner"

    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
          <h2 style="color: #38BDF8; text-align: center;">Verify Your Identity</h2>
          <p>Hello,</p>
          <p>Use the following code to verify your account integration with AI Study Planner:</p>
          <div style="text-align: center; margin: 30px 0;">
            <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #1E293B; background-color: #F1F5F9; padding: 10px 20px; border-radius: 5px;">{otp}</span>
          </div>
          <p>This code will expire shortly. Do not share this code with anyone.</p>
          <br>
          <p style="font-size: 12px; color: #94A3B8; text-align: center;">AI Study Planner Security Team</p>
        </div>
      </body>
    </html>
    """
    
    message.attach(MIMEText(body, "html"))

    try:
        if not sender_email or not sender_password:
             print("❌ ERROR: Email credentials empty")
             return False

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()
        print(f"✅ OTP sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

if __name__ == "__main__":
    # Test
    print("Test OTP Generation:", generate_otp())
