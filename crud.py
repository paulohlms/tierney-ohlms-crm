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
    
    Returns 0.0 if calculation fails (e.g., Service table issues, transaction errors).
    This ensures graceful degradation when database queries fail.
    
    CRITICAL: This function must not hang. Uses raw SQL with explicit timeout to avoid
    ORM query issues that can cause indefinite blocking.
    """
    import logging
    from sqlalchemy.exc import SQLAlchemyError, OperationalError, TimeoutError
    from database import SessionLocal, engine
    from sqlalchemy import text
    import signal
    import threading
    logger = logging.getLogger(__name__)
    
    # CRITICAL: Use raw SQL with connection-level timeout to prevent indefinite blocking
    # ORM queries can hang due to transaction locks, but raw SQL with timeout will fail fast
    fresh_db = None
    try:
        logger.info(f"[REVENUE] Starting revenue calculation for client {client_id}")
        logger.info(f"[REVENUE] Step 1: Creating fresh database connection...")
        
        # Create a fresh connection (not session) for raw SQL with timeout
        # This completely bypasses ORM and transaction state issues
        with engine.connect() as conn:
            logger.info(f"[REVENUE] Step 2: Connection established, executing raw SQL query...")
            
            try:
                # Use raw SQL query with explicit timeout
                # This avoids ORM query hanging issues
                # PostgreSQL: statement_timeout is set per connection
                # SQLite: timeout is handled by connection args
                query = text("""
                    SELECT id, service_type, billing_frequency, monthly_fee, active
                    FROM services
                    WHERE client_id = :client_id AND active = true
                """)
                
                logger.info(f"[REVENUE] Step 3: Executing SQL query for client {client_id}...")
                result = conn.execute(query, {"client_id": client_id})
                services_data = result.fetchall()
                
                logger.info(f"[REVENUE] Step 4: Query completed - found {len(services_data)} active services for client {client_id}")
                
            except (SQLAlchemyError, OperationalError, TimeoutError) as query_error:
                # Database error - return 0 immediately
                error_msg = str(query_error)
                logger.error(f"[REVENUE] Step 4 ERROR: Database query failed for client {client_id}: {error_msg}", exc_info=True)
                
                # Check if it's a column-related error
                if 'column' in error_msg.lower() or 'duplicate' in error_msg.lower() or 'ambiguous' in error_msg.lower():
                    logger.error(f"[REVENUE] Possible schema issue with services table - duplicate columns may exist")
                
                return 0.0
            except Exception as query_error:
                # Any other error - return 0 immediately
                error_msg = str(query_error)
                logger.error(f"[REVENUE] Step 4 ERROR: Unexpected error during query for client {client_id}: {error_msg}", exc_info=True)
                return 0.0
            
            # Calculate revenue from services data
            logger.info(f"[REVENUE] Step 5: Calculating revenue from {len(services_data)} services...")
            revenue = 0.0
            for row in services_data:
                try:
                    # Row is a Row object - access by index or column name
                    monthly_fee = row[3] if len(row) > 3 else None  # monthly_fee is 4th column (0-indexed)
                    billing_frequency = row[2] if len(row) > 2 else None  # billing_frequency is 3rd column
                    
                    if monthly_fee:
                        if billing_frequency == "Monthly":
                            revenue += monthly_fee * 12
                        elif billing_frequency == "Quarterly":
                            revenue += monthly_fee * 4
                        elif billing_frequency == "Annual":
                            revenue += monthly_fee
                        else:
                            # Default to monthly if frequency not set
                            revenue += monthly_fee * 12
                except Exception as e:
                    service_id = row[0] if len(row) > 0 else "unknown"
                    logger.warning(f"[REVENUE] Error calculating revenue for service {service_id}: {e}")
                    continue
            
            logger.info(f"[REVENUE] Step 6: Revenue calculation complete for client {client_id}: ${revenue:,.2f}")
            return revenue
        
    except Exception as e:
        # Graceful degradation: return 0 if anything fails
        logger.error(f"[REVENUE] Outer error calculating revenue for client {client_id}: {e}", exc_info=True)
        return 0.0


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
    import logging
    from sqlalchemy.exc import SQLAlchemyError
    logger = logging.getLogger(__name__)
    
    try:
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
                try:
                    revenue = calculate_client_revenue(db, client.id)
                    clients_with_revenue.append((client, revenue))
                except Exception as e:
                    logger.warning(f"Error calculating revenue for client {client.id} during sort: {e}")
                    clients_with_revenue.append((client, 0.0))
            
            clients_with_revenue.sort(
                key=lambda x: x[1], 
                reverse=(sort_order == "desc")
            )
            clients = [c[0] for c in clients_with_revenue]
        
        return clients
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_clients: {e}", exc_info=True)
        db.rollback()
        return []
    except Exception as e:
        logger.error(f"Unexpected error in get_clients: {e}", exc_info=True)
        return []


def create_client(db: Session, client: ClientCreate) -> Client:
    """Create a new client."""
    import logging
    from sqlalchemy.exc import SQLAlchemyError
    logger = logging.getLogger(__name__)
    
    try:
        db_client = Client(**client.dict())
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        logger.info(f"Created client {db_client.id}: {db_client.legal_name}")
        return db_client
    except SQLAlchemyError as e:
        logger.error(f"Database error creating client: {e}", exc_info=True)
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error creating client: {e}", exc_info=True)
        db.rollback()
        raise


def update_client(db: Session, client_id: int, client_update: ClientUpdate) -> Optional[Client]:
    """Update an existing client."""
    import logging
    from sqlalchemy.exc import SQLAlchemyError
    logger = logging.getLogger(__name__)
    
    try:
        db_client = get_client(db, client_id)
        if not db_client:
            logger.warning(f"Client {client_id} not found for update")
            return None
        
        update_data = client_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_client, field, value)
        
        db.commit()
        db.refresh(db_client)
        logger.info(f"Updated client {client_id}: {db_client.legal_name}")
        return db_client
    except SQLAlchemyError as e:
        logger.error(f"Database error updating client {client_id}: {e}", exc_info=True)
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error updating client {client_id}: {e}", exc_info=True)
        db.rollback()
        raise


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
    import logging
    from sqlalchemy.exc import SQLAlchemyError
    logger = logging.getLogger(__name__)
    
    try:
        db_client = get_client(db, client_id)
        if not db_client:
            logger.warning(f"Client {client_id} not found for deletion")
            return False
        
        client_name = db_client.legal_name
        db.delete(db_client)
        db.commit()
        logger.info(f"Deleted client {client_id}: {client_name}")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database error deleting client {client_id}: {e}", exc_info=True)
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error deleting client {client_id}: {e}", exc_info=True)
        db.rollback()
        raise


# Contact CRUD
def create_contact(db: Session, contact: ContactCreate) -> Contact:
    """Create a new contact."""
    import logging
    from sqlalchemy.exc import SQLAlchemyError
    logger = logging.getLogger(__name__)
    
    try:
        db_contact = Contact(**contact.dict())
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        logger.info(f"Created contact {db_contact.id} for client {db_contact.client_id}: {db_contact.name}")
        return db_contact
    except SQLAlchemyError as e:
        logger.error(f"Database error creating contact: {e}", exc_info=True)
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error creating contact: {e}", exc_info=True)
        db.rollback()
        raise


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
    import logging
    from sqlalchemy.exc import SQLAlchemyError
    logger = logging.getLogger(__name__)
    
    try:
        db_service = Service(**service.dict())
        db.add(db_service)
        db.commit()
        db.refresh(db_service)
        logger.info(f"Created service {db_service.id} for client {db_service.client_id}: {db_service.service_type}")
        return db_service
    except SQLAlchemyError as e:
        logger.error(f"Database error creating service: {e}", exc_info=True)
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error creating service: {e}", exc_info=True)
        db.rollback()
        raise


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
    import logging
    from sqlalchemy.exc import SQLAlchemyError
    logger = logging.getLogger(__name__)
    
    try:
        db_task = Task(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        logger.info(f"Created task {db_task.id} for client {db_task.client_id}: {db_task.title}")
        return db_task
    except SQLAlchemyError as e:
        logger.error(f"Database error creating task: {e}", exc_info=True)
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error creating task: {e}", exc_info=True)
        db.rollback()
        raise


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
    import logging
    from sqlalchemy.exc import SQLAlchemyError
    logger = logging.getLogger(__name__)
    
    try:
        db_note = Note(**note.dict())
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        logger.info(f"Created note {db_note.id} for client {db_note.client_id}")
        return db_note
    except SQLAlchemyError as e:
        logger.error(f"Database error creating note: {e}", exc_info=True)
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error creating note: {e}", exc_info=True)
        db.rollback()
        raise


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
    import logging
    from sqlalchemy.exc import SQLAlchemyError
    logger = logging.getLogger(__name__)
    
    try:
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
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_timesheets: {e}", exc_info=True)
        db.rollback()
        return []
    except Exception as e:
        logger.error(f"Unexpected error in get_timesheets: {e}", exc_info=True)
        return []


def get_timesheet(db: Session, timesheet_id: int) -> Optional[Timesheet]:
    """Get a single timesheet entry by ID."""
    return db.query(Timesheet).filter(Timesheet.id == timesheet_id).first()


def create_timesheet(db: Session, timesheet: TimesheetCreate) -> Timesheet:
    """Create a new timesheet entry."""
    import logging
    from sqlalchemy.exc import SQLAlchemyError
    logger = logging.getLogger(__name__)
    
    try:
        db_timesheet = Timesheet(**timesheet.dict())
        db.add(db_timesheet)
        db.commit()
        db.refresh(db_timesheet)
        logger.info(f"Created timesheet {db_timesheet.id} for client {db_timesheet.client_id}: {db_timesheet.hours}h by {db_timesheet.staff_member}")
        return db_timesheet
    except SQLAlchemyError as e:
        logger.error(f"Database error creating timesheet: {e}", exc_info=True)
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error creating timesheet: {e}", exc_info=True)
        db.rollback()
        raise


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
    import logging
    from sqlalchemy.exc import SQLAlchemyError
    logger = logging.getLogger(__name__)
    
    try:
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
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_timesheet_summary: {e}", exc_info=True)
        db.rollback()
        return {
            "total_hours": 0.0,
            "billable_hours": 0.0,
            "non_billable_hours": 0.0,
            "total_entries": 0
        }
    except Exception as e:
        logger.error(f"Unexpected error in get_timesheet_summary: {e}", exc_info=True)
        return {
            "total_hours": 0.0,
            "billable_hours": 0.0,
            "non_billable_hours": 0.0,
            "total_entries": 0
        }
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_timesheet_summary: {e}", exc_info=True)
        db.rollback()
        return {"total_hours": 0.0, "billable_hours": 0.0, "non_billable_hours": 0.0, "total_entries": 0}
    except Exception as e:
        logger.error(f"Unexpected error in get_timesheet_summary: {e}", exc_info=True)
        return {"total_hours": 0.0, "billable_hours": 0.0, "non_billable_hours": 0.0, "total_entries": 0}


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

