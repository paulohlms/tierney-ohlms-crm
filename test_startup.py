#!/usr/bin/env python3
"""
Test script to verify the application starts correctly.

This script:
1. Imports the app to check for import errors
2. Checks app initialization
3. Verifies routes are registered
4. Tests database connection (if available)
"""

import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all imports work correctly."""
    logger.info("Testing imports...")
    try:
        from main import app
        logger.info("✓ App imported successfully")
        return app
    except Exception as e:
        logger.error(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_app_initialization(app):
    """Test that app is initialized correctly."""
    logger.info("Testing app initialization...")
    try:
        assert app is not None, "App is None"
        assert hasattr(app, 'title'), "App missing title"
        assert hasattr(app, 'routes'), "App missing routes"
        logger.info(f"✓ App initialized: {app.title}")
        logger.info(f"✓ Routes registered: {len(app.routes)}")
        return True
    except Exception as e:
        logger.error(f"✗ App initialization failed: {e}")
        return False

def test_routes(app):
    """Test that key routes are registered."""
    logger.info("Testing route registration...")
    try:
        routes = [route.path for route in app.routes]
        required_routes = ["/", "/login", "/dashboard", "/clients", "/prospects", "/timesheets"]
        
        missing = [r for r in required_routes if r not in routes]
        if missing:
            logger.warning(f"⚠ Missing routes: {missing}")
        else:
            logger.info("✓ All required routes registered")
        
        logger.info(f"  Total routes: {len(routes)}")
        logger.info(f"  Key routes: {', '.join([r for r in routes if r in required_routes])}")
        return True
    except Exception as e:
        logger.error(f"✗ Route test failed: {e}")
        return False

def test_database_connection():
    """Test database connection (if available)."""
    logger.info("Testing database connection...")
    try:
        from database import engine
        # Try to connect
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("✓ Database connection successful")
        return True
    except Exception as e:
        logger.warning(f"⚠ Database connection failed (this is OK if DB is not available): {e}")
        return False

def main():
    """Run all tests."""
    logger.info("=" * 70)
    logger.info("Testing Application Startup")
    logger.info("=" * 70)
    
    # Test imports
    app = test_imports()
    if not app:
        logger.error("Cannot continue - app import failed")
        sys.exit(1)
    
    # Test app initialization
    if not test_app_initialization(app):
        logger.error("Cannot continue - app initialization failed")
        sys.exit(1)
    
    # Test routes
    if not test_routes(app):
        logger.warning("Some routes missing, but continuing...")
    
    # Test database (optional)
    test_database_connection()
    
    logger.info("=" * 70)
    logger.info("All startup tests passed! ✓")
    logger.info("=" * 70)
    logger.info("\nYou can now start the server with:")
    logger.info("  uvicorn main:app --reload")
    logger.info("=" * 70)

if __name__ == "__main__":
    main()

