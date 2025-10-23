"""
Email utilities for the AI Agent System
Provides functionality equivalent to PHPMailer in the original PHP implementation
"""

import smtplib
import os
import requests
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import ssl

class Mailer:
    """A Python equivalent of PHPMailer for sending emails"""
    
    def __init__(self):
        self.smtp_host = ""
        self.smtp_port = 587
        self.smtp_username = ""
        self.smtp_password = ""
        self.smtp_secure = None  # 'tls', 'ssl', or None
        self.from_email = ""
        self.from_name = ""
        self.to_addresses = []
        self.cc_addresses = []
        self.bcc_addresses = []
        self.subject = ""
        self.body = ""
        self.is_html = False
        self.attachments = []
        
    def is_smtp(self):
        """Enable SMTP usage"""
        pass  # In Python, we always use SMTP when sending via SMTP server
        
    def set_smtp_options(self, host, port, username, password, secure=None):
        """Set SMTP configuration"""
        self.smtp_host = host
        self.smtp_port = port
        self.smtp_username = username
        self.smtp_password = password
        self.smtp_secure = secure
        
    def set_from(self, email, name=""):
        """Set sender email and name"""
        self.from_email = email
        self.from_name = name
        
    def add_address(self, email, name=""):
        """Add recipient email"""
        self.to_addresses.append((email, name))
        
    def add_cc(self, email, name=""):
        """Add CC recipient"""
        self.cc_addresses.append((email, name))
        
    def add_bcc(self, email, name=""):
        """Add BCC recipient"""
        self.bcc_addresses.append((email, name))
        
    def set_subject(self, subject):
        """Set email subject"""
        self.subject = subject
        
    def set_body(self, body, is_html=False):
        """Set email body"""
        self.body = body
        self.is_html = is_html
        
    def add_attachment(self, file_path, filename=None):
        """Add attachment to email"""
        if os.path.exists(file_path):
            self.attachments.append((file_path, filename or os.path.basename(file_path)))
            
    def send(self):
        """Send the email"""
        try:
            # Create message
            msg = MIMEMultipart()
            
            # Set headers
            from_header = f"{self.from_name} <{self.from_email}>" if self.from_name else self.from_email
            msg['From'] = from_header if from_header else ""
            msg['Subject'] = self.subject
            
            # Add recipients
            if self.to_addresses:
                msg['To'] = ', '.join([addr[0] for addr in self.to_addresses])
            if self.cc_addresses:
                msg['Cc'] = ', '.join([addr[0] for addr in self.cc_addresses])
            if self.bcc_addresses:
                msg['Bcc'] = ', '.join([addr[0] for addr in self.bcc_addresses])
            
            # Add body
            body_type = 'html' if self.is_html else 'plain'
            msg.attach(MIMEText(self.body, body_type))
            
            # Add attachments
            for file_path, filename in self.attachments:
                with open(file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}',
                )
                msg.attach(part)
            
            # Create SMTP session
            if self.smtp_secure == 'ssl':
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context)
            else:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                if self.smtp_secure == 'tls':
                    server.starttls()
                    
            # Login and send
            server.login(self.smtp_username, self.smtp_password)
            text = msg.as_string()
            
            # Send to all recipients
            all_recipients = [addr[0] for addr in self.to_addresses + self.cc_addresses + self.bcc_addresses]
            server.sendmail(self.from_email, all_recipients, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

# Function to send email using Brevo API (updated to use API instead of SMTP)
def send_email_brevo(to, subject, html_content, api_key, sender_email, sender_name):
    """
    Send email using Brevo API (equivalent to the PHP function)
    """
    try:
        # Use Brevo API instead of SMTP for better reliability
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "api-key": api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "sender": {
                "name": sender_name,
                "email": sender_email
            },
            "to": [
                {
                    "email": to,
                    "name": to.split('@')[0] if '@' in to else "User"
                }
            ],
            "subject": subject,
            "htmlContent": html_content
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code in [200, 201]:
            return True
        else:
            print(f"Error sending email via Brevo API: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending email via Brevo: {str(e)}")
        return False

# Function to generate OTP email template (equivalent to PHP function)
def get_otp_email_template(otp_code, type='verification'):
    """
    Generate beautiful OTP email template (equivalent to the PHP function)
    """
    if type == 'reset':
        title = "Password Reset Code"
        message = "Your password reset code for AI Agent System"
    else:
        title = "Email Verification Code"
        message = "Your verification code for AI Agent System"
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background: #0c0c17; color: #fff; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: rgba(12, 12, 23, 0.9); border: 1px solid #00ff9d; border-radius: 10px; padding: 30px; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .logo {{ font-size: 2.5rem; color: #00ff9d; margin-bottom: 10px; }}
            .title {{ font-size: 1.5rem; color: #00ff9d; margin-bottom: 10px; }}
            .otp-code {{ background: rgba(0, 255, 157, 0.1); border: 2px solid #00ff9d; border-radius: 8px; padding: 20px; text-align: center; font-size: 2rem; font-weight: bold; letter-spacing: 5px; margin: 20px 0; color: #00ff9d; }}
            .footer {{ margin-top: 30px; text-align: center; font-size: 0.8rem; color: #888; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🤖 AI AGENT SYSTEM</div>
                <h1 class="title">{title}</h1>
            </div>
            <p>Hello,</p>
            <p>{message}</p>
            <div class="otp-code">{otp_code}</div>
            <p>This code will expire in 10 minutes. Please do not share this code with anyone.</p>
            <div class="footer">
                <p>If you didn't request this code, please ignore this email.</p>
                <p>&copy; 2024 AI Agent System. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>'''

# Function to generate schedule confirmation email template
def get_schedule_confirmation_email_template(user_name, course_name, schedule_details):
    """
    Generate beautiful schedule confirmation email template
    """
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background: #0c0c17; color: #fff; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: rgba(12, 12, 23, 0.9); border: 1px solid #00ff9d; border-radius: 10px; padding: 30px; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .logo {{ font-size: 2.5rem; color: #00ff9d; margin-bottom: 10px; }}
            .title {{ font-size: 1.5rem; color: #00ff9d; margin-bottom: 10px; }}
            .course-info {{ background: rgba(0, 255, 157, 0.1); border: 2px solid #00ff9d; border-radius: 8px; padding: 20px; margin: 20px 0; }}
            .schedule-details {{ background: rgba(0, 255, 157, 0.05); border-radius: 8px; padding: 15px; margin: 15px 0; }}
            .detail-item {{ margin: 10px 0; }}
            .detail-label {{ font-weight: bold; color: #00ff9d; }}
            .footer {{ margin-top: 30px; text-align: center; font-size: 0.8rem; color: #888; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🤖 AI AGENT SYSTEM</div>
                <h1 class="title">Learning Schedule Confirmation</h1>
            </div>
            <p>Hello {user_name},</p>
            <p>Congratulations! Your learning schedule has been successfully set up.</p>
            
            <div class="course-info">
                <h2>{course_name}</h2>
                <p>Your personalized learning journey is about to begin!</p>
            </div>
            
            <div class="schedule-details">
                <h3>Schedule Details:</h3>
                {schedule_details}
            </div>
            
            <p>You'll receive your first lesson according to your schedule. Make sure to check your email (and spam folder) for your lessons.</p>
            <p>If you have any questions or need to modify your schedule, please visit your dashboard.</p>
            
            <div class="footer">
                <p>&copy; 2025 AI Agent System. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>'''
