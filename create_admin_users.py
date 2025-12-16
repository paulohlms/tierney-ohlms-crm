"""
Manually create admin users in the database.
Run this if bootstrap didn't work or you need to reset users.
"""
from database import SessionLocal
from models import User
from auth import hash_password, get_default_permissions
import json

db = SessionLocal()

try:
    # Check if users already exist
    existing_paul = db.query(User).filter(User.email == "Paul@tierneyohlms.com").first()
    existing_dan = db.query(User).filter(User.email == "Dan@tierneyohlms.com").first()
    
    if existing_paul:
        print("Paul@tierneyohlms.com already exists. Skipping...")
    else:
        print("Creating Paul@tierneyohlms.com...")
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
        print("✅ Paul created!")
    
    if existing_dan:
        print("Dan@tierneyohlms.com already exists. Skipping...")
    else:
        print("Creating Dan@tierneyohlms.com...")
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
        print("✅ Dan created!")
    
    db.commit()
    print("\n✅ Admin users setup complete!")
    print("\nLogin credentials:")
    print("  - Paul@tierneyohlms.com / ChangeMe123!")
    print("  - Dan@tierneyohlms.com / ChangeMe123!")
    print("\n⚠️  CHANGE THESE PASSWORDS IMMEDIATELY after first login!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()

