import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_pension_email(receiver_email, pensioner_name,
                       certificate_id, rejection_reason):
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("SENDER_APP_PASSWORD")
    
    if not sender_email or not app_password:
        return False, "Gmail settings are missing in .env."
        
    message = EmailMessage()
    message["Subject"] = "Life Certificate Submission Notification"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    message.set_content(f"""
Dear {pensioner_name},

Your Life Certificate submission was rejected
by the local demonstration verification rules.
Certificate ID: {certificate_id}
Reason: {rejection_reason}

Please verify the information using your original
PPO document and contact your bank or pension
authority if you need official confirmation.

This is an educational demo application.

Regards,
Pension Assistance System
""")
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(message)
        return True, "Email sent successfully."
    except Exception as error:
        return False, f"Email could not be sent: {error}"