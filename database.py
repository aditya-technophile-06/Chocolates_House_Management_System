import sqlite3
from flask import g

DATABASE = 'chocolate_house.db'

# Get database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Close database connection
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create tables in the database
def create_tables():
    db = get_db()
    cursor = db.cursor()

    # Create Seasonal Flavors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seasonal_flavors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flavor_name TEXT NOT NULL,
            availability_start DATE NOT NULL,
            availability_end DATE NOT NULL
        )
    ''')

    # Create Ingredient Inventory table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredient_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient_name TEXT NOT NULL,
            quantity_in_stock INTEGER NOT NULL
        )
    ''')

    # Create Customer Suggestions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            suggested_flavor TEXT NOT NULL,
            allergy_concern TEXT
        )
    ''')

    db.commit()
