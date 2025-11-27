import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables")


genai.configure(api_key=GEMINI_API_KEY)

GEMINI_MODEL_NAME = "gemini-2.5-flash"  

def build_ticket_prompt(ticket_data: dict) -> str:
    """
    Build a clear, structured prompt for Gemini
    using the incoming webhook (ticket) data.
    """
    ticket_id = ticket_data.get("ticket_id") or ""
    subject = ticket_data.get("subject") or ""
    description = ticket_data.get("description") or ""
    requester_name = ticket_data.get("requester_name") or ""
    priority = ticket_data.get("priority") or ""
    from_email = ticket_data.get("from_email") or ""

    prompt = f"""
You are an IT helpdesk support agent replying to a user via email.

Write a clear, polite, and professional response to the support ticket.

Instructions:
- Start with a short greeting using the requester’s name if available.
- Acknowledge the issue briefly in your own words.
- If extra information is needed, ask only one relevant question.
- Offer 2–4 helpful troubleshooting steps or guidance.
- Avoid asking multiple questions.
- Keep the response short, friendly, and professional (4–6 sentences).
- Use simple, clear English. No slang or unnecessary technical terms.
- Do not create a ticket number; only use it if it exists.


Ticket details:
- Ticket ID: {ticket_id}
- Priority: {priority}
- Requester name: {requester_name}
- Requester email: {from_email}
- Subject: {subject}
- Description: {description}
"""
    return prompt.strip()


def generate_ticket_reply(ticket_data: dict) -> str:
    """
    Generate a reply for the ticket using Gemini.
    Returns a plain text response string.
    """
    prompt = build_ticket_prompt(ticket_data)

    model = genai.GenerativeModel(GEMINI_MODEL_NAME)

    try:
        response = model.generate_content(prompt)
        reply_text = (response.text or "").strip()
    except Exception as e:
        print("Error calling Gemini:", e)
        reply_text = (
            "Thank you for reaching out. We have received your ticket and our team "
            "will review your issue shortly. If possible, please share any additional "
            "details or screenshots that might help us troubleshoot."
        )

    if not reply_text:
        reply_text = (
            "Thank you for your message. Our support team has received your request "
            "and will get back to you as soon as possible."
        )

    return reply_text
