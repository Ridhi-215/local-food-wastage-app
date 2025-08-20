import sqlite3
import pandas as pd
import os

# Paths
DB_PATH = os.path.join("food_wastage.db")
DATA_DIR = os.path.join("data")

def init_db():
    conn = sqlite3.connect(DB_PATH)

    # --- Providers ---
    providers = pd.read_csv(os.path.join(DATA_DIR, "providers_data.csv"))
    providers.to_sql("Providers", conn, if_exists="replace", index=False)

    # --- Receivers ---
    receivers = pd.read_csv(os.path.join(DATA_DIR, "receivers_data.csv"))
    receivers.to_sql("Receivers", conn, if_exists="replace", index=False)

    # --- Food Listings ---
    food_listings = pd.read_csv(os.path.join(DATA_DIR, "food_listings_data.csv"))
    food_listings.to_sql("Food_Listings", conn, if_exists="replace", index=False)

    # --- Claims ---
    claims = pd.read_csv(os.path.join(DATA_DIR, "claims_data.csv"))
    claims.to_sql("Claims", conn, if_exists="replace", index=False)

    conn.close()
    print("✅ Database initialized from CSV files!")

if __name__ == "__main__":
    init_db()
