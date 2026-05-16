import smtplib
import csv
import os
import time
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ── Only change these two ────────────────────────────────────────────────────

sender_email = "srthakrahane@gmail.com"
password     = "gqut srpc bnwt buyt"

# ── Everything below is ready to go ─────────────────────────────────────────

subject = "Internship Update from Syntecxhub"

body_template = """Hi {name},

Hope you're doing well!;

I'm Sarthak, currently interning at Syntecxhub as a Python Developer.
As part of my internship Task 3, I'm sharing a quick project update with you.

This email was sent automatically using Python (smtplib) as part of
the Email Sender Bot project.

Feel free to reply if you have any questions.

Best regards,
Sarthak
Python Intern | Syntecxhub"""

# Sample recipients — already filled in for you
recipients = [
    {"email": "hyperstone81@gmail.com",  "name": "Sarthak"},
    {"email": "sarthakrahane06@gmail.com","name": "Nagi"},
    {"email": "yoichinagumo0081@gmail.com",     "name": "Nagumo"},
]

# ── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    filename="email_log.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ── Build Message ─────────────────────────────────────────────────────────────

def build_message(recipient):
    msg = MIMEMultipart()
    msg["From"]    = sender_email
    msg["To"]      = recipient["email"]
    msg["Subject"] = subject
    body = body_template.format(name=recipient["name"])
    msg.attach(MIMEText(body, "plain"))
    return msg

# ── Send with Retry ───────────────────────────────────────────────────────────

def send_email(server, recipient, retries=3):
    email_addr = recipient["email"]
    name       = recipient["name"]

    for attempt in range(1, retries + 1):
        try:
            msg = build_message(recipient)
            server.sendmail(sender_email, email_addr, msg.as_string())
            print(f"[OK]  Email sent to {name} <{email_addr}>")
            logging.info(f"Sent to {name} <{email_addr}>")
            return
        except Exception as e:
            print(f"[RETRY {attempt}/{retries}] Failed for {email_addr}: {e}")
            logging.warning(f"Attempt {attempt} failed for {email_addr}: {e}")
            time.sleep(5)

    print(f"[FAIL] Could not send to {email_addr} after {retries} attempts.")
    logging.error(f"Failed after {retries} attempts: {email_addr}")

# ── Main ──────────────────────────────────────────────────────────────────────

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(sender_email, password)
    print("Login successful. Sending emails...\n")
    logging.info("Login successful.")

    for recipient in recipients:
        send_email(server, recipient)
        time.sleep(1)

print("\nDone! Check email_log.log for details.")