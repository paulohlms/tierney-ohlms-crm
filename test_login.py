"""
Quick test script to check if users exist and can be verified.
Run this to diagnose login issues.
"""
from database import SessionLocal
from models import User
from auth import verify_user, hash_password

db = SessionLocal()

try:
    # Check if users table exists
    user_count = db.query(User).count()
    print(f"Total users in database: {user_count}")
    
    # List all users
    users = db.query(User).all()
    if users:
        print("\nExisting users:")
        for u in users:
            print(f"  - {u.email} ({u.name}) - Role: {u.role} - Active: {u.active}")
    else:
        print("\n❌ No users found in database!")
        print("\nTo fix this, run:")
        print("  python create_admin_users.py")
        print("\nOr restart your server - it should auto-create users on startup.")
    
    # Test login
    print("\nTesting login...")
    test_user = verify_user(db, "Paul@tierneyohlms.com", "ChangeMe123!")
    if test_user:
        print("✅ Login test PASSED for Paul@tierneyohlms.com")
    else:
        print("❌ Login test FAILED for Paul@tierneyohlms.com")
        print("   This could mean:")
        print("   - User doesn't exist (run: python create_admin_users.py)")
        print("   - Password is wrong")
        print("   - Password hash is incorrect")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

