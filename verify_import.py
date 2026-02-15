import os
import sys
import asyncio

# Mock environment variables for testing imports
os.environ["BOT_TOKEN"] = "123:test"
os.environ["DATABASE_URL"] = "postgresql+asyncpg://user:pass@localhost/db"
os.environ["ADMIN_ID"] = "123"

print("Starting import verification...")

try:
    import config
    print("Config imported.")
    import database
    print("Database imported.")
    import models
    print("Models imported.")
    import keyboards
    print("Keyboards imported.")
    import services
    print("Services imported.")
    import scheduler
    print("Scheduler imported.")
    
    # Check model attributes to ensure fix worked
    if getattr(models.User, "__tablename__", None) == "users":
        print("User model fixed.")
    else:
        print("User model NOT fixed: " + str(getattr(models.User, "__tablename__", "Missing")))
        
    if getattr(models.Listing, "__tablename__", None) == "listings":
        print("Listing model fixed.")
    else:
        print("Listing model NOT fixed: " + str(getattr(models.Listing, "__tablename__", "Missing")))
        
    print("All imports successful.")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
