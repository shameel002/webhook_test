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

Write a clear, professional email response using clean HTML format.
The response must adapt to the situation:
If the issue requires user action, provide clear step-by-step instructions.
If the issue requires IT-side action (installation, configuration, fix handled by IT), clearly state that the issue will be taken care of and an agent will be with you shortly, and briefly explain what is being handled or monitored, without requesting any action from the user.

Formatting Rules (very important):
- Do NOT include greeting or closing (they are added separately).
- Use <br> for normal line breaks.
- do  not ask for reply to  this email
- Use <br><br> only when you want to separate sections, specifically:
    • After the opening acknowledgement sentence.
    • After headings like "Please try these steps:".
    • Before the final sentence (closing support line).
- You may use <b> only for headings or emphasis.
- Do NOT use <p>, <div>, <span>, bullet points, hyphens, or extra HTML tags.
- Use numbered steps like 1), 2), 3),4),5) with <br> after each.
- DO NOT ask to open new ticket, tell politely to close the ticket if the issue is resolved
- Do NOT ask any question only provide clear instructios on what to do now.
- Keep response between 70–130 words.
- Must be safe to directly insert into an HTML email template.
- Must look visually organized even if copied as plain text.

Ticket details:
- Requester name: {requester_name}
- Requester email: {from_email}
- Ticket ID: {ticket_id}
- Priority: {priority}
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









