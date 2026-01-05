"""
Main FastAPI application for the CRM tool.

This is a server-rendered application using Jinja2 templates.
All routes return HTML pages, not JSON APIs.
"""
from fastapi import FastAPI, Depends, Request, Form, HTTPException, Query, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse, Response, JSONResponse
import asyncio
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import date, datetime, timedelta
import csv
import io
import math
import os
import logging
import time
import asyncio
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from performance import PerformanceMiddleware, get_cache, set_cache, clear_cache

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from database import get_db, engine, Base
from models import Client, Contact, Service, Task, Note, Timesheet
from schemas import (
    ClientCreate, ClientUpdate,
    ContactCreate, ServiceCreate, TaskCreate, NoteCreate,
    TimesheetCreate, TimesheetUpdate,
    UserCreate, UserUpdate
)
from crud import (
    get_client, get_clients, create_client, update_client, update_client_field, delete_client,
    calculate_client_revenue_async,
    create_contact, delete_contact,
    create_service, update_service, delete_service,
    create_task, update_task_status, delete_task,
    create_note, delete_note,
    get_timesheets, get_timesheet, create_timesheet, update_timesheet, delete_timesheet,
    get_timesheet_summary,
    get_users, get_user, get_user_by_email, create_user, update_user, delete_user
)
from auth import (
    get_current_user, verify_user, has_permission, require_permission,
    get_default_permissions, can_edit_timesheet, can_delete_timesheet
)

# Import migration utilities
from migrations import migrate_database_schema

# Note: Base.metadata.create_all() moved to startup event to prevent crashes
# if database is unavailable during import

# Auto-bootstrap: Create admin users if none exist
def bootstrap_admin_users():
    """Create admin users if users table is empty."""
    from models import User
    from auth import hash_password, get_default_permissions
    import json
    
    db = next(get_db())
    try:
        # Check if users table exists and has any users
        try:
            user_count = db.query(User).count()
        except Exception as e:
            # Table might not exist yet - that's OK, Base.metadata.create_all will create it
            print(f"Users table not ready yet: {e}")
            db.close()
            return
        
        if user_count == 0:
            print("No users found. Creating admin users...")
            
            # Create Admin account
            admin_permissions = get_default_permissions("Admin")
            admin = User(
                email="admin@tierneyohlms.com",
                name="Administrator",
                hashed_password=hash_password("ChangeMe123!"),
                role="Admin",
                permissions=json.dumps(admin_permissions),
                active=True
            )
            db.add(admin)
            
            # Create Paul
            paul_permissions = get_default_permissions("Admin")
            paul = User(
                email="Paul@tierneyohlms.com",
                name="Paul Ohlms",
                hashed_password=hash_password("ChangeMe123!"),
                role="Admin",
                permissions=json.dumps(paul_permissions),
                active=True
            )
            db.add(paul)
            
            # Create Dan
            dan_permissions = get_default_permissions("Admin")
            dan = User(
                email="Dan@tierneyohlms.com",
                name="Dan Tierney",
                hashed_password=hash_password("ChangeMe123!"),
                role="Admin",
                permissions=json.dumps(dan_permissions),
                active=True
            )
            db.add(dan)
            
            db.commit()
            print("[OK] Admin users created!")
            print("  - admin@tierneyohlms.com / ChangeMe123!")
            print("  - Paul@tierneyohlms.com / ChangeMe123!")
            print("  - Dan@tierneyohlms.com / ChangeMe123!")
            print("  [WARNING] CHANGE THESE PASSWORDS IMMEDIATELY!")
        else:
            print(f"[OK] Found {user_count} existing user(s). Skipping bootstrap.")
    except Exception as e:
        print(f"[ERROR] Error bootstrapping users: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


def reset_admin_users():
    """
    Forcefully reset/create admin users with default passwords.
    
    Returns:
        dict with status ("success" or "error"), created count, updated count, and message
    """
    from models import User
    from auth import hash_password, get_default_permissions
    import json
    from datetime import datetime
    
    db = None
    try:
        db = next(get_db())
    except Exception as e:
        logger.error(f"[RESET USERS] Failed to get database connection: {e}", exc_info=True)
        return {"status": "error", "message": f"Database connection failed: {str(e)}", "created": 0, "updated": 0}
    
    try:
        admin_emails = [
            "admin@tierneyohlms.com",
            "Paul@tierneyohlms.com",
            "Dan@tierneyohlms.com"
        ]
        
        admin_data = [
            ("admin@tierneyohlms.com", "Administrator"),
            ("Paul@tierneyohlms.com", "Paul Ohlms"),
            ("Dan@tierneyohlms.com", "Dan Tierney")
        ]
        
        created_count = 0
        updated_count = 0
        
        for email, name in admin_data:
            # Check if user exists
            user = db.query(User).filter(func.lower(User.email) == func.lower(email)).first()
            
            admin_permissions = get_default_permissions("Admin")
            password_hash = hash_password("ChangeMe123!")
            
            if user:
                # Update existing user
                user.name = name
                user.hashed_password = password_hash
                user.role = "Admin"
                user.permissions = json.dumps(admin_permissions)
                user.active = True
                user.updated_at = datetime.utcnow()
                updated_count += 1
                print(f"[OK] Updated user: {email}")
            else:
                # Create new user
                new_user = User(
                    email=email,
                    name=name,
                    hashed_password=password_hash,
                    role="Admin",
                    permissions=json.dumps(admin_permissions),
                    active=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(new_user)
                created_count += 1
                print(f"[OK] Created user: {email}")
        
        db.commit()
        print(f"[OK] Reset complete: {created_count} created, {updated_count} updated")
        print("  - admin@tierneyohlms.com / ChangeMe123!")
        print("  - Paul@tierneyohlms.com / ChangeMe123!")
        print("  - Dan@tierneyohlms.com / ChangeMe123!")
        return {"status": "success", "created": created_count, "updated": updated_count}
    except Exception as e:
        print(f"[ERROR] Error resetting admin users: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return {"status": "error", "message": str(e), "created": 0, "updated": 0}
    finally:
        if db:
            try:
                db.close()
            except Exception as e:
                logger.warning(f"[RESET USERS] Error closing database connection: {e}")

# Initialize FastAPI app
app = FastAPI(title="Tierney & Ohlms CRM")

# PERFORMANCE: Add performance monitoring middleware FIRST
app.add_middleware(PerformanceMiddleware)

# CRITICAL: Add TrustedHostMiddleware to handle proxy headers
# This must be added before SessionMiddleware so proxy headers are available
# When deployed behind a proxy (Render, etc.), this allows FastAPI to:
# 1. Trust X-Forwarded-* headers from the proxy
# 2. Detect HTTPS correctly for secure cookies
# 3. Set correct cookie domain/path
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # In production, specify your domain
)

# Run migrations and bootstrap on startup
# CRITICAL: Use background task to avoid blocking port binding
# This ensures Uvicorn binds to the port immediately for Render's health check
@app.on_event("startup")
async def startup_event():
    """
    Fast startup that binds port immediately, then runs database init in background.
    
    This is critical for Render deployment - the port must open within seconds.
    Database operations run in a background task to avoid blocking the event loop.
    """
    import asyncio
    
    logger.info("=" * 70)
    logger.info("Starting CRM Application")
    logger.info("=" * 70)
    logger.info("[STARTUP] Server binding to port... (database init will run in background)")
    
    # Schedule database initialization as a background task
    # This allows the server to bind to the port immediately
    asyncio.create_task(initialize_database_background())
    
    logger.info("[STARTUP] Application ready - port should be open now")
    logger.info("=" * 70)


async def initialize_database_background():
    """
    Run database initialization in background after server starts.
    
    This function runs asynchronously after the server has bound to the port,
    allowing Render's health check to succeed immediately.
    """
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    
    # Give the server a moment to bind to the port
    await asyncio.sleep(0.5)
    
    logger.info("[BACKGROUND] Starting database initialization...")
    
    # Run synchronous database operations in a thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=1)
    
    try:
        # Step 1: Create database tables (if they don't exist)
        try:
            logger.info("[BACKGROUND] Creating database tables...")
            await loop.run_in_executor(executor, Base.metadata.create_all, engine)
            logger.info("[BACKGROUND] Database tables created/verified successfully")
        except Exception as e:
            logger.error(f"[BACKGROUND ERROR] Failed to create database tables: {e}", exc_info=True)
            logger.warning("[BACKGROUND] Application will continue but database operations may fail")
        
        # Step 2: Run database migrations
        try:
            logger.info("[BACKGROUND] Running database migrations...")
            migration_success = await loop.run_in_executor(executor, migrate_database_schema)
            if migration_success:
                logger.info("[BACKGROUND] Database migrations completed successfully")
            else:
                logger.warning("[BACKGROUND] Database migrations completed with errors - some columns may be missing")
        except Exception as e:
            logger.error(f"[BACKGROUND ERROR] Database migration failed: {e}", exc_info=True)
            logger.warning("[BACKGROUND] Continuing without migrations - application will work")
        
        # Step 2.5: Self-healing schema migration (CRITICAL - runs every startup)
        try:
            logger.info("[BACKGROUND] Running self-healing schema migration...")
            from self_heal_schema import self_heal_all_schema
            heal_success = await loop.run_in_executor(executor, self_heal_all_schema)
            if heal_success:
                logger.info("[BACKGROUND] ✓ Self-healing schema migration completed successfully")
            else:
                logger.warning("[BACKGROUND] ⚠ Self-healing schema migration completed with issues")
                logger.warning("[BACKGROUND] Application will continue but some features may not work")
        except Exception as e:
            logger.error(f"[BACKGROUND ERROR] Self-healing schema migration failed: {e}", exc_info=True)
            logger.warning("[BACKGROUND] Continuing without self-healing - application may experience errors")
        
        # Step 2.6: Comprehensive schema fix (backup - runs after self-healing)
        try:
            logger.info("[BACKGROUND] Running comprehensive schema fix (backup)...")
            from schema_fix import fix_all_schema_drift
            schema_success, schema_report = await loop.run_in_executor(executor, fix_all_schema_drift)
            if schema_success:
                logger.info("[BACKGROUND] Comprehensive schema fix completed successfully")
            else:
                logger.warning(f"[BACKGROUND] Schema fix completed with issues:\n{schema_report}")
        except Exception as e:
            logger.debug(f"[BACKGROUND] Comprehensive schema fix not available: {e}")
        
        # Step 3: Reset/Create admin users
        try:
            logger.info("[BACKGROUND] Resetting admin users...")
            result = await loop.run_in_executor(executor, reset_admin_users)
            if result and result.get("status") == "success":
                created = result.get("created", 0)
                updated = result.get("updated", 0)
                logger.info(f"[BACKGROUND] Admin users ready: {created} created, {updated} updated")
            else:
                logger.warning("[BACKGROUND] Admin user reset had issues - check logs")
        except Exception as e:
            logger.error(f"[BACKGROUND ERROR] Failed to reset admin users: {e}", exc_info=True)
            logger.warning("[BACKGROUND] Continuing without admin users - login may not work")
        
        logger.info("[BACKGROUND] Database initialization complete!")
        
    except Exception as e:
        logger.error(f"[BACKGROUND ERROR] Unexpected error during database initialization: {e}", exc_info=True)
    finally:
        executor.shutdown(wait=False)

# Add session middleware for authentication
# CRITICAL FIX: Configure session cookies to work behind proxy (Render, etc.)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

# Detect if we're behind a proxy (HTTPS) or local development
# Render and similar services set X-Forwarded-Proto header
IS_PRODUCTION = os.getenv("RENDER", "").lower() == "true" or os.getenv("ENVIRONMENT", "").lower() == "production"
USE_HTTPS = IS_PRODUCTION  # Assume HTTPS in production

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=604800,  # 7 days
    same_site="lax",  # Allows cookies on top-level navigations (redirects)
    https_only=USE_HTTPS,  # Secure cookies in production (behind HTTPS proxy)
    # Note: SessionMiddleware automatically detects HTTPS from X-Forwarded-Proto
    # when TrustedHostMiddleware is configured (which we added above)
)

# Setup templates and static files
# Configure Jinja2 to handle UTF-8 encoding gracefully
templates = Jinja2Templates(
    directory="templates",
    # Ensure UTF-8 encoding is used for all template files
    # This prevents UnicodeDecodeError when templates have encoding issues
    autoescape=False  # We handle escaping in templates manually
)
# Set encoding explicitly for template loading
templates.env.auto_reload = True  # Useful for development

# Add custom Jinja2 filters
import json as json_lib
def from_json(value):
    """Jinja2 filter to parse JSON string."""
    if not value:
        return {}
    try:
        return json_lib.loads(value)
    except:
        return {}

templates.env.filters["from_json"] = from_json
templates.env.filters["tojson"] = json_lib.dumps

app.mount("/static", StaticFiles(directory="static"), name="static")


# ============================================================================
# Authentication Routes
# ============================================================================

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Login page - always returns the login form.
    
    Step 1: Restore Basic Page Functionality
    - No authentication checks
    - No redirects
    - Always returns login page HTML
    """
    try:
        return templates.TemplateResponse("login.html", {"request": request, "error": None})
    except Exception as e:
        logger.error(f"[LOGIN PAGE ERROR] Failed to render login page: {e}", exc_info=True)
        # Return a simple error page if template fails
        return HTMLResponse(
            content="<h1>Login</h1><p>Login page temporarily unavailable. Please try again.</p>",
            status_code=500
        )


@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Handle login - redirects to dashboard on success.
    
    State transitions:
    1. Bootstrap users if none exist
    2. Verify user credentials
    3. Set session if valid
    4. Redirect to dashboard or show error
    """
    from models import User as UserModel
    from auth import verify_user, set_user_session
    
    # Bootstrap users if none exist
    try:
        user_count = db.query(UserModel).count()
        if user_count == 0:
            bootstrap_admin_users()
            db.expire_all()
    except Exception as e:
        error_context = {
            "function": "login",
            "step": "bootstrap_users",
            "email": email.strip() if email else "unknown",
            "error_type": type(e).__name__,
            "error_message": str(e)
        }
        print(f"[LOGIN ERROR] {error_context}")
        import traceback
        traceback.print_exc()
    
    # Verify credentials
    try:
        user = verify_user(db, email, password)
    except Exception as e:
        # Specific error handling for different exception types
        error_type = type(e).__name__
        email_clean = email.strip() if email else "unknown"
        
        error_context = {
            "function": "login",
            "step": "verify_user",
            "email": email_clean,
            "error_type": error_type,
            "error_message": str(e)
        }
        print(f"[LOGIN ERROR] {error_context}")
        import traceback
        traceback.print_exc()
        
        # Provide precise, actionable error messages
        if "UndefinedColumn" in error_type or "ProgrammingError" in error_type:
            error_msg = "Database configuration error. Please contact support. (Error: Database schema mismatch)"
        elif "OperationalError" in error_type or "Connection" in error_type:
            error_msg = "Database connection error. Please try again in a moment."
        elif "AttributeError" in error_type:
            error_msg = "System configuration error. Please contact support. (Error: Missing required attributes)"
        else:
            error_msg = f"Login error: {error_type}. Please try again or contact support if the problem persists."
        
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": error_msg},
            status_code=500
        )
    
    if not user:
        error_msg = "Invalid email or password."
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": error_msg},
            status_code=401
        )
    
    # Step 2: Repair Login POST Logic
    # Set session and redirect
    try:
        # Set the session
        set_user_session(request, user)
        logger.info(f"[LOGIN] Session set for user {user.id} ({user.email})")
        
        # Redirect to dashboard on success
        # The session cookie will be set automatically by SessionMiddleware
        logger.info(f"[LOGIN] Redirecting user {user.id} to dashboard")
        logger.info(f"[LOGIN] Session state before redirect - user_id: {request.session.get('user_id')}, keys: {list(request.session.keys())}")
        
        # Create redirect response
        # SessionMiddleware will automatically:
        # 1. Save session data
        # 2. Set session cookie in response headers
        # 3. Include cookie in redirect response
        response = RedirectResponse(url="/dashboard", status_code=303)
        
        # Log cookie information for debugging
        # Check if we're behind a proxy (HTTPS)
        is_https = request.url.scheme == "https" or request.headers.get("X-Forwarded-Proto") == "https"
        logger.info(f"[LOGIN] Redirect created - HTTPS: {is_https}, URL scheme: {request.url.scheme}")
        logger.info(f"[LOGIN] X-Forwarded-Proto: {request.headers.get('X-Forwarded-Proto', 'not set')}")
        
        return response
    except ValueError as e:
        # Invalid user object
        error_context = {
            "function": "login",
            "step": "set_user_session",
            "email": email.strip() if email else "unknown",
            "user_id": getattr(user, 'id', None),
            "error_type": "ValueError",
            "error_message": str(e)
        }
        logger.error(f"[LOGIN ERROR] {error_context}")
        error_msg = "Invalid user data. Please contact support. (Error: User object validation failed)"
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": error_msg},
            status_code=500
        )
    except RuntimeError as e:
        # Session configuration error
        error_context = {
            "function": "login",
            "step": "set_user_session",
            "email": email.strip() if email else "unknown",
            "user_id": getattr(user, 'id', None),
            "error_type": "RuntimeError",
            "error_message": str(e)
        }
        logger.error(f"[LOGIN ERROR] {error_context}")
        error_msg = str(e) if "Session middleware" in str(e) else "Session error. Please try again or contact support."
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": error_msg},
            status_code=500
        )
    except Exception as e:
        # Unexpected error
        error_context = {
            "function": "login",
            "step": "set_user_session",
            "email": email.strip() if email else "unknown",
            "user_id": getattr(user, 'id', None),
            "error_type": type(e).__name__,
            "error_message": str(e)
        }
        logger.error(f"[LOGIN ERROR] {error_context}")
        import traceback
        traceback.print_exc()
        error_msg = f"Unexpected error during login. Please contact support. (Error: {type(e).__name__})"
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": error_msg},
            status_code=500
        )


