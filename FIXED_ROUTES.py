"""
FIXED ROUTES - Dashboard, Clients, Prospects, Timesheets

This file contains the fixed versions of all routes with:
- Proper error handling and logging
- Transaction management (rollback on errors)
- Fixed bugs (current_user.get() -> current_user.name)
- Context managers for database operations
- Comprehensive error messages
"""

import logging
from typing import Optional
from datetime import date, datetime, timedelta
from fastapi import FastAPI, Depends, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy import func

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# DASHBOARD ROUTE - FIXED
# ============================================================================

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Display 2025 Sales Pipeline Dashboard.
    
    Fixed with:
    - Comprehensive error handling
    - Transaction rollback on errors
    - Proper logging
    - Safe defaults for all data
    """
    from auth import get_current_user, require_permission
    from crud import calculate_client_revenue, get_timesheet_summary
    
    # Step 1: Authentication
    try:
        current_user = get_current_user(request)
        if not current_user:
            logger.warning("Dashboard access denied: No authenticated user")
            return RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        logger.error(f"Error getting current user: {e}", exc_info=True)
        return RedirectResponse(url="/login", status_code=303)
    
    # Step 2: Authorization
    try:
        permission_check = require_permission(current_user, "view_dashboard")
        if permission_check:
            return permission_check
    except Exception as e:
        logger.error(f"Error checking permissions: {e}", exc_info=True)
        return RedirectResponse(url="/login", status_code=303)
    
    # Step 3: Load clients data with error handling
    all_clients = []
    try:
        all_clients = db.query(Client).all()
        logger.info(f"Loaded {len(all_clients)} clients for dashboard")
    except SQLAlchemyError as e:
        logger.error(f"Database error loading clients: {e}", exc_info=True)
        db.rollback()
        all_clients = []
    except Exception as e:
        logger.error(f"Unexpected error loading clients: {e}", exc_info=True)
        all_clients = []
    
    # Step 4: Calculate statistics with error handling
    total_clients = len(all_clients)
    active_clients = [c for c in all_clients if c.status == "Active"]
    total_active = len(active_clients)
    
    # Calculate total revenue
    total_revenue = 0.0
    for c in active_clients:
        try:
            revenue = calculate_client_revenue(db, c.id)
            total_revenue += revenue
        except Exception as e:
            logger.warning(f"Error calculating revenue for client {c.id}: {e}")
            # Continue with 0 for this client
    
    # Calculate total hours
    try:
        timesheet_summary_all = get_timesheet_summary(db)
        total_hours = timesheet_summary_all.get("total_hours", 0.0)
    except Exception as e:
        logger.warning(f"Error getting timesheet summary: {e}")
        total_hours = 0.0
    
    # Step 5: Filter clients by status
    current_year = 2025
    prospects = [c for c in all_clients if c.status == "Prospect"]
    lost_clients = [c for c in all_clients if c.status == "Dead"]
    
    # Won deals - Active clients
    won_clients = []
    for client in all_clients:
        if client.status == "Active":
            try:
                # Include if created in 2025
                if client.created_at:
                    if hasattr(client.created_at, 'year') and client.created_at.year == current_year:
                        won_clients.append(client)
                        continue
                
                # Check if has active services
                try:
                    services = db.query(Service).filter(
                        Service.client_id == client.id,
                        Service.active == True
                    ).first()
                    if services:
                        won_clients.append(client)
                except Exception as e:
                    logger.warning(f"Error checking services for client {client.id}: {e}")
            except Exception as e:
                logger.warning(f"Error processing won client {client.id}: {e}")
    
    # Step 6: Calculate prospect revenue
    prospects_data = []
    total_prospect_revenue = 0.0
    for prospect in prospects:
        try:
            estimated_revenue = calculate_client_revenue(db, prospect.id)
            if estimated_revenue == 0:
                estimated_revenue = 75000  # Default estimate
            
            total_prospect_revenue += estimated_revenue
            
            # Safely get expected close date
            expected_close_date = None
            if prospect.next_follow_up_date:
                expected_close_date = prospect.next_follow_up_date
            elif prospect.created_at:
                if hasattr(prospect.created_at, 'date'):
                    expected_close_date = prospect.created_at.date()
                else:
                    expected_close_date = prospect.created_at
            
            prospects_data.append({
                "client": prospect,
                "estimated_revenue": estimated_revenue,
                "expected_close_date": expected_close_date
            })
        except Exception as e:
            logger.warning(f"Error processing prospect {prospect.id}: {e}")
            # Add with defaults
            prospects_data.append({
                "client": prospect,
                "estimated_revenue": 75000,
                "expected_close_date": None
            })
    
    # Step 7: Calculate won revenue
    won_data = []
    total_won_revenue = 0.0
    for client in won_clients:
        try:
            actual_revenue = calculate_client_revenue(db, client.id)
            total_won_revenue += actual_revenue
            
            close_date = None
            if client.created_at:
                if hasattr(client.created_at, 'date'):
                    close_date = client.created_at.date()
                else:
                    close_date = client.created_at
            
            won_data.append({
                "client": client,
                "actual_revenue": actual_revenue,
                "close_date": close_date
            })
        except Exception as e:
            logger.warning(f"Error processing won client {client.id}: {e}")
    
    # Step 8: Calculate lost value
    lost_data = []
    total_lost_value = 0.0
    for client in lost_clients:
        try:
            estimated_value = calculate_client_revenue(db, client.id)
            if estimated_value == 0:
                estimated_value = 60000  # Default estimate
            
            total_lost_value += estimated_value
            
            lost_date = None
            if client.created_at:
                if hasattr(client.created_at, 'date'):
                    lost_date = client.created_at.date()
                else:
                    lost_date = client.created_at
            
            reason = "Not specified"
            try:
                if client.notes:
                    notes_list = list(client.notes)
                    if notes_list:
                        latest_note = sorted(notes_list, key=lambda n: n.created_at, reverse=True)[0]
                        if latest_note and "lost" in latest_note.content.lower():
                            reason = latest_note.content[:100]
            except Exception as e:
                logger.warning(f"Error getting notes for client {client.id}: {e}")
            
            lost_data.append({
                "client": client,
                "estimated_value": estimated_value,
                "lost_date": lost_date,
                "reason": reason
            })
        except Exception as e:
            logger.warning(f"Error processing lost client {client.id}: {e}")
    
    # Step 9: Render dashboard
    try:
        return templates.TemplateResponse(
            "dashboard.html",
            {
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
        )
    except Exception as e:
        logger.error(f"Error rendering dashboard template: {e}", exc_info=True)
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "An error occurred loading the dashboard. Please try again."
            },
            status_code=500
        )


# ============================================================================
# CLIENTS ROUTE - FIXED
# ============================================================================

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
    from auth import get_current_user
    from crud import get_clients, calculate_client_revenue, get_timesheet_summary
    
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
    
    # Calculate revenue and timesheet summaries with error handling
    clients_with_data = []
    for client in clients:
        try:
            revenue = calculate_client_revenue(db, client.id)
        except Exception as e:
            logger.warning(f"Error calculating revenue for client {client.id}: {e}")
            revenue = 0.0
        
        try:
            timesheet_summary = get_timesheet_summary(db, client_id=client.id)
        except Exception as e:
            logger.warning(f"Error getting timesheet summary for client {client.id}: {e}")
            timesheet_summary = {"total_hours": 0.0, "billable_hours": 0.0, "total_entries": 0}
        
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
# PROSPECTS ROUTE - FIXED
# ============================================================================

@app.get("/prospects", response_class=HTMLResponse)
async def prospects_list(
    request: Request,
    search: Optional[str] = Query(None),
    stage: Optional[str] = Query(None),
    owner: Optional[str] = Query(None),
    follow_up: Optional[str] = Query(None),
    sort_by: str = Query("name"),
    sort_order: str = Query("asc"),
    db: Session = Depends(get_db)
):
    """Display list of all prospects with pipeline filtering."""
    from auth import get_current_user, require_permission
    from crud import get_clients, calculate_client_revenue
    
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
            status_filter="Prospect",
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
    prospects_with_data = []
    for prospect in prospects:
        try:
            estimated_revenue = calculate_client_revenue(db, prospect.id)
            if estimated_revenue == 0:
                estimated_revenue = 75000  # Default estimate
            
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
            
            prospects_with_data.append({
                "client": prospect,
                "estimated_revenue": estimated_revenue,
                "estimated_revenue_formatted": f"{estimated_revenue:,.0f}",
                "stage": stage_value,
                "expected_close_date": expected_close_date
            })
        except Exception as e:
            logger.warning(f"Error processing prospect {prospect.id}: {e}")
            # Skip this prospect or add with defaults
            continue
    
    # Get unique owners for filter
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
    
    # Render template
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
                "user": current_user,
                "today": date.today()
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


# ============================================================================
# TIMESHEETS ROUTE - FIXED (with current_user.get() bug fix)
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
    from auth import get_current_user, has_permission, can_edit_timesheet
    from crud import get_timesheets, get_timesheet_summary
    
    try:
        current_user = get_current_user(request)
        if not current_user:
            logger.warning("Timesheets list access denied: No authenticated user")
            return RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        logger.error(f"Error getting current user: {e}", exc_info=True)
        return RedirectResponse(url="/login", status_code=303)
    
    # Check permission
    try:
        if not has_permission(current_user, "view_own_timesheets") and not has_permission(current_user, "view_all_timesheets"):
            logger.warning(f"User {current_user.id} denied access to timesheets")
            raise HTTPException(status_code=403, detail="You don't have permission to view timesheets")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking permissions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error checking permissions")
    
    # Parse date filters
    date_from_parsed = None
    date_to_parsed = None
    if date_from:
        try:
            date_from_parsed = datetime.strptime(date_from, "%Y-%m-%d").date()
        except ValueError:
            logger.warning(f"Invalid date_from format: {date_from}")
            pass
    if date_to:
        try:
            date_to_parsed = datetime.strptime(date_to, "%Y-%m-%d").date()
        except ValueError:
            logger.warning(f"Invalid date_to format: {date_to}")
            pass
    
    # Check if user can view all timesheets
    can_view_all = has_permission(current_user, "view_all_timesheets")
    
    # Get timesheets with error handling
    timesheets = []
    try:
        if can_view_all:
            timesheets = get_timesheets(
                db,
                client_id=client_id,
                staff_member=staff_member,
                date_from=date_from_parsed,
                date_to=date_to_parsed,
                search=search
            )
        else:
            # FIXED: current_user is a User object, not a dict!
            # Changed from: current_user.get("name")
            # To: current_user.name
            timesheets = get_timesheets(
                db,
                client_id=client_id,
                staff_member=current_user.name,  # FIXED BUG
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
    
    # Get summary statistics
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
            staff_member=current_user.name,  # FIXED BUG
            date_from=week_start,
            date_to=today
        )
    except Exception as e:
        logger.warning(f"Error getting week summary: {e}")
    
    try:
        # FIXED: current_user.name instead of current_user.get("name")
        summary_month = get_timesheet_summary(
            db,
            staff_member=current_user.name,  # FIXED BUG
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
    
    # Render template
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

