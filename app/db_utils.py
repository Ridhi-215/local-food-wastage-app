import sqlite3

DB_NAME = "food_wastage.db"

# -----------------------------
# Add Provider
# -----------------------------
def add_provider(name, contact, city):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Providers (Provider_Name, Contact, City)
        VALUES (?, ?, ?)
    """, (name, contact, city))
    conn.commit()
    conn.close()

# -----------------------------
# Add Receiver
# -----------------------------
def add_receiver(name, contact, city):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Receivers (Receiver_Name, Contact, City)
        VALUES (?, ?, ?)
    """, (name, contact, city))
    conn.commit()
    conn.close()

# -----------------------------
# Add Food
# -----------------------------
import sqlite3

def add_food(food_name, food_type, quantity, expiry_date, provider_id, provider_type, location, meal_type):
    conn = sqlite3.connect("food_wastage.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Food_Listings
        (Food_Name, Food_Type, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Meal_Type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (food_name, food_type, quantity, expiry_date, provider_id, provider_type, location, meal_type))
    conn.commit()
    conn.close()
