#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initialize/Migrate database for data source priority feature
"""

from database import Database

def init_database():
    """Initialize database with new fields"""
    print("Initializing database...")

    db = Database('AITradeGame.db')
    db.init_db()

    print("✓ Database initialized successfully")

    # Test reading settings
    settings = db.get_settings()
    print("\nCurrent settings:")
    print(f"  Trading Frequency: {settings.get('trading_frequency_minutes')} minutes")
    print(f"  Trading Fee Rate: {settings.get('trading_fee_rate')}")
    print(f"  Data Source Priority: {settings.get('data_source_priority')}")

    return True

if __name__ == "__main__":
    init_database()
