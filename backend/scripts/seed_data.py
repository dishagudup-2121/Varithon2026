"""Standalone script to seed the VARI OS database.

Usage: python -m scripts.seed_data
(run from the backend/ directory)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import create_tables, SessionLocal
from app.services.state_service import seed_initial_data


def main():
    print('Creating tables...')
    create_tables()
    
    db = SessionLocal()
    try:
        print('Seeding initial data...')
        seed_initial_data(db)
        print('Done! Database seeded successfully.')
    finally:
        db.close()


if __name__ == '__main__':
    main()
