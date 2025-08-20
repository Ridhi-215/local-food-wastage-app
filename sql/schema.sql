PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Providers (
    Provider_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Type TEXT,
    Address TEXT,
    City TEXT,
    Contact TEXT
);

CREATE TABLE IF NOT EXISTS Receivers (
    Receiver_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Type TEXT,
    City TEXT,
    Contact TEXT
);

CREATE TABLE IF NOT EXISTS Food_Listings (
    Food_ID INTEGER PRIMARY KEY,
    Food_Name TEXT,
    Quantity INTEGER,
    Expiry_Date TEXT,  -- YYYY-MM-DD format
    Provider_ID INTEGER,
    Provider_Type TEXT,
    Location TEXT,
    Food_Type TEXT,
    Meal_Type TEXT,
    FOREIGN KEY (Provider_ID) REFERENCES Providers(Provider_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Claims (
    Claim_ID INTEGER PRIMARY KEY,
    Food_ID INTEGER,
    Receiver_ID INTEGER,
    Status TEXT,       -- Pending, Completed, Cancelled
    Timestamp TEXT,    -- YYYY-MM-DD HH:MM:SS
    FOREIGN KEY (Food_ID) REFERENCES Food_Listings(Food_ID) ON DELETE CASCADE,
    FOREIGN KEY (Receiver_ID) REFERENCES Receivers(Receiver_ID) ON DELETE CASCADE
);
