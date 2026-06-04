import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


# ──────────────────────────────────────────────
# Configure these via environment variables or a .env file
# ──────────────────────────────────────────────
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "your_email@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_app_password")
SENDER_NAME = os.getenv("SENDER_NAME", "Reminder App")


def build_html_email(title: str, message: str, remind_at: datetime) -> str:
    """Return a nicely formatted HTML email body."""
    formatted_time = remind_at.strftime("%A, %B %d %Y at %I:%M %p")
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; background:#f4f4f4; padding:30px;">
        <div style="max-width:600px; margin:auto; background:white;
                    border-radius:8px; padding:30px; box-shadow:0 2px 8px rgba(0,0,0,.1);">
          <h2 style="color:#4f46e5;">⏰ Reminder: {title}</h2>
          <hr style="border:none; border-top:1px solid #eee;">
          <p style="font-size:16px; color:#333;">{message}</p>
          <p style="color:#888; font-size:13px;">Scheduled for: <strong>{formatted_time}</strong></p>
          <div style="margin-top:30px; padding:15px; background:#f0f0ff;
                      border-left:4px solid #4f46e5; border-radius:4px;">
            <p style="margin:0; color:#4f46e5; font-size:13px;">
              This reminder was sent automatically by Reminder API.
            </p>
          </div>
        </div>
      </body>
    </html>
    """


def send_reminder_email(to_email: str, title: str, message: str, remind_at: datetime) -> bool:
    """
    Send a reminder email via SMTP.
    Returns True on success, False on failure.
    """
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"⏰ Reminder: {title}"
        msg["From"] = f"{SENDER_NAME} <{SMTP_USER}>"
        msg["To"] = to_email

        # Plain text fallback
        plain_text = f"Reminder: {title}\n\n{message}\n\nScheduled for: {remind_at}"
        msg.attach(MIMEText(plain_text, "plain"))

        # HTML version
        html_body = build_html_email(title, message, remind_at)
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())

        print(f"[EMAIL] ✅ Sent to {to_email} — '{title}'")
        return True

    except smtplib.SMTPAuthenticationError:
        print("[EMAIL] ❌ SMTP authentication failed. Check SMTP_USER / SMTP_PASSWORD.")
        return False
    except smtplib.SMTPException as e:
        print(f"[EMAIL] ❌ SMTP error: {e}")
        return False
    except Exception as e:
        print(f"[EMAIL] ❌ Unexpected error: {e}")
        return False