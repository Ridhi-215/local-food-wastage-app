import sqlite3
import pandas as pd

# Connect to SQLite database (it will be created if not exists)
conn = sqlite3.connect("food_wastage.db")
cursor = conn.cursor()

# Load schema.sql file
with open("sql/schema.sql", "r") as f:
    cursor.executescript(f.read())
print("✅ Tables created successfully.")

# Load CSVs
providers = pd.read_csv("data/providers_data.csv")
receivers = pd.read_csv("data/receivers_data.csv")
food = pd.read_csv("data/food_listings_data.csv")
claims = pd.read_csv("data/claims_data.csv")

# Push into SQL tables
providers.to_sql("Providers", conn, if_exists="append", index=False)
receivers.to_sql("Receivers", conn, if_exists="append", index=False)
food.to_sql("Food_Listings", conn, if_exists="append", index=False)
claims.to_sql("Claims", conn, if_exists="append", index=False)

print("✅ Data loaded successfully into food_wastage.db")

conn.commit()
conn.close()
