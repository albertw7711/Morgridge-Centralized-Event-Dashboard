# 1. Turn on IMAP in settings. in IMAP I did this . When messages are accessed with POP mark Gmail's copy as read
# 2. Turn on 2FA
# 3. Go to https://myaccount.google.com/apppasswords
# 4. Enter App name and get the 16 digit key
# 5. Update everthing in the .env file
# 6. Run python3 emailScraper.py
# 7. The [✗] error is expected for now because the backend server isn't running yet.

import imaplib
import email
from email.header import decode_header
import requests
import os
from dotenv import load_dotenv
load_dotenv()

import re
import json
from datetime import datetime, timezone
import asyncio
from google import genai
# --------------
# CONFIG
# --------------

EMAIL_HOST     = "imap.gmail.com"
EMAIL_PORT     = 993
EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_FOLDER   = "inbox" # folder/label to scrape
UNREAD_ONLY    = True    # set False to scrape all emails

BACKEND_URL    = os.getenv("BACKEND_URL", "http://localhost:5005/insert")

# --------------
# HELPERS
# --------------

def decode_mime_words(s):
    # Convert encoded email headers into readable text.
    if s is None:
        return ""
    parts = decode_header(s)
    decoded = []
    for part, enc in parts:
        if isinstance(part, bytes):
            decoded.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            decoded.append(part)
    return " ".join(decoded)


import io
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

def extract_pdf_text(payload_bytes):
    if not PyPDF2:
        return "[PyPDF2 not installed, cannot extract PDF text]"
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(payload_bytes))
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        print(f"  [!] Failed to extract PDF: {e}")
        return ""

def get_body(msg):
    # Get the plain text content from an email message
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition  = str(part.get("Content-Disposition", ""))
            filename = part.get_filename()

            if content_type == "text/plain" and "attachment" not in disposition:
                charset = part.get_content_charset() or "utf-8"
                body += part.get_payload(decode=True).decode(charset, errors="replace") + "\n"

            # Parse PDF attachments
            if content_type == "application/pdf" or (filename and filename.lower().endswith('.pdf')):
                pdf_bytes = part.get_payload(decode=True)
                if pdf_bytes:
                    print(f"  [*] Found PDF attachment: {filename}")
                    pdf_text = extract_pdf_text(pdf_bytes)
                    if pdf_text.strip():
                        body += f"\n\n--- PDF Attachment ({filename}) ---\n{pdf_text}\n--------------------------\n"

    else:
        charset = msg.get_content_charset() or "utf-8"
        body = msg.get_payload(decode=True).decode(charset, errors="replace")
    return body.strip()

async def build_payload(msg, client):
    # Transform an email message into a dictionary for the backend.
    subject     = decode_mime_words(msg.get("Subject", "(no subject)"))
    sender      = decode_mime_words(msg.get("From", ""))
    message_id  = msg.get("Message-ID", "")
    sent_date   = msg.get("Date", str(datetime.now(timezone.utc)))
    body        = get_body(msg)

    # Use LLM summarizer
    try:
        from utils.llmScraper import summarizer
        summary = await summarizer(client, f"Subject: {subject}\n\n{body}")
        
        # If the LLM determines this is not an event, discard it
        if not summary.get("is_event", True):
            return None

        location = summary.get("location")
        event_date = summary.get("start_date_time", sent_date)
        duration = summary.get("duration")
        food = summary.get("food", "No")
    except Exception as e:
        print(f"  [!] LLM summarization failed: {e}")
        return None

    payload = {
        # Matches the backend schema defined in app.py
        "name":        subject,
        "description": body,
        "start":       event_date,
        "location":    location,
        "duration":    duration,
        "food":        food,
        "media":       [],
    }
    return payload

# --------------
# SCRAPER
# --------------

def connect(host, port, user, password):
    mail = imaplib.IMAP4_SSL(host, port)
    mail.login(user, password)
    return mail


def fetch_messages(mail, folder="inbox", unread_only=True):
    # Return all email messages from the specified folder.
    mail.select(folder)
    search_criterion = "(UNSEEN)" if unread_only else "ALL"
    status, data = mail.search(None, search_criterion)

    if status != "OK":
        print(f"[!] Failed to search mailbox: {status}")
        return []

    message_ids = data[0].split()
    print(f"[*] Found {len(message_ids)} email(s) to process.")

    messages = []
    for mid in message_ids:
        status, msg_data = mail.fetch(mid, "(RFC822)")
        if status != "OK":
            print(f"[!] Failed to fetch message {mid}")
            continue
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)
        messages.append(msg)

    return messages


def post_event(payload, url):
    # Send a single event payload to the backend using POST
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code in (200, 201):
            print(f"  [✓] Posted OK  — '{payload['name'][:60]}'")
        else:
            print(f"  [✗] Backend returned {response.status_code}: {response.text[:200]}")
        return response
    except requests.exceptions.ConnectionError:
        print(f"  [✗] Could not connect to backend at {url}")
        print("      Is the Flask server running?")
        return None
    except Exception as e:
        print(f"  [✗] Unexpected error: {e}")
        return None


async def run():
    print("=" * 50)
    print("  Email Scraper — UPL Event Aggregator")
    print("=" * 50)
    # 1. Connect
    print(f"\n[*] Connecting to {EMAIL_HOST} as {EMAIL_USER} ...")
    try:
        mail = connect(EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD)
        print("[✓] Connected.")
    except imaplib.IMAP4.error as e:
        print(f"[✗] Login failed: {e}")
        print("    Check EMAIL_USER / EMAIL_PASSWORD and that IMAP is enabled.")
        return
    # 2. Fetch emails
    messages = fetch_messages(mail, folder=EMAIL_FOLDER, unread_only=UNREAD_ONLY)
    if not messages:
        print("[*] No messages to process. Done.")
        mail.logout()
        return
    # 3. Parse and POST each one
    print(f"\n[*] Sending to backend: {BACKEND_URL}\n")
    results = {"success": 0, "failed": 0}
    
    # Initialize Gemini client
    try:
        from config import GEMINI_API_KEY
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"[!] Failed to initialize Gemini Client: {e}")
        return

    for msg in messages:
        payload = await build_payload(msg, client)
        
        if not payload:
            print("-" * 40)
            print(f"  [!] Skipping: '{msg.get('Subject', '(no subject)')}' (Not an event)")
            # Wait 4 seconds to avoid hitting Gemini Free Tier rate limits (15 RPM)
            await asyncio.sleep(4.5)
            continue

        # debug: print payload before sending
        print("-" * 40)
        print(f"  Name    : {payload['name'][:70]}")
        # Debug print
        print(f"  Start   : {payload['start']}")
        print(f"  Location: {payload['location']}")
        print(f"  Food?   : {payload['food']}")
        print(f"  Body    : {payload['description'][:80].replace(chr(10), ' ')}...")

        resp = post_event(payload, BACKEND_URL)
        if resp and resp.status_code in (200, 201):
            results["success"] += 1
        else:
            results["failed"] += 1
            
        # Wait to avoid Gemini API 429 Resource Exhausted errors
        print("  [*] Sleeping for 4.5s for rate limit...")
        await asyncio.sleep(4.5)

    # 4. Summary
    print("\n" + "=" * 50)
    print(f"  Done. ✓ {results['success']} posted  ✗ {results['failed']} failed")
    print("=" * 50)

    mail.logout()


# --------------
#  ENTRY POINT
# --------------

if __name__ == "__main__":
    asyncio.run(run())