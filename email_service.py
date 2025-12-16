"""
Email service abstraction for sending internal reminder emails.

This abstraction allows swapping email providers later without changing
the rest of the application code.
"""
from typing import List, Dict
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class EmailProvider:
    """
    Abstract base class for email providers.
    
    Implementations can use SMTP, SendGrid, AWS SES, etc.
    """
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """
        Send an email.
        
        Returns True if successful, False otherwise.
        """
        raise NotImplementedError


class SMTPEmailProvider(EmailProvider):
    """
    Simple SMTP email provider for internal use.
    
    Configure via environment variables:
    - SMTP_HOST (default: localhost)
    - SMTP_PORT (default: 25)
    - SMTP_USER (optional)
    - SMTP_PASSWORD (optional)
    - EMAIL_FROM (default: crm@tierneyohlms.com)
    """
    def __init__(self):
        self.host = os.getenv("SMTP_HOST", "localhost")
        self.port = int(os.getenv("SMTP_PORT", "25"))
        self.user = os.getenv("SMTP_USER")
        self.password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("EMAIL_FROM", "crm@tierneyohlms.com")
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send email via SMTP."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.host, self.port)
            if self.user and self.password:
                server.starttls()
                server.login(self.user, self.password)
            
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False


class ConsoleEmailProvider(EmailProvider):
    """
    Development email provider that prints to console.
    
    Useful for testing and development when SMTP isn't configured.
    """
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Print email to console instead of sending."""
        print("=" * 60)
        print(f"EMAIL TO: {to}")
        print(f"SUBJECT: {subject}")
        print("-" * 60)
        print(body)
        print("=" * 60)
        return True


# Global email provider instance
_email_provider = None


def get_email_provider() -> EmailProvider:
    """
    Get the configured email provider.
    
    Defaults to ConsoleEmailProvider if SMTP not configured.
    """
    global _email_provider
    if _email_provider is None:
        # Use SMTP if configured, otherwise use console
        if os.getenv("SMTP_HOST"):
            _email_provider = SMTPEmailProvider()
        else:
            _email_provider = ConsoleEmailProvider()
    return _email_provider


def send_prospect_followup_reminder(
    email_provider: EmailProvider,
    to_email: str,
    prospects: List[Dict]
) -> bool:
    """
    Send reminder email about prospects needing follow-up.
    
    Args:
        email_provider: Email provider to use
        to_email: Email address to send to
        prospects: List of prospect dicts with 'name', 'next_follow_up_date', 'overdue'
    
    Returns:
        True if email sent successfully
    """
    overdue = [p for p in prospects if p.get('overdue', False)]
    due_today = [p for p in prospects if not p.get('overdue', False)]
    
    subject = "Prospect Follow-Up Reminder - Tierney & Ohlms CRM"
    
    body = "Prospect Follow-Up Reminder\n"
    body += "=" * 60 + "\n\n"
    
    if overdue:
        body += f"OVERDUE ({len(overdue)}):\n"
        for prospect in overdue:
            body += f"  - {prospect['name']} (due: {prospect['next_follow_up_date']})\n"
        body += "\n"
    
    if due_today:
        body += f"DUE TODAY ({len(due_today)}):\n"
        for prospect in due_today:
            body += f"  - {prospect['name']} (due: {prospect['next_follow_up_date']})\n"
        body += "\n"
    
    body += f"Total prospects needing follow-up: {len(prospects)}\n"
    body += "\n"
    body += "View in CRM: http://localhost:8000/clients?follow_up=needed\n"
    
    return email_provider.send_email(to_email, subject, body)

