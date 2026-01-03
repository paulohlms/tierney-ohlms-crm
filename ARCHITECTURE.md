# CRM System Architecture

## Intended System Behavior

1. **Database Layer**
   - SQLAlchemy ORM with declarative models
   - PostgreSQL for production (Render), SQLite for local development
   - Tables created via `Base.metadata.create_all()` on first run
   - Schema defined entirely in `models.py`

2. **Application Layer**
   - FastAPI server-rendered application (HTML responses)
   - Session-based authentication
   - CRUD operations separated into `crud.py`
   - Business logic in route handlers

3. **Startup Sequence**
   - Create tables if they don't exist (`Base.metadata.create_all()`)
   - Migrate schema if needed (add missing columns to existing tables)
   - Bootstrap admin users if none exist

## Broken Assumptions (Current Issues)

1. **Migration Code Complexity**: Trying to ALTER existing tables causes transaction state issues
2. **Connection Pool Contamination**: Migration uses same connection pool as application, causing `InFailedSqlTransaction` errors
3. **Mixed Concerns**: DDL operations mixed with application logic
4. **Error Handling**: Complex retry logic that doesn't solve root cause
5. **Debug Code**: Instrumentation code left in production files

## Corrected Architecture

### Database Initialization
- `Base.metadata.create_all()` creates all tables with correct schema on first run
- For existing databases: Use isolated DDL connection with proper error handling
- Each ALTER TABLE operation is independent and doesn't affect application connections

### Migration Strategy
- Use separate connection for DDL operations (not from session pool)
- Each DDL operation in its own transaction with proper rollback
- Check if column exists before attempting to add it
- Fail gracefully - log warnings but don't crash application

### Transaction Management
- Application queries use normal session pool (autocommit=False)
- DDL operations use isolated connection with explicit transactions
- No mixing of DDL and DML in same transaction

### Error Handling
- Simple, clear error messages
- Log warnings for migration issues
- Application continues even if some migrations fail
- No complex retry logic - fix root cause instead

## Implementation

1. **Clean Migration Function**: Isolated DDL operations with proper error handling
2. **Remove Debug Code**: All instrumentation removed
3. **Simplify Error Handling**: Clear, actionable error messages
4. **Proper Transaction Isolation**: DDL never affects application queries