@app.get("/logout")
async def logout(request: Request):
    """Logout user and clear session."""
    from auth import clear_user_session
    clear_user_session(request)
    return RedirectResponse(url="/login", status_code=303)


# ============================================================================
# Client Routes
# ============================================================================

@app.get("/")
async def root(request: Request):
    """Redirect root to login page."""
    return RedirectResponse(url="/login", status_code=303)

@app.get("/health")
async def health_check():
    """Health check endpoint - no auth required."""
    return {"status": "ok", "service": "tierney-ohlms-crm"}


@app.get("/clients", response_class=HTMLResponse)
async def clients_list(
    request: Request,
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    follow_up: Optional[str] = Query(None),
    sort_by: str = Query("name"),
    sort_order: str = Query("asc"),
    db: Session = Depends(get_db)
):
    """Display list of all clients with optional search, filtering, and sorting."""
    try:
        current_user = get_current_user(request)
        if not current_user:
            logger.warning("Clients list access denied: No authenticated user")
            return RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        logger.error(f"Error getting current user: {e}", exc_info=True)
        return RedirectResponse(url="/login", status_code=303)
    
    # Get clients with error handling
    clients = []
    try:
        clients = get_clients(
            db, 
            search=search,
            status_filter=status,
            entity_type_filter=entity_type,
            follow_up_filter=follow_up,
            sort_by=sort_by,
            sort_order=sort_order
        )
        logger.info(f"Loaded {len(clients)} clients with filters: search={search}, status={status}")
    except SQLAlchemyError as e:
        logger.error(f"Database error loading clients: {e}", exc_info=True)
        db.rollback()
        clients = []
    except Exception as e:
        logger.error(f"Unexpected error loading clients: {e}", exc_info=True)
        clients = []
    
    # Calculate revenue and timesheet summaries for each client
    # NO FALLBACKS: If columns are missing, this will crash (migration must fix it)
    from crud import get_timesheet_summary
    clients_with_data = []
    for client in clients:
        revenue = await calculate_client_revenue_async(client.id)
        timesheet_summary = get_timesheet_summary(db, client_id=client.id)
        
        clients_with_data.append({
            "client": client,
            "revenue": revenue,
            "total_hours": timesheet_summary.get("total_hours", 0.0),
            "billable_hours": timesheet_summary.get("billable_hours", 0.0),
            "timesheet_entries": timesheet_summary.get("total_entries", 0)
        })
    
    # Get unique values for filter dropdowns with error handling
    statuses = []
    entity_types = []
    try:
        all_clients = db.query(Client).all()
        statuses = sorted(set(c.status for c in all_clients if c.status))
        entity_types = sorted(set(c.entity_type for c in all_clients if c.entity_type))
    except Exception as e:
        logger.warning(f"Error getting filter options: {e}")
        statuses = []
        entity_types = []
    
    # Render template with error handling
    try:
        return templates.TemplateResponse(
            "clients_list.html",
            {
                "request": request, 
                "clients_with_revenue": clients_with_data,
                "search": search,
                "status_filter": status,
                "entity_type_filter": entity_type,
                "follow_up_filter": follow_up,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "statuses": statuses,
                "entity_types": entity_types,
                "today": date.today(),
                "user": current_user
            }
        )
    except Exception as e:
        logger.error(f"Error rendering clients list template: {e}", exc_info=True)
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "An error occurred loading the clients list. Please try again."
            },
            status_code=500
        )


