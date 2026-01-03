"""
CRUD operations for all models.

These functions encapsulate database operations and can be reused
across different routes. Keeps business logic separate from routing.
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, case
from sqlalchemy.sql import desc, asc
from typing import List, Optional, Tuple
from datetime import date, datetime
from models import Client, Contact, Service, Task, Note, Timesheet, User
from schemas import (
    ClientCreate, ClientUpdate,
    ContactCreate, ServiceCreate, TaskCreate, NoteCreate,
    TimesheetCreate, TimesheetUpdate,
    UserCreate, UserUpdate
)
import json
from auth import hash_password, get_default_permissions


# Client CRUD
def get_client(db: Session, client_id: int) -> Optional[Client]:
    """Get a single client by ID."""
    return db.query(Client).filter(Client.id == client_id).first()


def calculate_client_revenue(db: Session, client_id: int) -> float:
    """
    Calculate annual revenue for a client based on active services.
    
    Revenue = sum of (monthly_fee × multiplier) for all active services
    Multiplier: 12 for Monthly, 4 for Quarterly, 1 for Annual
    """
    services = db.query(Service).filter(
        Service.client_id == client_id,
        Service.active == True
    ).all()
    
    revenue = 0.0
    for service in services:
        if service.monthly_fee:
            if service.billing_frequency == "Monthly":
                revenue += service.monthly_fee * 12
            elif service.billing_frequency == "Quarterly":
                revenue += service.monthly_fee * 4
            elif service.billing_frequency == "Annual":
                revenue += service.monthly_fee
            else:
                # Default to monthly if frequency not set
                revenue += service.monthly_fee * 12
    
    return revenue


def get_clients(
    db: Session, 
    skip: int = 0, 
    limit: int = 1000, 
    search: Optional[str] = None,
    status_filter: Optional[str] = None,
    entity_type_filter: Optional[str] = None,
    follow_up_filter: Optional[str] = None,
    sort_by: str = "name",
    sort_order: str = "asc"
) -> List[Client]:
    """
    Get all clients with optional search, filtering, and sorting.
    
    follow_up_filter options:
    - "needed": Prospects with follow-up date today or in the past
    - "overdue": Prospects with follow-up date in the past
    """
    query = db.query(Client)
    
    if search:
        query = query.filter(Client.legal_name.ilike(f"%{search}%"))
    
    if status_filter:
        query = query.filter(Client.status == status_filter)
    
    if entity_type_filter:
        query = query.filter(Client.entity_type == entity_type_filter)
    
    if follow_up_filter:
        today = date.today()
        if follow_up_filter == "needed":
            # Prospects needing follow-up (due today or past)
            query = query.filter(
                Client.status == "Prospect",
                Client.next_follow_up_date <= today
            )
        elif follow_up_filter == "overdue":
            # Prospects overdue for follow-up (past date only)
            query = query.filter(
                Client.status == "Prospect",
                Client.next_follow_up_date < today
            )
    
    # Sorting
    if sort_by == "name":
        if sort_order == "desc":
            query = query.order_by(desc(Client.legal_name))
        else:
            query = query.order_by(asc(Client.legal_name))
    elif sort_by == "status":
        if sort_order == "desc":
            query = query.order_by(desc(Client.status))
        else:
            query = query.order_by(asc(Client.status))
    elif sort_by == "revenue":
        # For revenue sorting, we'll need to calculate it in Python
        # since SQLite doesn't easily support subqueries in ORDER BY
        # We'll sort in Python after fetching
        query = query.order_by(Client.legal_name)
    else:
        query = query.order_by(Client.legal_name)
    
    clients = query.offset(skip).limit(limit).all()
    
    # If sorting by revenue, sort in Python
    if sort_by == "revenue":
        clients_with_revenue = []
        for client in clients:
            revenue = calculate_client_revenue(db, client.id)
            clients_with_revenue.append((client, revenue))
        
        clients_with_revenue.sort(
            key=lambda x: x[1], 
            reverse=(sort_order == "desc")
        )
        clients = [c[0] for c in clients_with_revenue]
    
    return clients


def create_client(db: Session, client: ClientCreate) -> Client:
    """Create a new client."""
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def update_client(db: Session, client_id: int, client_update: ClientUpdate) -> Optional[Client]:
    """Update an existing client."""
    db_client = get_client(db, client_id)
    if not db_client:
        return None
    
    update_data = client_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_client, field, value)
    
    db.commit()
    db.refresh(db_client)
    return db_client


def update_client_field(db: Session, client_id: int, field: str, value: any) -> Optional[Client]:
    """
    Update a single field on a client (for inline editing).
    
    Used for quick updates from the clients list page.
    """
    db_client = get_client(db, client_id)
    if not db_client:
        return None
    
    if hasattr(db_client, field):
        # Handle date conversion
        if field == "next_follow_up_date" and isinstance(value, str):
            if value:
                try:
                    value = datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError:
                    value = None
            else:
                value = None
        
        setattr(db_client, field, value)
        db.commit()
        db.refresh(db_client)
    
    return db_client


def delete_client(db: Session, client_id: int) -> bool:
    """Delete a client (cascade deletes related records)."""
    db_client = get_client(db, client_id)
    if not db_client:
        return False
    
    db.delete(db_client)
    db.commit()
    return True


# Contact CRUD
def create_contact(db: Session, contact: ContactCreate) -> Contact:
    """Create a new contact."""
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int) -> bool:
    """Delete a contact."""
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        return False
    
    db.delete(db_contact)
    db.commit()
    return True


# Service CRUD
def create_service(db: Session, service: ServiceCreate) -> Service:
    """Create a new service."""
    db_service = Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def update_service(db: Session, service_id: int, active: bool) -> Optional[Service]:
    """Toggle service active status."""
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if not db_service:
        return None
    
    db_service.active = active
    db.commit()
    db.refresh(db_service)
    return db_service


def delete_service(db: Session, service_id: int) -> bool:
    """Delete a service."""
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if not db_service:
        return False
    
    db.delete(db_service)
    db.commit()
    return True


# Task CRUD
def create_task(db: Session, task: TaskCreate) -> Task:
    """Create a new task."""
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task_status(db: Session, task_id: int, status: str) -> Optional[Task]:
    """Update task status."""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None
    
    db_task.status = status
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """Delete a task."""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True


# Note CRUD
def create_note(db: Session, note: NoteCreate) -> Note:
    """Create a new note."""
    db_note = Note(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int) -> bool:
    """Delete a note."""
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        return False
    
    db.delete(db_note)
    db.commit()
    return True


# Timesheet CRUD
def get_timesheets(
    db: Session,
    skip: int = 0,
    limit: int = 1000,
    client_id: Optional[int] = None,
    staff_member: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    search: Optional[str] = None
) -> List[Timesheet]:
    """Get timesheet entries with optional filtering."""
    query = db.query(Timesheet)
    
    if client_id:
        query = query.filter(Timesheet.client_id == client_id)
    
    if staff_member:
        query = query.filter(Timesheet.staff_member == staff_member)
    
    if date_from:
        query = query.filter(Timesheet.entry_date >= date_from)
    
    if date_to:
        query = query.filter(Timesheet.entry_date <= date_to)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Timesheet.description.ilike(search_term),
                Timesheet.project_task.ilike(search_term),
                Timesheet.staff_member.ilike(search_term)
            )
        )
    
    # Order by most recent first
    query = query.order_by(desc(Timesheet.entry_date), desc(Timesheet.created_at))
    
    return query.offset(skip).limit(limit).all()


def get_timesheet(db: Session, timesheet_id: int) -> Optional[Timesheet]:
    """Get a single timesheet entry by ID."""
    return db.query(Timesheet).filter(Timesheet.id == timesheet_id).first()


def create_timesheet(db: Session, timesheet: TimesheetCreate) -> Timesheet:
    """Create a new timesheet entry."""
    db_timesheet = Timesheet(**timesheet.dict())
    db.add(db_timesheet)
    db.commit()
    db.refresh(db_timesheet)
    return db_timesheet


def update_timesheet(db: Session, timesheet_id: int, timesheet_update: TimesheetUpdate) -> Optional[Timesheet]:
    """Update an existing timesheet entry."""
    db_timesheet = get_timesheet(db, timesheet_id)
    if not db_timesheet:
        return None
    
    update_data = timesheet_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_timesheet, field, value)
    
    db_timesheet.updated_at = datetime.now()
    db.commit()
    db.refresh(db_timesheet)
    return db_timesheet


def delete_timesheet(db: Session, timesheet_id: int) -> bool:
    """Delete a timesheet entry."""
    db_timesheet = db.query(Timesheet).filter(Timesheet.id == timesheet_id).first()
    if not db_timesheet:
        return False
    
    db.delete(db_timesheet)
    db.commit()
    return True


def get_timesheet_summary(
    db: Session,
    client_id: Optional[int] = None,
    staff_member: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None
) -> dict:
    """Get summary statistics for timesheets."""
    # Build base query with filters
    base_query = db.query(Timesheet)
    filters = []
    
    if client_id:
        filters.append(Timesheet.client_id == client_id)
    
    if staff_member:
        filters.append(Timesheet.staff_member == staff_member)
    
    if date_from:
        filters.append(Timesheet.entry_date >= date_from)
    
    if date_to:
        filters.append(Timesheet.entry_date <= date_to)
    
    # Apply filters to base query
    if filters:
        base_query = base_query.filter(*filters)
    
    # Calculate totals
    total_hours_query = db.query(func.sum(Timesheet.hours))
    billable_hours_query = db.query(func.sum(Timesheet.hours)).filter(Timesheet.billable == True)
    
    if filters:
        total_hours_query = total_hours_query.filter(*filters)
        billable_hours_query = billable_hours_query.filter(*filters)
    
    total_hours = total_hours_query.scalar() or 0.0
    billable_hours = billable_hours_query.scalar() or 0.0
    total_entries = base_query.count()
    
    return {
        "total_hours": float(total_hours),
        "billable_hours": float(billable_hours),
        "non_billable_hours": float(total_hours - billable_hours),
        "total_entries": total_entries
    }


# User CRUD
def get_users(db: Session, skip: int = 0, limit: int = 1000, active_only: bool = False) -> List[User]:
    """Get all users."""
    query = db.query(User)
    if active_only:
        query = query.filter(User.active == True)
    return query.offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get a single user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    try:
        # Hash password
        hashed_password = hash_password(user.password)
        
        # Set default permissions if not provided
        if user.permissions is None:
            permissions = get_default_permissions(user.role)
        else:
            permissions = user.permissions
        
        # Convert permissions to JSON string
        permissions_json = json.dumps(permissions)
        
        db_user = User(
            email=user.email,
            name=user.name,
            hashed_password=hashed_password,
            role=user.role,
            permissions=permissions_json,
            active=True
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(f"Error in create_user: {e}")
        import traceback
        traceback.print_exc()
        raise


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update an existing user."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    
    # Handle password update
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))
    
    # Handle permissions update
    if "permissions" in update_data:
        update_data["permissions"] = json.dumps(update_data["permissions"])
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Soft delete a user (set active=False)."""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db_user.active = False
    db.commit()
    return True

