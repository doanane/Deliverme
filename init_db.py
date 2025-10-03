from database import engine, Base
from models import User, Order
import models  # This ensures models are registered


def debug_database():
    print("=== DEBUG DATABASE CREATION ===")

    # Check what tables are registered with Base
    print("\n1. Tables registered with Base:")
    for table_name, table in Base.metadata.tables.items():
        print(f"   - {table_name}")
        for column in table.columns:
            print(f"     - {column.name} ({column.type})")

    # Drop all tables first
    print("\n2. Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("   ✅ Tables dropped")

    # Create all tables
    print("\n3. Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("   ✅ Tables creation command executed")

    # Verify tables exist in database
    print("\n4. Checking tables in PostgreSQL...")
    from sqlalchemy import inspect

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if tables:
        print("   ✅ Tables found in database:")
        for table in tables:
            print(f"     - {table}")
            columns = inspector.get_columns(table)
            for column in columns:
                print(f"       - {column['name']} ({column['type']})")
    else:
        print("   ❌ No tables found in database")


if __name__ == "__main__":
    debug_database()