# ============================================================================
# Prospects Routes
# ============================================================================

@app.get("/prospects", response_class=HTMLResponse)
async def prospects_list(
    request: Request,
    search: Optional[str] = Query(None),
    stage: Optional[str] = Query(None),  # New, Contacted, Proposal, Negotiation, Closed-Won, Closed-Lost
    owner: Optional[str] = Query(None),
    follow_up: Optional[str] = Query(None),  # needed, overdue, all
    sort_by: str = Query("name"),
    sort_order: str = Query("asc"),
    db: Session = Depends(get_db)
):
    """Display list of all prospects with pipeline filtering."""
    try:
        current_user = get_current_user(request)
        if not current_user:
            logger.warning("Prospects list access denied: No authenticated user")
            return RedirectResponse(url="/login", status_code=303)
        
        permission_check = require_permission(current_user, "view_clients")
        if permission_check:
            return permission_check
    except Exception as e:
        logger.error(f"Error in authentication/authorization: {e}", exc_info=True)
        return RedirectResponse(url="/login", status_code=303)
    
    # Get prospects with error handling
    prospects = []
    try:
        prospects = get_clients(
            db,
            search=search,
            status_filter="Prospect",  # Always filter to prospects only
            follow_up_filter=follow_up,
            sort_by=sort_by,
            sort_order=sort_order
        )
        logger.info(f"Loaded {len(prospects)} prospects")
    except SQLAlchemyError as e:
        logger.error(f"Database error loading prospects: {e}", exc_info=True)
        db.rollback()
        prospects = []
    except Exception as e:
        logger.error(f"Unexpected error loading prospects: {e}", exc_info=True)
        prospects = []
        
    # Calculate estimated revenue for each prospect
    # NO FALLBACKS: If columns are missing, this will crash (migration must fix it)
    prospects_with_data = []
    for prospect in prospects:
        estimated_revenue = await calculate_client_revenue_async(prospect.id)
        
        # Determine stage
        stage_value = "New"
        if prospect.next_follow_up_date:
            days_until = (prospect.next_follow_up_date - date.today()).days
            if days_until < 0:
                stage_value = "Negotiation"
            elif days_until <= 7:
                stage_value = "Proposal"
            elif days_until <= 30:
                stage_value = "Contacted"
        
        # Check filters
        if stage and stage != stage_value:
            continue
        
        if owner and prospect.owner_name and owner.lower() not in prospect.owner_name.lower():
            continue
        
        # Get expected close date
        expected_close_date = None
        if prospect.next_follow_up_date:
            expected_close_date = prospect.next_follow_up_date
        elif prospect.created_at:
            if hasattr(prospect.created_at, 'date'):
                expected_close_date = prospect.created_at.date()
            else:
                expected_close_date = prospect.created_at
        
        # Get first contact for display
        first_contact = None
        if prospect.contacts:
            first_contact = prospect.contacts[0] if len(prospect.contacts) > 0 else None
        
        prospects_with_data.append({
            "client": prospect,
            "contact": first_contact,
            "estimated_revenue": estimated_revenue,
            "estimated_revenue_formatted": f"{estimated_revenue:,.0f}",
            "stage": stage_value,
            "expected_close_date": expected_close_date
        })
    
    # Get unique owners for filter with error handling
    owners = []
    try:
        all_prospects = db.query(Client).filter(Client.status == "Prospect").all()
        owners = sorted(set(p.owner_name for p in all_prospects if p.owner_name))
    except Exception as e:
        logger.warning(f"Error getting owners list: {e}")
        owners = []
    
    # Calculate pipeline totals
    total_estimated = sum(p["estimated_revenue"] for p in prospects_with_data)
    total_count = len(prospects_with_data)
    total_estimated_formatted = f"{total_estimated:,.0f}"
    
    # Render template with error handling
    try:
        return templates.TemplateResponse(
            "prospects_list.html",
            {
                "request": request,
                "prospects": prospects_with_data,
                "search": search,
                "stage_filter": stage,
                "owner_filter": owner,
                "follow_up_filter": follow_up,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "owners": owners,
                "total_estimated": total_estimated,
                "total_estimated_formatted": total_estimated_formatted,
                "total_count": total_count,
                "today": date.today(),
                "user": current_user
            }
        )
    except Exception as e:
        logger.error(f"Error rendering prospects list template: {e}", exc_info=True)
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "An error occurred loading the prospects list. Please try again."
            },
            status_code=500
        )


@app.get("/prospects/export")
async def prospects_export(
    request: Request,
    search: Optional[str] = Query(None),
    stage: Optional[str] = Query(None),
    owner: Optional[str] = Query(None),
    follow_up: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Export filtered prospects list to CSV."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "export_clients")
    if permission_check:
        return permission_check
    
    # Get all prospects
    prospects = get_clients(
        db,
        search=search,
        status_filter="Prospect",
        follow_up_filter=follow_up
    )
    
    # Filter by stage and owner (same logic as list view)
    prospects_with_data = []
    for prospect in prospects:
        estimated_revenue = await calculate_client_revenue_async(prospect.id)
        if estimated_revenue == 0:
            estimated_revenue = 75000
        
        # Determine stage
        stage_value = "New"
        if prospect.next_follow_up_date:
            days_until = (prospect.next_follow_up_date - date.today()).days
            if days_until < 0:
                stage_value = "Negotiation"
            elif days_until <= 7:
                stage_value = "Proposal"
            elif days_until <= 30:
                stage_value = "Contacted"
        
        if stage and stage != stage_value:
            continue
        
        if owner and prospect.owner_name and owner.lower() not in prospect.owner_name.lower():
            continue
        
        prospects_with_data.append({
            "client": prospect,
            "estimated_revenue": estimated_revenue,
            "stage": stage_value
        })
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "Company Name",
        "Stage",
        "Owner Name",
        "Owner Email",
        "Next Follow-Up Date",
        "Estimated Value",
        "Entity Type",
        "Created At"
    ])
    
    # Write data
    for item in prospects_with_data:
        client = item["client"]
        writer.writerow([
            client.legal_name,
            item["stage"],
            client.owner_name or "",
            client.owner_email or "",
            client.next_follow_up_date.strftime("%Y-%m-%d") if client.next_follow_up_date else "",
            f"{item['estimated_revenue']:.2f}",
            client.entity_type or "",
            client.created_at.strftime("%Y-%m-%d") if client.created_at else ""
        ])
    
    # Return CSV file
    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="prospects_export_{datetime.now().strftime("%Y%m%d")}.csv"'
        }
    )


@app.get("/prospects/new", response_class=HTMLResponse)
async def prospect_new_form(request: Request):
    """Display form to create a new prospect."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "create_clients")
    if permission_check:
        return permission_check
    
    return templates.TemplateResponse(
        "prospect_form.html",
        {"request": request, "user": current_user, "today": date.today()}
    )


@app.post("/prospects/new")
async def prospect_create(
    request: Request,
    name: str = Form(...),
    company: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    source: Optional[str] = Form(None),
    stage: Optional[str] = Form("New"),
    estimated_revenue: Optional[float] = Form(None),
    next_follow_up: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Create a new prospect (client with status='Prospect')."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "create_clients")
    if permission_check:
        return permission_check
    
    # Parse follow-up date
    follow_up_date = None
    if next_follow_up:
        try:
            follow_up_date = datetime.strptime(next_follow_up, "%Y-%m-%d").date()
        except ValueError:
            pass
    
    # Create client with status='Prospect'
    client_data = ClientCreate(
        legal_name=company if company else name,  # Use company name or contact name
        entity_type=None,
        fiscal_year_end=None,
        status="Prospect",
        owner_name=current_user.name if current_user else None,
        owner_email=current_user.email if current_user else None,
        next_follow_up_date=follow_up_date
    )
    
    try:
        # Create client with status='Prospect'
        client = create_client(db, client_data)
        logger.info(f"Created prospect client: {client.id} - {client.legal_name}")
        
        # Always create a contact if name is provided (even if name == company)
        # This ensures contact info is stored and can be displayed in the prospects table
        if name:
            try:
                contact_data = ContactCreate(
                    client_id=client.id,
                    name=name,
                    email=email,
                    phone=phone,
                    role="Primary Contact"
                )
                create_contact(db, contact_data)
                logger.info(f"Created contact for prospect {client.id}: {name}")
            except Exception as e:
                logger.warning(f"Could not create contact for prospect {client.id}: {e}", exc_info=True)
                # Continue even if contact creation fails - client is already created
        
        # If notes provided, create a note
        if notes:
            try:
                note_data = NoteCreate(client_id=client.id, content=notes)
                create_note(db, note_data)
                logger.info(f"Created note for prospect {client.id}")
            except Exception as e:
                logger.warning(f"Could not create note for prospect {client.id}: {e}", exc_info=True)
                # Continue even if note creation fails
        
        # Commit all changes
        db.commit()
        logger.info(f"Successfully created prospect: {client.id} - {client.legal_name}")
        
        return RedirectResponse(url="/prospects", status_code=303)
    except SQLAlchemyError as e:
        logger.error(f"Database error creating prospect: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: Failed to create prospect")
    except Exception as e:
        logger.error(f"Error creating prospect: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create prospect: {str(e)}")


@app.post("/prospects/{client_id}/convert")
async def convert_prospect_to_client(
    request: Request,
    client_id: int,
    db: Session = Depends(get_db)
):
    """Convert a prospect to an active client."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "edit_clients")
    if permission_check:
        return permission_check
    
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Prospect not found")
    
    if client.status != "Prospect":
        raise HTTPException(status_code=400, detail="This is not a prospect")
    
    # Update status to Active
    update_client_field(db, client_id, "status", "Active")
    
    return RedirectResponse(url=f"/clients/{client_id}", status_code=303)


