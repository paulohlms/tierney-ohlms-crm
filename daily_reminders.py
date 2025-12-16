"""
Daily reminder job for prospect follow-ups.

Run this script daily (via cron, task scheduler, etc.) to send
internal reminder emails about prospects needing follow-up.

Usage:
    python daily_reminders.py

Or schedule it to run daily:
    - Windows Task Scheduler
    - Linux cron: 0 9 * * * /path/to/python /path/to/daily_reminders.py
"""
from datetime import date
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Client
from email_service import get_email_provider, send_prospect_followup_reminder
import os


def get_prospects_needing_followup(db: Session) -> list:
    """
    Get all prospects that need follow-up (due today or overdue).
    
    Returns list of dicts with client info.
    """
    today = date.today()
    
    prospects = db.query(Client).filter(
        Client.status == "Prospect",
        Client.next_follow_up_date <= today
    ).all()
    
    results = []
    for prospect in prospects:
        results.append({
            'name': prospect.legal_name,
            'next_follow_up_date': prospect.next_follow_up_date.strftime('%Y-%m-%d') if prospect.next_follow_up_date else '',
            'overdue': prospect.next_follow_up_date < today if prospect.next_follow_up_date else False,
            'client_id': prospect.id
        })
    
    return results


def send_daily_reminders():
    """Send daily reminder emails to internal users."""
    db = SessionLocal()
    
    try:
        # Get prospects needing follow-up
        prospects = get_prospects_needing_followup(db)
        
        if not prospects:
            print("No prospects need follow-up today.")
            return
        
        # Get email addresses to notify
        # In production, this would come from a user table
        # For now, use environment variable or default
        notify_emails = os.getenv("REMINDER_EMAILS", "admin@tierneyohlms.com").split(",")
        notify_emails = [e.strip() for e in notify_emails if e.strip()]
        
        if not notify_emails:
            print("No email addresses configured for reminders.")
            return
        
        # Get email provider
        email_provider = get_email_provider()
        
        # Send emails
        success_count = 0
        for email in notify_emails:
            if send_prospect_followup_reminder(email_provider, email, prospects):
                success_count += 1
                print(f"✓ Reminder sent to {email}")
            else:
                print(f"✗ Failed to send reminder to {email}")
        
        print(f"\nSent {success_count} reminder email(s) about {len(prospects)} prospect(s).")
        
    except Exception as e:
        print(f"Error sending daily reminders: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Running daily prospect follow-up reminders...")
    print("=" * 60)
    send_daily_reminders()
    print("=" * 60)
    print("Done.")

