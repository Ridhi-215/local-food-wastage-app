import sqlite3

DB_NAME = "food_wastage.db"

# -------------------------------
# Providers CRUD
# -------------------------------
def add_provider(name, city, contact):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO Providers (Name, City, Contact) VALUES (?, ?, ?)", (name, city, contact))
    conn.commit()
    conn.close()

def update_provider(provider_id, name, city, contact):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE Providers SET Name=?, City=?, Contact=? WHERE Provider_ID=?", (name, city, contact, provider_id))
    conn.commit()
    conn.close()

def delete_provider(provider_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM Providers WHERE Provider_ID=?", (provider_id,))
    conn.commit()
    conn.close()

# -------------------------------
# Receivers CRUD
# -------------------------------
def add_receiver(name, city, contact):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO Receivers (Name, City, Contact) VALUES (?, ?, ?)", (name, city, contact))
    conn.commit()
    conn.close()

def update_receiver(receiver_id, name, city, contact):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE Receivers SET Name=?, City=?, Contact=? WHERE Receiver_ID=?", (name, city, contact, receiver_id))
    conn.commit()
    conn.close()

def delete_receiver(receiver_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM Receivers WHERE Receiver_ID=?", (receiver_id,))
    conn.commit()
    conn.close()

# -------------------------------
# Food Listings CRUD
# -------------------------------
def add_food(item, food_type, city, expiry_date, provider_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO Food_Listings (Food_Name, Food_Type, City, Expiry_Date, Provider_ID) VALUES (?, ?, ?, ?, ?)", 
              (item, food_type, city, expiry_date, provider_id))
    conn.commit()
    conn.close()

def update_food(food_id, item, food_type, city, expiry_date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE Food_Listings SET Food_Name=?, Food_Type=?, City=?, Expiry_Date=? WHERE Food_ID=?", 
              (item, food_type, city, expiry_date, food_id))
    conn.commit()
    conn.close()

def delete_food(food_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM Food_Listings WHERE Food_ID=?", (food_id,))
    conn.commit()
    conn.close()
