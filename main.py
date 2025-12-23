"""
Main FastAPI application for CRM Tool.
Includes all improvements:
1. Client creation - contact info autopopulates
2. Services - Special Projects field
3. Service Banner - hourly rate selection
4. Prospects - no $75k auto-populate
"""
import os
from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from datetime import datetime, date
from decimal import Decimal
import json

from database import engine, Base, get_db, SessionLocal
from models import User, Client, Contact, Service, Prospect, Timesheet, Task, ClientNote
from auth import hash_password, verify_password, get_current_user, has_permission

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Session middleware
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-change-this")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def bootstrap_admin_users():
    """Create admin users if none exist."""
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        if user_count == 0:
            # Create default admin user
            admin_user = User(
                email="admin@example.com",
                hashed_password=hash_password("admin123"),
                full_name="Admin User",
                permissions=json.dumps({
                    "view_all_clients": True,
                    "edit_all_clients": True,
                    "view_all_timesheets": True,
                    "edit_all_timesheets": True,
                    "manage_users": True
                })
            )
            db.add(admin_user)
            db.commit()
            print("Created default admin user: admin@example.com / admin123")
    finally:
        db.close()


# Bootstrap on startup
bootstrap_admin_users()


# ==================== AUTHENTICATION ROUTES ====================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Redirect to login or dashboard."""
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=303)
    return RedirectResponse(url="/login", status_code=303)


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page."""
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request):
    """Handle login."""
    form = await request.form()
    email = form.get("email", "").strip()
    password = form.get("password", "")
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            # Try to bootstrap if no users exist
            user_count = db.query(User).count()
            if user_count == 0:
                bootstrap_admin_users()
                db.refresh(user)
                user = db.query(User).filter(User.email == email).first()
            
            if not user or not verify_password(password, user.hashed_password):
                return templates.TemplateResponse(
                    "login.html",
                    {"request": request, "error": "Invalid email or password"}
                )
        
        request.session["user_id"] = user.id
        return RedirectResponse(url="/dashboard", status_code=303)
    finally:
        db.close()


@app.get("/logout")
async def logout(request: Request):
    """Handle logout."""
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


# ==================== CLIENT ROUTES ====================

@app.get("/clients", response_class=HTMLResponse)
async def clients_list(request: Request, search: str = None):
    """List all clients."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    db = SessionLocal()
    try:
        query = db.query(Client)
        if search:
            query = query.filter(
                or_(
                    Client.legal_name.ilike(f"%{search}%"),
                    Client.email.ilike(f"%{search}%")
                )
            )
        clients = query.order_by(Client.legal_name).all()
        return templates.TemplateResponse(
            "clients_list.html",
            {"request": request, "clients": clients, "search": search}
        )
    finally:
        db.close()


@app.get("/clients/new", response_class=HTMLResponse)
async def new_client_form(request: Request):
    """Show new client form."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    # IMPROVEMENT 1: Get contact info from session if available (from previous step)
    contact_data = {
        "email": request.session.get("client_form_email", ""),
        "phone": request.session.get("client_form_phone", ""),
        "address": request.session.get("client_form_address", ""),
        "city": request.session.get("client_form_city", ""),
        "state": request.session.get("client_form_state", ""),
        "zip": request.session.get("client_form_zip", "")
    }
    
    return templates.TemplateResponse(
        "client_form.html",
        {"request": request, "client": None, "contact_data": contact_data}
    )


@app.post("/clients/new")
async def create_client(request: Request):
    """Create a new client."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    form = await request.form()
    
    db = SessionLocal()
    try:
        # IMPROVEMENT 1: Get contact info from form or session
        email = form.get("email", "").strip() or request.session.get("client_form_email", "")
        phone = form.get("phone", "").strip() or request.session.get("client_form_phone", "")
        address = form.get("address", "").strip() or request.session.get("client_form_address", "")
        city = form.get("city", "").strip() or request.session.get("client_form_city", "")
        state = form.get("state", "").strip() or request.session.get("client_form_state", "")
        zip_code = form.get("zip", "").strip() or request.session.get("client_form_zip", "")
        
        client = Client(
            legal_name=form.get("legal_name", "").strip(),
            entity_type=form.get("entity_type", "").strip() or None,
            ein_last4=form.get("ein_last4", "").strip() or None,
            fiscal_year_end=form.get("fiscal_year_end", "").strip() or None,
            status=form.get("status", "Active"),
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            notes=form.get("notes", "").strip() or None
        )
        db.add(client)
        db.commit()
        db.refresh(client)
        
        # IMPROVEMENT 1: Clear session data after use
        for key in ["client_form_email", "client_form_phone", "client_form_address", 
                   "client_form_city", "client_form_state", "client_form_zip"]:
            request.session.pop(key, None)
        
        # IMPROVEMENT 1: Redirect to contact creation with client info pre-filled
        return RedirectResponse(url=f"/clients/{client.id}/contacts/new?autopopulate=true", status_code=303)
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse(
            "client_form.html",
            {"request": request, "error": f"Error creating client: {str(e)}"}
        )
    finally:
        db.close()


