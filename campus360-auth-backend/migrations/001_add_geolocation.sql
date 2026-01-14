-- Migration: Add Location table and update AccessLog for geolocation features
-- Date: 2026-01-13

-- Create Location table
CREATE TABLE IF NOT EXISTS locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_code VARCHAR(255) UNIQUE NOT NULL,
    location_name VARCHAR(255),
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    class_start TIMESTAMP NOT NULL,
    class_end TIMESTAMP NOT NULL,
    grace_period INTEGER DEFAULT 15 NOT NULL,
    created_by UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
);

-- Add new columns to access_logs table
ALTER TABLE access_logs 
ADD COLUMN IF NOT EXISTS location_id UUID,
ADD COLUMN IF NOT EXISTS status VARCHAR(50),
ADD COLUMN IF NOT EXISTS user_latitude DOUBLE PRECISION,
ADD COLUMN IF NOT EXISTS user_longitude DOUBLE PRECISION,
ADD COLUMN IF NOT EXISTS distance_meters DOUBLE PRECISION;

-- Add foreign key constraint for location_id
ALTER TABLE access_logs
ADD CONSTRAINT fk_access_logs_location
FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE SET NULL;

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_locations_code ON locations(location_code);
CREATE INDEX IF NOT EXISTS idx_locations_created_by ON locations(created_by);
CREATE INDEX IF NOT EXISTS idx_access_logs_location_id ON access_logs(location_id);
CREATE INDEX IF NOT EXISTS idx_access_logs_status ON access_logs(status);
CREATE INDEX IF NOT EXISTS idx_access_logs_timestamp ON access_logs(timestamp);
