import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")


def send_reminder_email(to_email: str, title: str, message: str, remind_at: datetime) -> bool:
    """
    Send a reminder email. Returns True on success, False on failure.
    If SMTP credentials are not configured, logs the email to console (dev mode).
    """
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        # Dev mode: print instead of sending
        print(f"\n{'='*50}")
        print(f"[DEV MODE] Email would be sent to: {to_email}")
        print(f"Subject: Reminder: {title}")
        print(f"Scheduled for: {remind_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print(f"Message: {message}")
        print(f"{'='*50}\n")
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"⏰ Reminder: {title}"
        msg["From"] = SMTP_USERNAME
        msg["To"] = to_email

        # Plain text version
        text_body = f"""
Hello!

This is your scheduled reminder.

📌 {title}

{message}

Scheduled for: {remind_at.strftime('%Y-%m-%d %H:%M:%S')} UTC

---
Sent by Reminder API
        """.strip()

        # HTML version
        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
            <div style="background: #f0f4ff; border-radius: 8px; padding: 24px;">
              <h2 style="color: #3b5bdb;">⏰ Reminder: {title}</h2>
              <p style="font-size: 16px; color: #333;">{message}</p>
              <hr style="border: none; border-top: 1px solid #ddd;" />
              <p style="color: #888; font-size: 13px;">
                Scheduled for: {remind_at.strftime('%Y-%m-%d %H:%M:%S')} UTC
              </p>
            </div>
          </body>
        </html>
        """

        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, to_email, msg.as_string())

        print(f"[EMAIL SENT] To: {to_email} | Subject: Reminder: {title}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("[EMAIL ERROR] Authentication failed. Check SMTP_USERNAME and SMTP_PASSWORD.")
        return False
    except smtplib.SMTPException as e:
        print(f"[EMAIL ERROR] SMTP error: {e}")
        return False
    except Exception as e:
        print(f"[EMAIL ERROR] Unexpected error: {e}")
        return False