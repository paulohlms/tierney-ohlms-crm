"""
SQLAlchemy models for the CRM database.

All models use standard naming conventions and include proper relationships.
Foreign keys ensure data integrity at the database level.
"""
from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.sqlite import JSON
from database import Base


class Client(Base):
    """
    Main client entity representing a business that the firm serves.
    
    Status values: Prospect, Active, Paused, Former, Dead
    Entity types: LLC, S-Corp, C-Corp, Partnership, Sole Proprietorship, Unknown, etc.
    """
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    legal_name = Column(String, nullable=False, index=True)  # Indexed for search performance
    entity_type = Column(String)  # LLC, S-Corp, C-Corp, Partnership, Unknown, etc.
    fiscal_year_end = Column(String)  # e.g., "12/31", "06/30"
    status = Column(String, nullable=False, default="Prospect")  # Prospect, Active, Paused, Former, Dead
    owner_name = Column(String)  # Name of the deal owner (who gets reminder emails)
    owner_email = Column(String)  # Email of the deal owner (for follow-up reminders)
    next_follow_up_date = Column(Date)  # For prospect follow-up tracking
    last_reminder_sent = Column(Date)  # Track when last reminder was sent (prevent spam)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships - cascade delete ensures related records are cleaned up
    contacts = relationship("Contact", back_populates="client", cascade="all, delete-orphan")
    services = relationship("Service", back_populates="client", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="client", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="client", cascade="all, delete-orphan", order_by="Note.created_at.desc()")
    timesheets = relationship("Timesheet", back_populates="client", cascade="all, delete-orphan")


class Contact(Base):
    """
    People associated with a client (owners, controllers, bookkeepers, etc.).
    
    Each client can have multiple contacts for different roles.
    """
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    name = Column(String, nullable=False)
    role = Column(String)  # Owner, Controller, Bookkeeper, Tax, Other
    email = Column(String)
    phone = Column(String)
    
    # Relationship back to client
    client = relationship("Client", back_populates="contacts")


class Service(Base):
    """
    Services provided to clients (bookkeeping, payroll, tax prep, etc.).
    
    Tracks billing frequency and monthly fee for each service.
    Active flag allows soft-deletion of services.
    """
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    service_type = Column(String, nullable=False)  # Bookkeeping, AP, AR, Payroll, Sales Tax, Tax Return
    billing_frequency = Column(String)  # Monthly, Quarterly, Annual
    monthly_fee = Column(Float)  # Fee amount (interpreted based on billing_frequency)
    active = Column(Boolean, default=True)
    
    # Relationship back to client
    client = relationship("Client", back_populates="services")


class Task(Base):
    """
    Tasks and to-dos associated with clients.
    
    Status workflow: Open → Waiting on Client → Completed
    Due dates help prioritize work.
    """
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    title = Column(String, nullable=False)
    due_date = Column(Date)
    status = Column(String, nullable=False, default="Open")  # Open, Waiting on Client, Completed
    notes = Column(Text)  # Additional task details
    
    # Relationship back to client
    client = relationship("Client", back_populates="tasks")


class Note(Base):
    """
    General notes and observations about clients.
    
    Chronological record of interactions, issues, or important information.
    Ordered by creation date (newest first) in the relationship.
    """
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship back to client
    client = relationship("Client", back_populates="notes")


class Timesheet(Base):
    """
    Time tracking entries for staff working on client projects.
    
    Tracks hours worked, billable status, and associated client/project.
    """
    __tablename__ = "timesheets"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    staff_member = Column(String, nullable=False)  # Name of staff member who logged time
    entry_date = Column(Date, nullable=False, index=True)  # Date when work was performed
    start_time = Column(String)  # Optional: Start time (HH:MM format)
    end_time = Column(String)  # Optional: End time (HH:MM format)
    hours = Column(Float, nullable=False)  # Total hours (decimal, e.g., 1.5)
    project_task = Column(String)  # Optional: Project or task name
    description = Column(Text)  # Notes/description of work performed
    billable = Column(Boolean, default=True)  # Whether this time is billable to client
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship back to client
    client = relationship("Client", back_populates="timesheets")


class User(Base):
    """
    User accounts with role-based permissions.
    
    Permissions are stored as JSON for flexibility.
    Role: Admin, Manager, Staff, Limited
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="Staff")  # Admin, Manager, Staff, Limited
    permissions = Column(Text)  # JSON string of permissions
    active = Column(Boolean, default=True)  # Soft delete
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

