"""
Manual migration script - Fixed data types to match existing schema
"""
import asyncio
from prisma import Prisma

async def apply_migration_step_by_step():
    """Apply migration commands one by one with correct data types"""
    prisma = Prisma()
    await prisma.connect()
    
    commands = [
        # Create locations table with TEXT for created_by to match users.id
        """
        CREATE TABLE IF NOT EXISTS locations (
            id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
            location_code VARCHAR(255) UNIQUE NOT NULL,
            location_name VARCHAR(255),
            latitude DOUBLE PRECISION NOT NULL,
            longitude DOUBLE PRECISION NOT NULL,
            class_start TIMESTAMP NOT NULL,
            class_end TIMESTAMP NOT NULL,
            grace_period INTEGER DEFAULT 15 NOT NULL,
            created_by TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        # Add columns to access_logs
        "ALTER TABLE access_logs ADD COLUMN IF NOT EXISTS location_id TEXT",
        "ALTER TABLE access_logs ADD COLUMN IF NOT EXISTS status VARCHAR(50)",
        "ALTER TABLE access_logs ADD COLUMN IF NOT EXISTS user_latitude DOUBLE PRECISION",
        "ALTER TABLE access_logs ADD COLUMN IF NOT EXISTS user_longitude DOUBLE PRECISION",
        "ALTER TABLE access_logs ADD COLUMN IF NOT EXISTS distance_meters DOUBLE PRECISION",
        # Add foreign key
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.table_constraints 
                WHERE constraint_name = 'fk_access_logs_location'
            ) THEN
                ALTER TABLE access_logs
                ADD CONSTRAINT fk_access_logs_location
                FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE SET NULL;
            END IF;
        END $$
        """,
        # Create indexes
        "CREATE INDEX IF NOT EXISTS idx_locations_code ON locations(location_code)",
        "CREATE INDEX IF NOT EXISTS idx_locations_created_by ON locations(created_by)",
        "CREATE INDEX IF NOT EXISTS idx_access_logs_location_id ON access_logs(location_id)",
        "CREATE INDEX IF NOT EXISTS idx_access_logs_status ON access_logs(status)",
        "CREATE INDEX IF NOT EXISTS idx_access_logs_timestamp ON access_logs(timestamp)",
    ]
    
    try:
        for i, cmd in enumerate(commands, 1):
            print(f"Executing command {i}/{len(commands)}...")
            await prisma.execute_raw(cmd.strip())
            print(f"✅ Command {i} completed")
        
        print("\n✅ All migration commands applied successfully!")
        print("\n📊 Database schema updated with:")
        print("  - locations table (geolocation + time constraints)")
        print("  - access_logs enhancements (status, coordinates, distance)")
        
    except Exception as e:
        print(f"\n❌ Error applying migration: {e}")
    finally:
        await prisma.disconnect()

if __name__ == "__main__":
    asyncio.run(apply_migration_step_by_step())