@app.get("/clients/{client_id}", response_class=HTMLResponse)
async def client_detail(request: Request, client_id: int):
    """Show client details."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    db = SessionLocal()
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Get related data
        contacts = db.query(Contact).filter(Contact.client_id == client_id).all()
        services = db.query(Service).filter(Service.client_id == client_id).all()
        timesheets = db.query(Timesheet).filter(Timesheet.client_id == client_id).all()
        tasks = db.query(Task).filter(Task.client_id == client_id).all()
        notes = db.query(ClientNote).filter(ClientNote.client_id == client_id).order_by(ClientNote.created_at.desc()).all()
        
        return templates.TemplateResponse(
            "client_detail.html",
            {
                "request": request,
                "client": client,
                "contacts": contacts,
                "services": services,
                "timesheets": timesheets,
                "tasks": tasks,
                "notes": notes
            }
        )
    finally:
        db.close()


@app.get("/clients/{client_id}/contacts/new", response_class=HTMLResponse)
async def new_contact_form(request: Request, client_id: int):
    """Show new contact form with autopopulated data."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    db = SessionLocal()
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # IMPROVEMENT 1: Autopopulate from client if autopopulate param is set
        autopopulate = request.query_params.get("autopopulate") == "true"
        contact_data = {}
        if autopopulate and client:
            contact_data = {
                "email": client.email or "",
                "phone": client.phone or "",
                "address": client.address or "",
                "city": client.city or "",
                "state": client.state or "",
                "zip": client.zip_code or ""
            }
        
        return templates.TemplateResponse(
            "contact_form.html",
            {"request": request, "client": client, "contact": None, "contact_data": contact_data}
        )
    finally:
        db.close()


@app.post("/clients/{client_id}/contacts/new")
async def create_contact(request: Request, client_id: int):
    """Create a new contact."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    form = await request.form()
    
    db = SessionLocal()
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        contact = Contact(
            client_id=client_id,
            name=form.get("name", "").strip(),
            email=form.get("email", "").strip() or None,
            phone=form.get("phone", "").strip() or None,
            title=form.get("title", "").strip() or None,
            notes=form.get("notes", "").strip() or None
        )
        db.add(contact)
        db.commit()
        
        return RedirectResponse(url=f"/clients/{client_id}", status_code=303)
    finally:
        db.close()


# ==================== SERVICE ROUTES ====================

@app.get("/clients/{client_id}/services/new", response_class=HTMLResponse)
async def new_service_form(request: Request, client_id: int):
    """Show new service form."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    db = SessionLocal()
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        return templates.TemplateResponse(
            "service_form.html",
            {"request": request, "client": client, "service": None}
        )
    finally:
        db.close()


@app.post("/clients/{client_id}/services/new")
async def create_service(request: Request, client_id: int):
    """Create a new service."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    form = await request.form()
    
    db = SessionLocal()
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # IMPROVEMENT 2 & 3: Get special_projects, billing_type, and hourly_rate
        billing_type = form.get("billing_type", "fixed")
        hourly_rate = form.get("hourly_rate", "").strip()
        price = form.get("price", "").strip()
        
        service = Service(
            client_id=client_id,
            name=form.get("name", "").strip(),
            description=form.get("description", "").strip() or None,
            special_projects=form.get("special_projects", "").strip() or None,  # IMPROVEMENT 2
            billing_type=billing_type,  # IMPROVEMENT 3
            hourly_rate=float(hourly_rate) if hourly_rate and billing_type == "hourly" else None,  # IMPROVEMENT 3
            price=float(price) if price else None,
            status=form.get("status", "Active")
        )
        db.add(service)
        db.commit()
        
        return RedirectResponse(url=f"/clients/{client_id}", status_code=303)
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse(
            "service_form.html",
            {"request": request, "client": client, "error": f"Error creating service: {str(e)}"}
        )
    finally:
        db.close()


# ==================== PROSPECT ROUTES ====================

@app.get("/prospects", response_class=HTMLResponse)
async def prospects_list(request: Request):
    """List all prospects."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    db = SessionLocal()
    try:
        prospects = db.query(Prospect).order_by(Prospect.created_at.desc()).all()
        return templates.TemplateResponse(
            "prospects_list.html",
            {"request": request, "prospects": prospects}
        )
    finally:
        db.close()


@app.get("/prospects/new", response_class=HTMLResponse)
async def new_prospect_form(request: Request):
    """Show new prospect form."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse(
        "prospect_form.html",
        {"request": request, "prospect": None}
    )


@app.post("/prospects/new")
async def create_prospect(request: Request):
    """Create a new prospect."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    form = await request.form()
    
    db = SessionLocal()
    try:
        # IMPROVEMENT 4: Only set revenue if explicitly provided (no default)
        estimated_revenue = form.get("estimated_revenue", "").strip()
        estimated_revenue_value = None
        if estimated_revenue:
            try:
                estimated_revenue_value = float(estimated_revenue)
            except ValueError:
                estimated_revenue_value = None
        
        next_follow_up_str = form.get("next_follow_up", "").strip()
        next_follow_up = None
        if next_follow_up_str:
            try:
                next_follow_up = datetime.strptime(next_follow_up_str, "%Y-%m-%d").date()
            except ValueError:
                next_follow_up = None
        
        prospect = Prospect(
            name=form.get("name", "").strip(),
            company=form.get("company", "").strip() or None,
            email=form.get("email", "").strip() or None,
            phone=form.get("phone", "").strip() or None,
            source=form.get("source", "").strip() or None,
            stage=form.get("stage", "New"),
            estimated_revenue=estimated_revenue_value,  # IMPROVEMENT 4: No default!
            next_follow_up=next_follow_up,
            notes=form.get("notes", "").strip() or None
        )
        db.add(prospect)
        db.commit()
        
        return RedirectResponse(url="/prospects", status_code=303)
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse(
            "prospect_form.html",
            {"request": request, "error": f"Error creating prospect: {str(e)}"}
        )
    finally:
        db.close()


# ==================== DASHBOARD ====================

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard page."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    db = SessionLocal()
    try:
        total_clients = db.query(Client).count()
        active_clients = db.query(Client).filter(Client.status == "Active").count()
        total_prospects = db.query(Prospect).count()
        
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "total_clients": total_clients,
                "active_clients": active_clients,
                "total_prospects": total_prospects
            }
        )
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

