"""
Database seeding script with sample data.

Run this once to populate the database with realistic sample data
for testing and demonstration purposes.
"""
from database import engine, SessionLocal
from models import Base, Client, Contact, Service, Task, Note
from datetime import date, timedelta

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Check if data already exists
    if db.query(Client).count() > 0:
        print("Database already seeded. Skipping...")
    else:
        # Sample Clients
        client1 = Client(
            legal_name="Acme Manufacturing LLC",
            entity_type="LLC",
            fiscal_year_end="12/31",
            status="Active",
            owner_name="Sarah Johnson",
            owner_email="sarah@firm.com"
        )
        client2 = Client(
            legal_name="Smith & Associates Inc",
            entity_type="S-Corp",
            fiscal_year_end="06/30",
            status="Active",
            owner_name="Michael Chen",
            owner_email="michael@firm.com"
        )
        client3 = Client(
            legal_name="Downtown Bakery",
            entity_type="LLC",
            fiscal_year_end="12/31",
            status="Prospect",
            owner_name="Emily Rodriguez",
            owner_email="emily@firm.com",
            next_follow_up_date=date.today() + timedelta(days=3)
        )
        client4 = Client(
            legal_name="Tech Solutions Corp",
            entity_type="C-Corp",
            fiscal_year_end="12/31",
            status="Active",
            owner_name="David Thompson",
            owner_email="david@firm.com"
        )
        
        # Add more prospects with realistic follow-up dates
        client5 = Client(
            legal_name="Green Energy Partners",
            entity_type="LLC",
            fiscal_year_end="12/31",
            status="Prospect",
            owner_name="Sarah Johnson",
            owner_email="sarah@firm.com",
            next_follow_up_date=date.today()  # Due today for testing
        )
        client6 = Client(
            legal_name="Metro Consulting Group",
            entity_type="S-Corp",
            fiscal_year_end="06/30",
            status="Prospect",
            owner_name="Michael Chen",
            owner_email="michael@firm.com",
            next_follow_up_date=date.today() - timedelta(days=2)  # Overdue
        )
        
        db.add_all([client1, client2, client3, client4, client5, client6])
        db.flush()  # Get IDs
        
        # Sample Contacts
        contacts = [
            Contact(client_id=client1.id, name="John Acme", role="Owner", email="john@acme.com", phone="555-0101"),
            Contact(client_id=client1.id, name="Jane Acme", role="Controller", email="jane@acme.com", phone="555-0102"),
            Contact(client_id=client2.id, name="Robert Smith", role="Owner", email="robert@smith.com", phone="555-0201"),
            Contact(client_id=client3.id, name="Mary Baker", role="Owner", email="mary@bakery.com", phone="555-0301"),
            Contact(client_id=client4.id, name="David Tech", role="CEO", email="david@tech.com", phone="555-0401"),
            Contact(client_id=client4.id, name="Sarah Tech", role="CFO", email="sarah@tech.com", phone="555-0402"),
            Contact(client_id=client5.id, name="James Green", role="Owner", email="james@greenenergy.com", phone="555-0501"),
            Contact(client_id=client6.id, name="Lisa Metro", role="Founder", email="lisa@metroconsulting.com", phone="555-0601"),
        ]
        
        # Sample Services
        services = [
            Service(client_id=client1.id, service_type="Bookkeeping", billing_frequency="Monthly", monthly_fee=1500.00, active=True),
            Service(client_id=client1.id, service_type="Payroll", billing_frequency="Monthly", monthly_fee=500.00, active=True),
            Service(client_id=client1.id, service_type="Tax Return", billing_frequency="Annual", monthly_fee=5000.00, active=True),
            Service(client_id=client2.id, service_type="Bookkeeping", billing_frequency="Monthly", monthly_fee=2000.00, active=True),
            Service(client_id=client2.id, service_type="Sales Tax", billing_frequency="Monthly", monthly_fee=300.00, active=True),
            Service(client_id=client3.id, service_type="Bookkeeping", billing_frequency="Monthly", monthly_fee=800.00, active=True),
            Service(client_id=client4.id, service_type="Bookkeeping", billing_frequency="Monthly", monthly_fee=3000.00, active=True),
            Service(client_id=client4.id, service_type="AP", billing_frequency="Monthly", monthly_fee=1000.00, active=True),
            Service(client_id=client4.id, service_type="AR", billing_frequency="Monthly", monthly_fee=1000.00, active=True),
            Service(client_id=client5.id, service_type="Bookkeeping", billing_frequency="Monthly", monthly_fee=1200.00, active=True),
            Service(client_id=client6.id, service_type="Bookkeeping", billing_frequency="Monthly", monthly_fee=1800.00, active=True),
        ]
        
        # Sample Tasks
        tasks = [
            Task(client_id=client1.id, title="Review Q4 financials", due_date=date.today() + timedelta(days=7), status="Open", notes="Need to prepare for year-end"),
            Task(client_id=client1.id, title="File sales tax return", due_date=date.today() + timedelta(days=14), status="Open"),
            Task(client_id=client2.id, title="Update payroll system", due_date=date.today() + timedelta(days=3), status="Waiting on Client", notes="Waiting for new employee list"),
            Task(client_id=client3.id, title="Initial consultation", due_date=date.today() + timedelta(days=1), status="Open", notes="New prospect meeting"),
            Task(client_id=client4.id, title="Monthly reconciliation", due_date=date.today() + timedelta(days=5), status="Open"),
            Task(client_id=client4.id, title="Tax planning meeting", due_date=date.today() + timedelta(days=30), status="Open"),
        ]
        
        # Sample Notes
        notes = [
            Note(client_id=client1.id, content="Client is expanding operations. May need additional services next quarter."),
            Note(client_id=client1.id, content="John mentioned they're considering opening a second location. Good opportunity for growth."),
            Note(client_id=client2.id, content="Robert is very responsive and organized. Great client to work with."),
            Note(client_id=client3.id, content="Initial contact made. They're looking for bookkeeping services. Follow up next week."),
            Note(client_id=client4.id, content="Fast-growing tech company. They may need CFO advisory services in the future."),
            Note(client_id=client4.id, content="David mentioned they're raising Series A funding. Will need help with financial projections."),
            Note(client_id=client5.id, content="Initial meeting went well. They're interested in full-service bookkeeping. Follow up in 3 days."),
            Note(client_id=client6.id, content="Met with Lisa last week. They need help with tax planning and quarterly reporting. Overdue for follow-up!"),
        ]
        
        db.add_all(contacts)
        db.add_all(services)
        db.add_all(tasks)
        db.add_all(notes)
        
        db.commit()
        print("Database seeded successfully!")
        
except Exception as e:
    print(f"Error seeding database: {e}")
    db.rollback()
finally:
    db.close()