@app.get("/clients/new", response_class=HTMLResponse)
async def client_new_form(request: Request):
    """Display form to create a new client."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "create_clients")
    if permission_check:
        return permission_check
    
    return templates.TemplateResponse(
        "client_form.html",
        {"request": request, "client": None, "user": current_user, "today": date.today()}
    )


@app.post("/clients/new")
async def client_create(
    request: Request,
    legal_name: str = Form(...),
    entity_type: Optional[str] = Form(None),
    fiscal_year_end: Optional[str] = Form(None),
    status: str = Form("Prospect"),
    owner_name: Optional[str] = Form(None),
    owner_email: Optional[str] = Form(None),
    next_follow_up_date: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Create a new client."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "create_clients")
    if permission_check:
        return permission_check
    
    follow_up_date = None
    if next_follow_up_date:
        try:
            follow_up_date = datetime.strptime(next_follow_up_date, "%Y-%m-%d").date()
        except ValueError:
            pass
    
    client_data = ClientCreate(
        legal_name=legal_name,
        entity_type=entity_type,
        fiscal_year_end=fiscal_year_end,
        status=status,
        owner_name=owner_name,
        owner_email=owner_email,
        next_follow_up_date=follow_up_date
    )
    client = create_client(db, client_data)
    return RedirectResponse(url=f"/clients/{client.id}", status_code=303)


@app.get("/clients/{client_id}", response_class=HTMLResponse)
async def client_detail(
    request: Request,
    client_id: int,
    db: Session = Depends(get_db)
):
    """Display client detail page with all related data."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "view_clients")
    if permission_check:
        return permission_check
    
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Get timesheet summaries
    from crud import get_timesheet_summary
    from datetime import timedelta
    
    today = date.today()
    month_start = date(today.year, today.month, 1)
    year_start = date(today.year, 1, 1)
    
    # All-time summary
    summary_all = get_timesheet_summary(db, client_id=client_id)
    
    # This month summary
    summary_month = get_timesheet_summary(
        db,
        client_id=client_id,
        date_from=month_start,
        date_to=today
    )
    
    # This year summary
    summary_year = get_timesheet_summary(
        db,
        client_id=client_id,
        date_from=year_start,
        date_to=today
    )
    
    # Get recent timesheet entries (last 10)
    recent_timesheets = get_timesheets(
        db,
        client_id=client_id,
        limit=10
    )
    
    # Get all timesheets for monthly breakdown
    all_timesheets = get_timesheets(db, client_id=client_id, limit=1000)
    
    # Calculate monthly breakdown (last 12 months)
    monthly_breakdown = {}
    for i in range(12):
        month_date = date(today.year, today.month, 1) - timedelta(days=30*i)
        month_start_date = date(month_date.year, month_date.month, 1)
        if month_date.month == 12:
            month_end_date = date(month_date.year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end_date = date(month_date.year, month_date.month + 1, 1) - timedelta(days=1)
        
        month_summary = get_timesheet_summary(
            db,
            client_id=client_id,
            date_from=month_start_date,
            date_to=min(month_end_date, today)
        )
        month_key = month_start_date.strftime("%Y-%m")
        monthly_breakdown[month_key] = {
            "month": month_start_date.strftime("%B %Y"),
            "total_hours": month_summary["total_hours"],
            "billable_hours": month_summary["billable_hours"],
            "non_billable_hours": month_summary["non_billable_hours"],
            "entries": month_summary["total_entries"]
        }
    
    # Get related data (explicitly load relationships)
    contacts = []
    services = []
    tasks = []
    notes = []
    try:
        contacts = list(client.contacts) if client.contacts else []
    except Exception as e:
        logger.warning(f"Error loading contacts for client {client_id}: {e}")
        contacts = []
    
    try:
        services = list(client.services) if client.services else []
    except Exception as e:
        logger.warning(f"Error loading services for client {client_id}: {e}")
        services = []
    
    try:
        tasks = list(client.tasks) if client.tasks else []
    except Exception as e:
        logger.warning(f"Error loading tasks for client {client_id}: {e}")
        tasks = []
    
    try:
        notes = list(client.notes) if client.notes else []
    except Exception as e:
        logger.warning(f"Error loading notes for client {client_id}: {e}")
        notes = []
    
    return templates.TemplateResponse(
        "client_detail.html",
        {
            "request": request,
            "client": client,
            "contacts": contacts,
            "services": services,
            "tasks": tasks,
            "notes": notes,
            "user": current_user,
            "timesheet_summary_all": summary_all,
            "timesheet_summary_month": summary_month,
            "timesheet_summary_year": summary_year,
            "recent_timesheets": recent_timesheets,
            "monthly_breakdown": monthly_breakdown,
            "today": today
        }
    )


@app.get("/clients/{client_id}/edit", response_class=HTMLResponse)
async def client_edit_form(
    request: Request,
    client_id: int,
    db: Session = Depends(get_db)
):
    """Display form to edit an existing client."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "edit_clients")
    if permission_check:
        return permission_check
    
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return templates.TemplateResponse(
        "client_form.html",
        {"request": request, "client": client, "user": current_user, "today": date.today()}
    )


@app.post("/clients/{client_id}/edit")
async def client_update(
    request: Request,
    client_id: int,
    legal_name: str = Form(...),
    entity_type: Optional[str] = Form(None),
    fiscal_year_end: Optional[str] = Form(None),
    status: str = Form(...),
    owner_name: Optional[str] = Form(None),
    owner_email: Optional[str] = Form(None),
    next_follow_up_date: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Update an existing client."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "edit_clients")
    if permission_check:
        return permission_check
    
    follow_up_date = None
    if next_follow_up_date:
        try:
            follow_up_date = datetime.strptime(next_follow_up_date, "%Y-%m-%d").date()
        except ValueError:
            pass
    
    client_update_data = ClientUpdate(
        legal_name=legal_name,
        entity_type=entity_type,
        fiscal_year_end=fiscal_year_end,
        status=status,
        owner_name=owner_name,
        owner_email=owner_email,
        next_follow_up_date=follow_up_date
    )
    client = update_client(db, client_id, client_update_data)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return RedirectResponse(url=f"/clients/{client_id}", status_code=303)


@app.post("/clients/{client_id}/update-field")
async def client_update_field(
    request: Request,
    client_id: int,
    field: str = Form(...),
    value: str = Form(None),
    db: Session = Depends(get_db)
):
    """Update a single field on a client (for inline editing)."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "edit_clients")
    if permission_check:
        return permission_check
    
    # Whitelist of allowed fields for security
    allowed_fields = {
        "legal_name", "entity_type", "fiscal_year_end", "status",
        "owner_name", "owner_email", "next_follow_up_date"
    }
    
    if field not in allowed_fields:
        raise HTTPException(status_code=400, detail=f"Field '{field}' is not allowed to be updated")
    
    # Convert empty string to None
    if value == "":
        value = None
    
    try:
        client = update_client_field(db, client_id, field, value)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        return Response(content="OK", status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating client field: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to update field")


@app.post("/clients/{client_id}/delete")
async def client_delete(
    request: Request,
    client_id: int,
    db: Session = Depends(get_db)
):
    """Delete a client."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "delete_clients")
    if permission_check:
        return permission_check
    
    success = delete_client(db, client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return RedirectResponse(url="/clients", status_code=303)


# ============================================================================
# Contact Routes
# ============================================================================

@app.get("/clients/{client_id}/contacts/new", response_class=HTMLResponse)
async def contact_new_form(
    request: Request,
    client_id: int,
    db: Session = Depends(get_db)
):
    """Display form to create a new contact for a client."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "create_contacts")
    if permission_check:
        return permission_check
    
    # Verify client exists
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return templates.TemplateResponse(
        "contact_form.html",
        {
            "request": request,
            "client": client,
            "user": current_user
        }
    )


@app.post("/clients/{client_id}/contacts/new")
async def contact_create(
    request: Request,
    client_id: int,
    name: str = Form(...),
    role: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Create a new contact for a client."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "create_contacts")
    if permission_check:
        return permission_check
    
    # Verify client exists
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    try:
        contact_data = ContactCreate(
            client_id=client_id,
            name=name,
            role=role,
            email=email,
            phone=phone
        )
        create_contact(db, contact_data)
        return RedirectResponse(url=f"/clients/{client_id}", status_code=303)
    except Exception as e:
        print(f"Error creating contact: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to create contact")


@app.post("/contacts/{contact_id}/delete")
async def contact_delete(
    request: Request,
    contact_id: int,
    client_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Delete a contact."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "delete_contacts")
    if permission_check:
        return permission_check
    
    delete_contact(db, contact_id)
    return RedirectResponse(url=f"/clients/{client_id}", status_code=303)


# ============================================================================
# Service Routes
# ============================================================================

@app.get("/clients/{client_id}/services/new", response_class=HTMLResponse)
async def service_new_form(
    request: Request,
    client_id: int,
    db: Session = Depends(get_db)
):
    """Display form to create a new service for a client."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "create_services")
    if permission_check:
        return permission_check
    
    # Verify client exists
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return templates.TemplateResponse(
        "service_form.html",
        {
            "request": request,
            "client": client,
            "user": current_user,
            "service": None
        }
    )


@app.post("/clients/{client_id}/services/new")
async def service_create(
    request: Request,
    client_id: int,
    service_type: str = Form(...),
    billing_frequency: Optional[str] = Form(None),
    monthly_fee: Optional[str] = Form(None),  # Accept as string to handle empty strings
    db: Session = Depends(get_db)
):
    """Create a new service for a client."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "create_services")
    if permission_check:
        return permission_check
    
    # Verify client exists
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Validate and convert monthly_fee
    monthly_fee_value = None
    if monthly_fee is not None and monthly_fee.strip():  # Check for non-empty string
        try:
            fee_float = float(monthly_fee.strip())
            if fee_float < 0:
                raise HTTPException(status_code=400, detail="Monthly fee cannot be negative")
            monthly_fee_value = fee_float
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid monthly fee format: '{monthly_fee}'. Please enter a valid number.")
    
    # Validate service_type is not empty
    if not service_type or not service_type.strip():
        raise HTTPException(status_code=400, detail="Service type is required")
    
    # Validate billing_frequency if provided
    if billing_frequency and billing_frequency.strip():
        valid_frequencies = ["Monthly", "Quarterly", "Annual", "One-time"]
        if billing_frequency not in valid_frequencies:
            logger.warning(f"Invalid billing_frequency: {billing_frequency}, allowing anyway")
    
    try:
        service_data = ServiceCreate(
            client_id=client_id,
            service_type=service_type.strip(),
            billing_frequency=billing_frequency.strip() if billing_frequency and billing_frequency.strip() else None,
            monthly_fee=monthly_fee_value,
            active=True
        )
        created_service = create_service(db, service_data)
        logger.info(f"Successfully created service {created_service.id} for client {client_id}: {service_type}")
        return RedirectResponse(url=f"/clients/{client_id}", status_code=303)
    except SQLAlchemyError as e:
        logger.error(f"Database error creating service for client {client_id}: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: Failed to create service. Please check the service data and try again.")
    except ValueError as e:
        logger.error(f"Validation error creating service for client {client_id}: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Invalid service data: {str(e)}")
    except HTTPException:
        raise  # Re-raise HTTPException (e.g., from validation above)
    except Exception as e:
        logger.error(f"Error creating service for client {client_id}: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create service: {str(e)}")


@app.post("/services/{service_id}/toggle")
async def service_toggle(
    request: Request,
    service_id: int,
    client_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Toggle service active status."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    service = db.query(Service).filter(Service.id == service_id).first()
    if service:
        update_service(db, service_id, not service.active)
    return RedirectResponse(url=f"/clients/{client_id}", status_code=303)


@app.post("/services/{service_id}/delete")
async def service_delete(
    request: Request,
    service_id: int,
    client_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Delete a service."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    delete_service(db, service_id)
    return RedirectResponse(url=f"/clients/{client_id}", status_code=303)


# ============================================================================
# Task Routes
# ============================================================================

@app.post("/clients/{client_id}/tasks/new")
async def task_create(
    request: Request,
    client_id: int,
    title: str = Form(...),
    due_date: Optional[str] = Form(None),
    status: str = Form("Open"),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Create a new task for a client."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "create_tasks")
    if permission_check:
        return permission_check
    
    # Verify client exists
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    try:
        due_date_obj = None
        if due_date:
            try:
                due_date_obj = date.fromisoformat(due_date)
            except ValueError:
                pass
        
        task_data = TaskCreate(
            client_id=client_id,
            title=title,
            due_date=due_date_obj,
            status=status,
            notes=notes
        )
        create_task(db, task_data)
        return RedirectResponse(url=f"/clients/{client_id}", status_code=303)
    except Exception as e:
        print(f"Error creating task: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to create task")


@app.post("/tasks/{task_id}/update-status")
async def task_update_status(
    request: Request,
    task_id: int,
    status: str = Form(...),
    client_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Update task status."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    update_task_status(db, task_id, status)
    return RedirectResponse(url=f"/clients/{client_id}", status_code=303)


@app.post("/tasks/{task_id}/delete")
async def task_delete(
    request: Request,
    task_id: int,
    client_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Delete a task."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    delete_task(db, task_id)
    return RedirectResponse(url=f"/clients/{client_id}", status_code=303)


# ============================================================================
# Note Routes
# ============================================================================

@app.post("/clients/{client_id}/notes/new")
async def note_create(
    request: Request,
    client_id: int,
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    """Create a new note for a client."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "create_notes")
    if permission_check:
        return permission_check
    
    # Verify client exists
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    try:
        note_data = NoteCreate(client_id=client_id, content=content)
        create_note(db, note_data)
        return RedirectResponse(url=f"/clients/{client_id}", status_code=303)
    except Exception as e:
        print(f"Error creating note: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to create note")


@app.post("/notes/{note_id}/delete")
async def note_delete(
    request: Request,
    note_id: int,
    client_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Delete a note."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    delete_note(db, note_id)
    return RedirectResponse(url=f"/clients/{client_id}", status_code=303)


# ============================================================================
# Dashboard Routes
# ============================================================================

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    PERFORMANCE FIX: Fast dashboard that returns immediately.
    Revenue data loads asynchronously via /api/dashboard/revenue endpoint.
    """
    from auth import get_current_user, require_permission
    
    route_start = time.perf_counter()
    logger.info("[DASHBOARD] Fast dashboard route called...")
    
    # Fast authentication check
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "view_dashboard")
    if permission_check:
        return permission_check
    
    # Fast path: Load only essential data for immediate render
    logger.info("[DASHBOARD] Loading clients from database (fast path)...")
    try:
        all_clients = db.query(Client).all()
        logger.info(f"[DASHBOARD] Loaded {len(all_clients)} clients")
    except Exception as e:
        # Database query failed - return empty dashboard with safe defaults
        logger.error(f"[DASHBOARD] Error loading clients: {e}", exc_info=True)
        # Return empty dashboard immediately if query fails
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "user": current_user,
                "prospects": [],
                "prospects_count": 0,
                "total_prospect_revenue": 0.0,
                "won_deals": [],
                "won_count": 0,
                "total_won_revenue": 0.0,
                "lost_deals": [],
                "lost_count": 0,
                "total_lost_value": 0.0,
                "total_clients": 0,
                "active_clients": 0,
                "total_prospects": 0,
                "total_revenue": 0.0,
                "total_revenue_formatted": "0",
                "total_hours": 0.0,
                "today": date.today()
            }
        )
    
    # Step 4: Calculate statistics (with explicit error handling for each operation)
    logger.info("[DASHBOARD] Calculating statistics...")
    total_clients = len(all_clients)
    active_clients = [c for c in all_clients if c.status == "Active"]
    total_active = len(active_clients)
    logger.info(f"[DASHBOARD] Found {total_active} active clients out of {total_clients} total")
    
    # PERFORMANCE FIX: Revenue calculation moved to background/API endpoint
    # Dashboard returns immediately with cached or placeholder revenue
    logger.info(f"[DASHBOARD] Fast path - skipping revenue calculation (loads via API)")
    
    # Use placeholder revenue - will be updated via API call
    total_revenue = 0.0
    total_prospect_revenue = 0.0
    total_won_revenue = 0.0
    total_lost_value = 0.0
    
    # Schedule background task to pre-calculate revenue (non-blocking)
    try:
        background_tasks.add_task(calculate_and_cache_revenue, active_clients)
    except Exception as e:
        logger.debug(f"[DASHBOARD] Could not schedule background revenue calculation: {e}")
    
    # Calculate total hours (all timesheets)
    logger.info("[DASHBOARD] Getting timesheet summary...")
    try:
        timesheet_summary_all = get_timesheet_summary(db)
        total_hours = timesheet_summary_all.get("total_hours", 0.0)
        logger.info(f"[DASHBOARD] Total hours: {total_hours}")
    except Exception as e:
        # Error getting timesheet summary - use 0
        logger.error(f"[DASHBOARD] Error getting timesheet summary: {e}", exc_info=True)
        total_hours = 0.0
    
    # Step 5: Filter clients by status
    logger.info("[DASHBOARD] Filtering clients by status...")
    current_year = 2025
    prospects = [c for c in all_clients if c.status == "Prospect"]
    lost_clients = [c for c in all_clients if c.status == "Dead"]
    logger.info(f"[DASHBOARD] Found {len(prospects)} prospects, {len(lost_clients)} lost clients")
    
    # Won deals - Active clients (with explicit error handling)
    won_clients = []
    for client in all_clients:
        if client.status == "Active":
            # Include if created in 2025
            try:
                if client.created_at and hasattr(client.created_at, 'year'):
                    if client.created_at.year == current_year:
                        won_clients.append(client)
                        continue
            except Exception:
                pass  # Skip date check if it fails
            
            # Check if has active services (treated as won)
            try:
                services = db.query(Service).filter(
                    Service.client_id == client.id,
                    Service.active == True
                ).first()
                if services:
                    won_clients.append(client)
            except Exception as e:
                # Service query failed - skip this client
                pass
    
    # PERFORMANCE FIX: Prospect revenue loaded asynchronously
    logger.info(f"[DASHBOARD] Preparing prospect data (revenue will load via API)...")
    prospects_data = []
    total_prospect_revenue = 0.0  # Placeholder - will be updated via API
    for prospect in prospects:
        # Safely get expected close date
        expected_close_date = None
        try:
            if prospect.next_follow_up_date:
                expected_close_date = prospect.next_follow_up_date
            elif prospect.created_at:
                if hasattr(prospect.created_at, 'date'):
                    expected_close_date = prospect.created_at.date()
                else:
                    expected_close_date = prospect.created_at
        except Exception:
            pass
        
        prospects_data.append({
            "client": prospect,
            "estimated_revenue": 0.0,  # Placeholder - loaded via API
            "expected_close_date": expected_close_date
        })
    
    # PERFORMANCE FIX: Won revenue loaded asynchronously
    logger.info(f"[DASHBOARD] Preparing won deals data (revenue will load via API)...")
    won_data = []
    total_won_revenue = 0.0  # Placeholder - will be updated via API
    for client in won_clients:
        # Safely get close date
        close_date = None
        try:
            if client.created_at:
                if hasattr(client.created_at, 'date'):
                    close_date = client.created_at.date()
                else:
                    close_date = client.created_at
        except Exception:
            pass
        
        won_data.append({
            "client": client,
            "actual_revenue": 0.0,  # Placeholder - loaded via API
            "close_date": close_date
        })
    
    # PERFORMANCE FIX: Lost value loaded asynchronously
    logger.info(f"[DASHBOARD] Preparing lost deals data (revenue will load via API)...")
    lost_data = []
    total_lost_value = 0.0  # Placeholder - will be updated via API
    for client in lost_clients:
        # Safely get lost date
        lost_date = None
        try:
            if client.created_at:
                if hasattr(client.created_at, 'date'):
                    lost_date = client.created_at.date()
                else:
                    lost_date = client.created_at
        except Exception:
            pass
        
        # Get reason from notes if available (simplified - no DB query)
        reason = "Not specified"
        
        lost_data.append({
            "client": client,
            "estimated_value": 0.0,  # Placeholder - loaded via API
            "lost_date": lost_date,
            "reason": reason
        })
    
    # Prepare template data
    template_data = {
        "request": request,
        "user": current_user,
        "prospects": prospects_data,
        "prospects_count": len(prospects),
        "total_prospect_revenue": total_prospect_revenue,
        "won_deals": won_data,
        "won_count": len(won_clients),
        "total_won_revenue": total_won_revenue,
        "lost_deals": lost_data,
        "lost_count": len(lost_clients),
        "total_lost_value": total_lost_value,
        "total_clients": total_clients,
        "active_clients": total_active,
        "total_prospects": len(prospects),
        "total_revenue": total_revenue,
        "total_revenue_formatted": f"{total_revenue:,.0f}",
        "total_hours": total_hours,
        "today": date.today()
    }
    
    # PERFORMANCE: Cache the statistics for next request (optional - safe if cache unavailable)
    try:
        cache_key = f"dashboard_stats_{current_user.id}"
        background_tasks.add_task(
            set_cache,
            cache_key,
            {
                "prospects": prospects_data,
                "prospects_count": len(prospects),
                "total_prospect_revenue": total_prospect_revenue,
                "won_deals": won_data,
                "won_count": len(won_clients),
                "total_won_revenue": total_won_revenue,
                "lost_deals": lost_data,
                "lost_count": len(lost_clients),
                "total_lost_value": total_lost_value,
                "total_clients": total_clients,
                "active_clients": total_active,
                "total_prospects": len(prospects),
                "total_revenue": total_revenue,
                "total_revenue_formatted": f"{total_revenue:,.0f}",
                "total_hours": total_hours
            },
            timedelta(minutes=5)  # Cache for 5 minutes
        )
    except Exception as e:
        logger.debug(f"[DASHBOARD] Could not schedule cache update: {e}")
        # Non-critical - continue without caching
    
    # Render and return immediately - revenue loads via API
    response = templates.TemplateResponse("dashboard.html", template_data)
    route_duration = (time.perf_counter() - route_start) * 1000
    logger.info(f"[PERF] Dashboard returned in {route_duration:.2f}ms (fast path - revenue loads asynchronously)")
    return response


# ============================================================================
# Dashboard API Endpoints (Async Revenue Loading)
# ============================================================================

async def calculate_and_cache_revenue(active_clients: list):
    """
    Background task to calculate and cache revenue for all active clients.
    This runs asynchronously and doesn't block the dashboard request.
    """
    from database import SessionLocal
    logger.info(f"[REVENUE CACHE] Starting background revenue calculation for {len(active_clients)} clients...")
    
    total_revenue = 0.0
    db = None
    
    try:
        db = SessionLocal()
        
        for client in active_clients:
            try:
                revenue = await calculate_client_revenue_async(client.id)
                total_revenue += revenue
            except Exception as e:
                logger.error(f"[REVENUE CACHE] Error calculating revenue for client {client.id}: {e}")
                continue
        
        # Cache the result
        set_cache("dashboard_total_revenue", total_revenue, timedelta(minutes=10))
        logger.info(f"[REVENUE CACHE] Cached total revenue: ${total_revenue:,.2f}")
        
    except Exception as e:
        logger.error(f"[REVENUE CACHE] Error in background revenue calculation: {e}", exc_info=True)
    finally:
        if db:
            db.close()


@app.get("/api/dashboard/revenue")
async def get_dashboard_revenue(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    API endpoint to fetch dashboard revenue data asynchronously.
    Returns cached revenue if available, otherwise calculates and caches it.
    """
    from auth import get_current_user
    
    # Check authentication
    current_user = get_current_user(request)
    if not current_user:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    logger.info("[API] Revenue endpoint called - checking cache...")
    
    # Try cache first
    revenue_cache_key = "dashboard_total_revenue"
    cached_revenue = get_cache(revenue_cache_key)
    
    if cached_revenue is not None:
        logger.info(f"[API] Returning cached revenue: ${cached_revenue:,.2f}")
        return JSONResponse({
            "total_revenue": cached_revenue,
            "total_revenue_formatted": f"{cached_revenue:,.0f}",
            "cached": True
        })
    
    # No cache - calculate now
    logger.info("[API] No cache - calculating revenue...")
    
    try:
        # Get active clients
        all_clients = db.query(Client).all()
        active_clients = [c for c in all_clients if c.status == "Active"]
        prospects = [c for c in all_clients if c.status == "Prospect"]
        won_clients = [c for c in all_clients if c.status == "Active" and 
                      (c.created_at and hasattr(c.created_at, 'year') and c.created_at.year == 2025)]
        lost_clients = [c for c in all_clients if c.status == "Dead"]
        
        # Calculate revenues in parallel
        client_ids = set()
        for c in active_clients:
            client_ids.add(c.id)
        for p in prospects:
            client_ids.add(p.id)
        for w in won_clients:
            client_ids.add(w.id)
        for l in lost_clients:
            client_ids.add(l.id)
        
        # Calculate all revenues concurrently
        revenue_tasks = [calculate_client_revenue_async(cid) for cid in client_ids]
        revenues = await asyncio.gather(*revenue_tasks, return_exceptions=True)
        revenue_map = dict(zip(client_ids, revenues))
        revenue_map = {k: (v if not isinstance(v, Exception) else 0.0) for k, v in revenue_map.items()}
        
        # Calculate totals
        total_revenue = sum(revenue_map.get(c.id, 0.0) for c in active_clients)
        total_prospect_revenue = sum(revenue_map.get(p.id, 0.0) for p in prospects)
        total_won_revenue = sum(revenue_map.get(w.id, 0.0) for w in won_clients)
        total_lost_value = sum(revenue_map.get(l.id, 0.0) for l in lost_clients)
        
        # Build response data
        prospects_data = []
        for prospect in prospects:
            expected_close_date = None
            try:
                if prospect.next_follow_up_date:
                    expected_close_date = prospect.next_follow_up_date.strftime('%Y-%m-%d') if hasattr(prospect.next_follow_up_date, 'strftime') else str(prospect.next_follow_up_date)
                elif prospect.created_at:
                    if hasattr(prospect.created_at, 'date'):
                        expected_close_date = prospect.created_at.date().strftime('%Y-%m-%d')
                    else:
                        expected_close_date = str(prospect.created_at)
            except Exception:
                pass
            
            prospects_data.append({
                "client_id": prospect.id,
                "estimated_revenue": revenue_map.get(prospect.id, 0.0),
                "expected_close_date": expected_close_date
            })
        
        won_data = []
        for client in won_clients:
            close_date = None
            try:
                if client.created_at:
                    if hasattr(client.created_at, 'date'):
                        close_date = client.created_at.date().strftime('%Y-%m-%d')
                    else:
                        close_date = str(client.created_at)
            except Exception:
                pass
            
            won_data.append({
                "client_id": client.id,
                "actual_revenue": revenue_map.get(client.id, 0.0),
                "close_date": close_date
            })
        
        lost_data = []
        for client in lost_clients:
            lost_date = None
            try:
                if client.created_at:
                    if hasattr(client.created_at, 'date'):
                        lost_date = client.created_at.date().strftime('%Y-%m-%d')
                    else:
                        lost_date = str(client.created_at)
            except Exception:
                pass
            
            lost_data.append({
                "client_id": client.id,
                "estimated_value": revenue_map.get(client.id, 0.0),
                "lost_date": lost_date
            })
        
        # Cache the results
        set_cache(revenue_cache_key, total_revenue, timedelta(minutes=10))
        
        logger.info(f"[API] Revenue calculated: total=${total_revenue:,.2f}")
        
        return JSONResponse({
            "total_revenue": total_revenue,
            "total_revenue_formatted": f"{total_revenue:,.0f}",
            "total_prospect_revenue": total_prospect_revenue,
            "total_won_revenue": total_won_revenue,
            "total_lost_value": total_lost_value,
            "prospects": prospects_data,
            "won_deals": won_data,
            "lost_deals": lost_data,
            "cached": False
        })
        
    except Exception as e:
        logger.error(f"[API] Error calculating revenue: {e}", exc_info=True)
        return JSONResponse({
            "error": "Failed to calculate revenue",
            "total_revenue": 0.0,
            "total_revenue_formatted": "0"
        }, status_code=500)


# ============================================================================
# Timesheet Routes
# ============================================================================

@app.get("/timesheets", response_class=HTMLResponse)
async def timesheets_list(
    request: Request,
    client_id: Optional[int] = Query(None),
    staff_member: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Display list of timesheet entries."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    # Check permission to view timesheets (own or all)
    if not has_permission(current_user, "view_own_timesheets") and not has_permission(current_user, "view_all_timesheets"):
        raise HTTPException(status_code=403, detail="You don't have permission to view timesheets")
    
    # Parse date filters
    date_from_parsed = None
    date_to_parsed = None
    if date_from:
        try:
            date_from_parsed = datetime.strptime(date_from, "%Y-%m-%d").date()
        except ValueError:
            pass
    if date_to:
        try:
            date_to_parsed = datetime.strptime(date_to, "%Y-%m-%d").date()
        except ValueError:
            pass
    
    # Check if user can view all timesheets
    can_view_all = has_permission(current_user, "view_all_timesheets")
    
        # Get timesheets with permission filtering
    timesheets = []
    try:
        if can_view_all:
            # Can view all - use provided filters
            timesheets = get_timesheets(
                db,
                client_id=client_id,
                staff_member=staff_member,
                date_from=date_from_parsed,
                date_to=date_to_parsed,
                search=search
            )
        else:
            # Can only view own - force staff_member filter
            # FIXED: current_user is a User object, not a dict! Use current_user.name
            timesheets = get_timesheets(
                db,
                client_id=client_id,
                staff_member=current_user.name,  # FIXED BUG: was current_user.get("name")
                date_from=date_from_parsed,
                date_to=date_to_parsed,
                search=search
            )
        logger.info(f"Loaded {len(timesheets)} timesheet entries")
    except SQLAlchemyError as e:
        logger.error(f"Database error loading timesheets: {e}", exc_info=True)
        db.rollback()
        timesheets = []
    except Exception as e:
        logger.error(f"Unexpected error loading timesheets: {e}", exc_info=True)
        timesheets = []
    
    # Get all clients for filter dropdown
    all_clients = []
    try:
        all_clients = db.query(Client).order_by(Client.legal_name).all()
    except Exception as e:
        logger.warning(f"Error loading clients for filter: {e}")
        all_clients = []
    
    # Get summary statistics with error handling
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = date(today.year, today.month, 1)
    
    summary_week = {"total_hours": 0.0, "billable_hours": 0.0}
    summary_month = {"total_hours": 0.0, "billable_hours": 0.0}
    summary_all = {"total_hours": 0.0, "billable_hours": 0.0}
    
    try:
        # FIXED: current_user.name instead of current_user.get("name")
        summary_week = get_timesheet_summary(
            db,
            staff_member=current_user.name,  # FIXED BUG: was current_user.get("name")
            date_from=week_start,
            date_to=today
        )
    except Exception as e:
        logger.warning(f"Error getting week summary: {e}")
    
    try:
        # FIXED: current_user.name instead of current_user.get("name")
        summary_month = get_timesheet_summary(
            db,
            staff_member=current_user.name,  # FIXED BUG: was current_user.get("name")
            date_from=month_start,
            date_to=today
        )
    except Exception as e:
        logger.warning(f"Error getting month summary: {e}")
    
    try:
        summary_all = get_timesheet_summary(
            db,
            client_id=client_id,
            staff_member=staff_member,
            date_from=date_from_parsed,
            date_to=date_to_parsed
        )
    except Exception as e:
        logger.warning(f"Error getting all summary: {e}")
    
    # Render template with error handling
    try:
        return templates.TemplateResponse(
            "timesheets_list.html",
            {
                "request": request,
                "user": current_user,
                "timesheets": timesheets,
                "clients": all_clients,
                "selected_client_id": client_id,
                "selected_staff_member": staff_member,
                "date_from": date_from,
                "date_to": date_to,
                "search": search,
                "summary_week": summary_week,
                "summary_month": summary_month,
                "summary_all": summary_all,
                "today": today
            }
        )
    except Exception as e:
        logger.error(f"Error rendering timesheets list template: {e}", exc_info=True)
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "An error occurred loading the timesheets list. Please try again."
            },
            status_code=500
        )


@app.get("/timesheets/new", response_class=HTMLResponse)
async def timesheet_new_form(
    request: Request,
    client_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Display form to create a new timesheet entry."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    # Check permission to create timesheets
    permission_check = require_permission(current_user, "create_timesheets")
    if permission_check:
        return permission_check
    
    clients = db.query(Client).order_by(Client.legal_name).all()
    
    return templates.TemplateResponse(
        "timesheet_form.html",
        {
            "request": request,
            "user": current_user,
            "timesheet": None,
            "clients": clients,
            "preselected_client_id": client_id,
            "today": date.today()
        }
    )


@app.post("/timesheets/new")
async def timesheet_create(
    request: Request,
    client_id: int = Form(...),
    staff_member: str = Form(...),
    entry_date: str = Form(...),
    start_time: Optional[str] = Form(None),
    end_time: Optional[str] = Form(None),
    hours: Optional[str] = Form(None),
    project_task: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    billable: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Create a new timesheet entry."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    # Check permission to create timesheets
    permission_check = require_permission(current_user, "create_timesheets")
    if permission_check:
        return permission_check
    
    # Parse entry date
    try:
        entry_date_parsed = datetime.strptime(entry_date, "%Y-%m-%d").date()
    except ValueError:
        return RedirectResponse(url="/timesheets/new?error=invalid_date", status_code=303)
    
    # Calculate hours if start/end time provided
    hours_value = 0.0
    if start_time and end_time:
        try:
            start = datetime.strptime(start_time, "%H:%M").time()
            end = datetime.strptime(end_time, "%H:%M").time()
            start_dt = datetime.combine(entry_date_parsed, start)
            end_dt = datetime.combine(entry_date_parsed, end)
            if end_dt < start_dt:
                end_dt += timedelta(days=1)  # Handle overnight
            raw_hours = (end_dt - start_dt).total_seconds() / 3600.0
            # Round up to nearest 15-minute increment (0.25 hours)
            minutes = raw_hours * 60
            rounded_minutes = math.ceil(minutes / 15) * 15
            hours_value = rounded_minutes / 60
        except ValueError:
            pass
    elif hours:
        try:
            hours_value = float(hours)
        except ValueError:
            return RedirectResponse(url="/timesheets/new?error=invalid_hours", status_code=303)
    else:
        return RedirectResponse(url="/timesheets/new?error=hours_required", status_code=303)
    
    if hours_value <= 0:
        return RedirectResponse(url="/timesheets/new?error=hours_must_be_positive", status_code=303)
    
    # Round up to nearest 15-minute increment (0.25 hours)
    minutes = hours_value * 60
    rounded_minutes = math.ceil(minutes / 15) * 15
    hours_value = rounded_minutes / 60
    
    # Verify client exists
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    try:
        timesheet_data = TimesheetCreate(
            client_id=client_id,
            staff_member=staff_member,
            entry_date=entry_date_parsed,
            start_time=start_time,
            end_time=end_time,
            hours=hours_value,
            project_task=project_task,
            description=description,
            billable=billable
        )
        
        create_timesheet(db, timesheet_data)
        return RedirectResponse(url="/timesheets", status_code=303)
    except Exception as e:
        print(f"Error creating timesheet: {e}")
        import traceback
        traceback.print_exc()
        return RedirectResponse(url="/timesheets/new?error=creation_failed", status_code=303)


@app.get("/timesheets/{timesheet_id}/edit", response_class=HTMLResponse)
async def timesheet_edit_form(
    request: Request,
    timesheet_id: int,
    db: Session = Depends(get_db)
):
    """Display form to edit an existing timesheet entry."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    timesheet = get_timesheet(db, timesheet_id)
    if not timesheet:
        raise HTTPException(status_code=404, detail="Timesheet entry not found")
    
    # Check if user can edit
    if not can_edit_timesheet(current_user, timesheet.staff_member):
        raise HTTPException(status_code=403, detail="You don't have permission to edit this timesheet entry")
    
    clients = db.query(Client).order_by(Client.legal_name).all()
    
    return templates.TemplateResponse(
        "timesheet_form.html",
        {
            "request": request,
            "user": current_user,
            "timesheet": timesheet,
            "clients": clients,
            "today": date.today()
        }
    )


@app.post("/timesheets/{timesheet_id}/edit")
async def timesheet_update(
    request: Request,
    timesheet_id: int,
    client_id: int = Form(...),
    staff_member: str = Form(...),
    entry_date: str = Form(...),
    start_time: Optional[str] = Form(None),
    end_time: Optional[str] = Form(None),
    hours: Optional[str] = Form(None),
    project_task: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    billable: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Update an existing timesheet entry."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    timesheet = get_timesheet(db, timesheet_id)
    if not timesheet:
        raise HTTPException(status_code=404, detail="Timesheet entry not found")
    
    # Check if user can edit
    if not can_edit_timesheet(current_user, timesheet.staff_member):
        raise HTTPException(status_code=403, detail="You don't have permission to edit this timesheet entry")
    
    # Parse entry date
    try:
        entry_date_parsed = datetime.strptime(entry_date, "%Y-%m-%d").date()
    except ValueError:
        return RedirectResponse(url=f"/timesheets/{timesheet_id}/edit?error=invalid_date", status_code=303)
    
    # Calculate hours
    hours_value = 0.0
    if start_time and end_time:
        try:
            start = datetime.strptime(start_time, "%H:%M").time()
            end = datetime.strptime(end_time, "%H:%M").time()
            start_dt = datetime.combine(entry_date_parsed, start)
            end_dt = datetime.combine(entry_date_parsed, end)
            if end_dt < start_dt:
                end_dt += timedelta(days=1)
            raw_hours = (end_dt - start_dt).total_seconds() / 3600.0
            # Round up to nearest 15-minute increment (0.25 hours)
            minutes = raw_hours * 60
            rounded_minutes = math.ceil(minutes / 15) * 15
            hours_value = rounded_minutes / 60
        except ValueError:
            pass
    elif hours:
        try:
            hours_value = float(hours)
        except ValueError:
            return RedirectResponse(url=f"/timesheets/{timesheet_id}/edit?error=invalid_hours", status_code=303)
    else:
        return RedirectResponse(url=f"/timesheets/{timesheet_id}/edit?error=hours_required", status_code=303)
    
    if hours_value <= 0:
        return RedirectResponse(url=f"/timesheets/{timesheet_id}/edit?error=hours_must_be_positive", status_code=303)
    
    # Round up to nearest 15-minute increment (0.25 hours)
    minutes = hours_value * 60
    rounded_minutes = math.ceil(minutes / 15) * 15
    hours_value = rounded_minutes / 60
    
    # Verify client exists
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    try:
        timesheet_update_data = TimesheetUpdate(
            client_id=client_id,
            staff_member=staff_member,
            entry_date=entry_date_parsed,
            start_time=start_time,
            end_time=end_time,
            hours=hours_value,
            project_task=project_task,
            description=description,
            billable=billable
        )
        
        updated = update_timesheet(db, timesheet_id, timesheet_update_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Timesheet entry not found")
        
        return RedirectResponse(url="/timesheets", status_code=303)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating timesheet: {e}")
        import traceback
        traceback.print_exc()
        return RedirectResponse(url=f"/timesheets/{timesheet_id}/edit?error=update_failed", status_code=303)


@app.post("/timesheets/{timesheet_id}/delete")
async def timesheet_delete(
    request: Request,
    timesheet_id: int,
    db: Session = Depends(get_db)
):
    """Delete a timesheet entry."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    timesheet = get_timesheet(db, timesheet_id)
    if not timesheet:
        raise HTTPException(status_code=404, detail="Timesheet entry not found")
    
    # Check if user can delete
    if not can_delete_timesheet(current_user, timesheet.staff_member):
        raise HTTPException(status_code=403, detail="You don't have permission to delete this timesheet entry")
    
    delete_timesheet(db, timesheet_id)
    return RedirectResponse(url="/timesheets", status_code=303)


# ============================================================================
# Settings/User Management Routes
# ============================================================================

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """Display settings page with user management."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "view_settings")
    if permission_check:
        return permission_check
    
    users = get_users(db, active_only=False)
    
    # Get all available permissions
    all_permissions = [
        ("view_dashboard", "View Dashboard"),
        ("view_clients", "View Clients"),
        ("create_clients", "Create Clients"),
        ("edit_clients", "Edit Clients"),
        ("delete_clients", "Delete Clients"),
        ("export_clients", "Export Clients"),
        ("create_contacts", "Create Contacts"),
        ("delete_contacts", "Delete Contacts"),
        ("create_services", "Create Services"),
        ("edit_services", "Edit Services"),
        ("delete_services", "Delete Services"),
        ("create_tasks", "Create Tasks"),
        ("edit_tasks", "Edit Tasks"),
        ("delete_tasks", "Delete Tasks"),
        ("create_notes", "Create Notes"),
        ("delete_notes", "Delete Notes"),
        ("view_own_timesheets", "View Own Timesheets"),
        ("view_all_timesheets", "View All Timesheets"),
        ("create_timesheets", "Create Timesheets"),
        ("edit_own_timesheets", "Edit Own Timesheets"),
        ("edit_all_timesheets", "Edit All Timesheets"),
        ("delete_own_timesheets", "Delete Own Timesheets"),
        ("delete_all_timesheets", "Delete All Timesheets"),
        ("view_settings", "View Settings"),
        ("manage_users", "Manage Users"),
        ("manage_permissions", "Manage Permissions"),
    ]
    
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "user": current_user,
            "users": users,
            "all_permissions": all_permissions
        }
    )


@app.get("/settings/users/new")
async def create_user_page(request: Request):
    """Redirect to settings page - user creation is done via modal."""
    return RedirectResponse(url="/settings", status_code=303)


@app.post("/settings/users/new")
async def create_user_route(
    request: Request,
    email: str = Form(...),
    name: str = Form(...),
    password: str = Form(...),
    role: str = Form("Staff"),
    db: Session = Depends(get_db)
):
    """Create a new user."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "manage_users")
    if permission_check:
        return permission_check
    
    # Check if email already exists
    existing = get_user_by_email(db, email)
    if existing:
        return RedirectResponse(url="/settings?error=email_exists", status_code=303)
    
    # Get permissions from form (all checkboxes)
    # Need to await request.form() in FastAPI
    form_data = await request.form()
    permissions = {}
    for perm_key, _ in [
        ("view_dashboard", "View Dashboard"),
        ("view_clients", "View Clients"),
        ("create_clients", "Create Clients"),
        ("edit_clients", "Edit Clients"),
        ("delete_clients", "Delete Clients"),
        ("export_clients", "Export Clients"),
        ("create_contacts", "Create Contacts"),
        ("delete_contacts", "Delete Contacts"),
        ("create_services", "Create Services"),
        ("edit_services", "Edit Services"),
        ("delete_services", "Delete Services"),
        ("create_tasks", "Create Tasks"),
        ("edit_tasks", "Edit Tasks"),
        ("delete_tasks", "Delete Tasks"),
        ("create_notes", "Create Notes"),
        ("delete_notes", "Delete Notes"),
        ("view_own_timesheets", "View Own Timesheets"),
        ("view_all_timesheets", "View All Timesheets"),
        ("create_timesheets", "Create Timesheets"),
        ("edit_own_timesheets", "Edit Own Timesheets"),
        ("edit_all_timesheets", "Edit All Timesheets"),
        ("delete_own_timesheets", "Delete Own Timesheets"),
        ("delete_all_timesheets", "Delete All Timesheets"),
        ("view_settings", "View Settings"),
        ("manage_users", "Manage Users"),
        ("manage_permissions", "Manage Permissions"),
    ]:
        permissions[perm_key] = form_data.get(f"perm_{perm_key}") == "on"
    
    # Merge with defaults
    defaults = get_default_permissions(role)
    for key, value in defaults.items():
        if key not in permissions:
            permissions[key] = value
    
    try:
        user_data = UserCreate(
            email=email,
            name=name,
            password=password,
            role=role,
            permissions=permissions
        )
        
        create_user(db, user_data)
        return RedirectResponse(url="/settings?success=user_created", status_code=303)
    except Exception as e:
        import traceback
        print(f"Error creating user: {e}")
        traceback.print_exc()
        error_msg = str(e)
        # Make error message user-friendly
        if "UNIQUE constraint" in error_msg or "unique constraint" in error_msg:
            return RedirectResponse(url="/settings?error=email_exists", status_code=303)
        elif "password" in error_msg.lower():
            return RedirectResponse(url="/settings?error=password_error", status_code=303)
        else:
            return RedirectResponse(url=f"/settings?error=creation_failed&details={error_msg[:50]}", status_code=303)


@app.post("/settings/users/{user_id}/edit")
async def update_user_route(
    request: Request,
    user_id: int,
    name: str = Form(...),
    role: str = Form(...),
    password: Optional[str] = Form(None),
    active: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Update an existing user."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "manage_users")
    if permission_check:
        return permission_check
    
    # Get permissions from form
    # Need to await request.form() in FastAPI
    form_data = await request.form()
    permissions = {}
    for perm_key, _ in [
        ("view_dashboard", "View Dashboard"),
        ("view_clients", "View Clients"),
        ("create_clients", "Create Clients"),
        ("edit_clients", "Edit Clients"),
        ("delete_clients", "Delete Clients"),
        ("export_clients", "Export Clients"),
        ("create_contacts", "Create Contacts"),
        ("delete_contacts", "Delete Contacts"),
        ("create_services", "Create Services"),
        ("edit_services", "Edit Services"),
        ("delete_services", "Delete Services"),
        ("create_tasks", "Create Tasks"),
        ("edit_tasks", "Edit Tasks"),
        ("delete_tasks", "Delete Tasks"),
        ("create_notes", "Create Notes"),
        ("delete_notes", "Delete Notes"),
        ("view_own_timesheets", "View Own Timesheets"),
        ("view_all_timesheets", "View All Timesheets"),
        ("create_timesheets", "Create Timesheets"),
        ("edit_own_timesheets", "Edit Own Timesheets"),
        ("edit_all_timesheets", "Edit All Timesheets"),
        ("delete_own_timesheets", "Delete Own Timesheets"),
        ("delete_all_timesheets", "Delete All Timesheets"),
        ("view_settings", "View Settings"),
        ("manage_users", "Manage Users"),
        ("manage_permissions", "Manage Permissions"),
    ]:
        permissions[perm_key] = form_data.get(f"perm_{perm_key}") == "on"
    
    # Admins always get all permissions
    if role == "Admin":
        permissions = get_default_permissions("Admin")
    
    user_update = UserUpdate(
        name=name,
        role=role,
        password=password if password else None,
        permissions=permissions,
        active=active
    )
    
    update_user(db, user_id, user_update)
    return RedirectResponse(url="/settings?success=user_updated", status_code=303)


@app.post("/settings/users/{user_id}/delete")
async def delete_user_route(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete (deactivate) a user."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    permission_check = require_permission(current_user, "manage_users")
    if permission_check:
        return permission_check
    
    # Prevent deleting yourself
    if current_user.get("id") == user_id:
        return RedirectResponse(url="/settings?error=cannot_delete_self", status_code=303)
    
    delete_user(db, user_id)
    return RedirectResponse(url="/settings?success=user_deleted", status_code=303)


@app.get("/admin/reset-users")
@app.post("/admin/reset-users")
async def reset_admin_users_endpoint(request: Request):
    """
    Emergency endpoint to reset admin users.
    This endpoint can be called without authentication for emergency access.
    Accessible via GET or POST for easy testing.
    In production, you should secure this endpoint or remove it after use.
    """
    try:
        result = reset_admin_users()
        if result.get("status") == "success":
            response_data = {
                "status": "success",
                "message": "Admin users reset successfully",
                "created": result.get("created", 0),
                "updated": result.get("updated", 0),
                "credentials": {
                    "admin@tierneyohlms.com": "ChangeMe123!",
                    "Paul@tierneyohlms.com": "ChangeMe123!",
                    "Dan@tierneyohlms.com": "ChangeMe123!"
                }
            }
            # Return HTML response for easy viewing in browser
            html = f"""
            <!DOCTYPE html>
            <html>
            <head><title>Admin Users Reset</title></head>
            <body style="font-family: Arial; padding: 20px;">
                <h1>Admin Users Reset Successfully!</h1>
                <p><strong>Status:</strong> {response_data['status']}</p>
                <p><strong>Created:</strong> {response_data['created']} users</p>
                <p><strong>Updated:</strong> {response_data['updated']} users</p>
                <h2>Login Credentials:</h2>
                <ul>
                    <li><strong>admin@tierneyohlms.com</strong> / ChangeMe123!</li>
                    <li><strong>Paul@tierneyohlms.com</strong> / ChangeMe123!</li>
                    <li><strong>Dan@tierneyohlms.com</strong> / ChangeMe123!</li>
                </ul>
                <p><a href="/login">Go to Login Page</a></p>
            </body>
            </html>
            """
            return HTMLResponse(content=html)
        else:
            error_msg = result.get("message", "Unknown error")
            html = f"""
            <!DOCTYPE html>
            <html>
            <head><title>Reset Error</title></head>
            <body style="font-family: Arial; padding: 20px;">
                <h1>Error Resetting Users</h1>
                <p><strong>Error:</strong> {error_msg}</p>
                <p><a href="/login">Go to Login Page</a></p>
            </body>
            </html>
            """
            return HTMLResponse(content=html, status_code=500)
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[ERROR] Reset endpoint error: {error_trace}")
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Reset Error</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1>Error Resetting Users</h1>
            <p><strong>Exception:</strong> {str(e)}</p>
            <pre style="background: #f0f0f0; padding: 10px; overflow: auto;">{error_trace}</pre>
            <p><a href="/login">Go to Login Page</a></p>
        </body>
        </html>
        """
        return HTMLResponse(content=html, status_code=500)


# ============================================================================
# Export Routes
# ============================================================================

@app.get("/clients/export")
async def clients_export(
    request: Request,
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    follow_up: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Export filtered client list to CSV."""
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    clients = get_clients(
        db,
        search=search,
        status_filter=status,
        entity_type_filter=entity_type,
        follow_up_filter=follow_up
    )
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "Legal Name",
        "Entity Type",
        "Fiscal Year End",
        "Status",
        "Next Follow-Up Date",
        "Annual Revenue",
        "Created At"
    ])
    
    # Write data
    for client in clients:
        # Note: Export is synchronous, so use inline calculation
        try:
            services = db.query(Service).filter(
                Service.client_id == client.id,
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
                        revenue += service.monthly_fee * 12
        except Exception:
            revenue = 0.0
        writer.writerow([
            client.legal_name,
            client.entity_type or "",
            client.fiscal_year_end or "",
            client.status,
            client.next_follow_up_date.strftime("%Y-%m-%d") if client.next_follow_up_date else "",
            f"{revenue:.2f}",
            client.created_at.strftime("%Y-%m-%d") if client.created_at else ""
        ])
    
    # Return CSV file
    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="clients_export_{datetime.now().strftime("%Y%m%d")}.csv"'
        }
    )

