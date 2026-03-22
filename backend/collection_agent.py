import os
import json
import smtplib
from datetime import datetime
from typing import TypedDict
from langgraph.graph import StateGraph
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()

class LoanState(TypedDict):
    status: str
    payment_received: bool
    email_sent: bool
    last_action_time: str
    log: list

def generate_pdf_notice(state):
    """Generate a PDF notice with loan details."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="OFFICIAL LOAN PAYMENT NOTICE", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(200, 10, txt=f"Loan Status: {state['status']}", ln=True)
    pdf.cell(200, 10, txt="Account Holder: Nik Raival", ln=True) # Placeholder or from state
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Notice Details:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 10, txt="This is a formal notification regarding your outstanding loan payment. "
                               "Please ensure the payment is made promptly to avoid further escalations.")
    
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="Generated automatically by CredServe", ln=True, align='C')
    
    os.makedirs("notices", exist_ok=True)
    file_path = f"notices/notice_{state['status']}_{datetime.now().strftime('%H%M%S')}.pdf"
    pdf.output(file_path)
    return file_path

def send_email(subject, body, to_email, attachment_path=None):
    """Simulated or actual email sending with attachments."""
    user = os.getenv("SMTP_USER", "mock_user")
    password = os.getenv("SMTP_PASS", "mock_password")
    server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    port = os.getenv("SMTP_PORT", "587")

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(attachment_path)}",
            )
            msg.attach(part)

    if user != "mock_user":
        try:
            with smtplib.SMTP(server, int(port)) as s:
                s.starttls()
                s.login(user, password)
                s.send_message(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    else:
        print(f"SIMULATED EMAIL: Subject={subject}, To={to_email}, Attached={attachment_path}")
        return True

def reminder(state):
    state["last_action_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state["log"].append(f"Reminder process started for status {state['status']}")
    return state

def email_node(state):
    if not state["payment_received"] and not state["email_sent"]:
        # Generate PDF Notice
        pdf_path = generate_pdf_notice(state)
        
        subject = f"Urgent: Loan Payment Notice for {state['status']}"
        body = f"Attached is the official notice regarding your loan status: {state['status']}."
        
        sent = send_email(subject, body, "nikraval03@gmail.com", attachment_path=pdf_path)
        if sent:
            state["email_sent"] = True
            state["log"].append(f"PDF notice generated and email sent to nikraval03@gmail.com at {datetime.now().strftime('%H:%M:%S')}")
    return state

def check_payment(state):
    if state["payment_received"]:
        state["status"] = "CLOSED"
        state["log"].append("Payment verified. Case closed.")
    return state

def voice_call(state):
    if not state["payment_received"]:
        state["log"].append("Voice call scheduled due to no response.")
    return state

# Setup Graph
graph = StateGraph(LoanState)

graph.add_node("reminder", reminder)
graph.add_node("email_node", email_node)
graph.add_node("check_payment", check_payment)
graph.add_node("voice_call", voice_call)

graph.set_entry_point("reminder")
graph.add_edge("reminder", "email_node")
graph.add_edge("email_node", "check_payment")
graph.add_edge("check_payment", "voice_call")

app = graph.compile()

def run_agent():
    state = {
        "status": "D+3",
        "payment_received": False,
        "email_sent": False,
        "last_action_time": "",
        "log": []
    }

    result = app.invoke(state)

    os.makedirs("logs", exist_ok=True)
    with open("logs/agent_logs.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    return result