"""
Pydantic schemas for request/response validation.

These ensure data integrity at the API boundary and provide
automatic validation and serialization.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime


# Client schemas
class ClientBase(BaseModel):
    legal_name: str
    entity_type: Optional[str] = None
    fiscal_year_end: Optional[str] = None
    status: str = "Prospect"
    owner_name: Optional[str] = None
    owner_email: Optional[str] = None
    next_follow_up_date: Optional[date] = None
    last_reminder_sent: Optional[date] = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    legal_name: Optional[str] = None
    entity_type: Optional[str] = None
    fiscal_year_end: Optional[str] = None
    status: Optional[str] = None
    owner_name: Optional[str] = None
    owner_email: Optional[str] = None
    next_follow_up_date: Optional[date] = None
    last_reminder_sent: Optional[date] = None


class Client(ClientBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Contact schemas
class ContactBase(BaseModel):
    name: str
    role: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class ContactCreate(ContactBase):
    client_id: int


class Contact(ContactBase):
    id: int
    client_id: int
    
    class Config:
        from_attributes = True


# Service schemas
class ServiceBase(BaseModel):
    service_type: str
    billing_frequency: Optional[str] = None
    monthly_fee: Optional[float] = None
    active: bool = True


class ServiceCreate(ServiceBase):
    client_id: int


class Service(ServiceBase):
    id: int
    client_id: int
    
    class Config:
        from_attributes = True


# Task schemas
class TaskBase(BaseModel):
    title: str
    due_date: Optional[date] = None
    status: str = "Open"
    notes: Optional[str] = None


class TaskCreate(TaskBase):
    client_id: int


class Task(TaskBase):
    id: int
    client_id: int
    
    class Config:
        from_attributes = True


# Note schemas
class NoteBase(BaseModel):
    content: str


class NoteCreate(NoteBase):
    client_id: int


class Note(NoteBase):
    id: int
    client_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Client detail view with relationships
class ClientDetail(Client):
    contacts: List[Contact] = []
    services: List[Service] = []
    tasks: List[Task] = []
    notes: List[Note] = []


# Timesheet schemas
class TimesheetBase(BaseModel):
    client_id: int
    staff_member: str
    entry_date: date
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    hours: float
    project_task: Optional[str] = None
    description: Optional[str] = None
    billable: bool = True


class TimesheetCreate(TimesheetBase):
    pass


class TimesheetUpdate(BaseModel):
    client_id: Optional[int] = None
    staff_member: Optional[str] = None
    entry_date: Optional[date] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    hours: Optional[float] = None
    project_task: Optional[str] = None
    description: Optional[str] = None
    billable: Optional[bool] = None


class Timesheet(TimesheetBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# User schemas
class UserBase(BaseModel):
    email: str
    name: str
    role: str = "Staff"


class UserCreate(UserBase):
    password: str
    permissions: Optional[dict] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None
    permissions: Optional[dict] = None
    active: Optional[bool] = None


class User(UserBase):
    id: int
    active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

