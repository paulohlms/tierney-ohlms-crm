"""
Emergency script to create admin users.
Run this if bootstrap isn't working.
"""
import os
import sys
from database import get_db, engine, Base
from models import User
from auth import hash_password, get_default_permissions
import json

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def create_admin_users():
    """Create admin users directly."""
    db = next(get_db())
    try:
        # Check existing users
        existing = db.query(User).all()
        print(f"Found {len(existing)} existing users:")
        for u in existing:
            print(f"  - {u.email} (Active: {u.active}, Role: {u.role})")
        
        # Create admin if doesn't exist
        admin = db.query(User).filter(func.lower(User.email) == "admin@tierneyohlms.com").first()
        if not admin:
            print("\nCreating admin@tierneyohlms.com...")
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
            print("✅ Created admin@tierneyohlms.com")
        else:
            print(f"\nadmin@tierneyohlms.com already exists (Active: {admin.active})")
            # Reset password if needed
            admin.hashed_password = hash_password("ChangeMe123!")
            admin.active = True
            print("✅ Reset password for admin@tierneyohlms.com")
        
        # Create Paul if doesn't exist
        paul = db.query(User).filter(func.lower(User.email) == "paul@tierneyohlms.com").first()
        if not paul:
            print("\nCreating Paul@tierneyohlms.com...")
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
            print("✅ Created Paul@tierneyohlms.com")
        else:
            print(f"\nPaul@tierneyohlms.com already exists (Active: {paul.active})")
            paul.hashed_password = hash_password("ChangeMe123!")
            paul.active = True
            print("✅ Reset password for Paul@tierneyohlms.com")
        
        db.commit()
        print("\n✅ All users ready!")
        print("\nLogin credentials:")
        print("  - admin@tierneyohlms.com / ChangeMe123!")
        print("  - Paul@tierneyohlms.com / ChangeMe123!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    from sqlalchemy import func
    create_admin_users()

