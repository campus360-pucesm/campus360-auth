#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "🚀 Starting build process..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Generate Prisma client
echo "🔧 Generating Prisma client..."
python -m prisma generate

# Push database schema (creates tables if they don't exist)
echo "🗄️  Pushing database schema..."
python -m prisma db push --skip-generate

echo "✅ Build completed successfully!"
