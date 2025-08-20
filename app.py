import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Run this once at the start of your app.py
def create_tables():
    conn = sqlite3.connect("food_wastage.db")
    cur = conn.cursor()

    # Providers table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Providers (
        Provider_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Type TEXT,
        Address TEXT,
        City TEXT,
        Contact TEXT
    )
    """)

    # Receivers table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Receivers (
        Receiver_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Type TEXT,
        City TEXT,
        Contact TEXT
    )
    """)

    conn.commit()
    conn.close()

create_tables()

# -------------------------------------------------------
# Database Utility Functions
# -------------------------------------------------------
@st.cache_data
def load_data():
    conn = sqlite3.connect("food_wastage.db")

    providers = pd.read_sql_query("SELECT * FROM Providers;", conn)
    receivers = pd.read_sql_query("SELECT * FROM Receivers;", conn)
    food_listings = pd.read_sql_query("SELECT * FROM Food_Listings;", conn)
    claims = pd.read_sql_query("SELECT * FROM Claims;", conn) 
    
    conn.close()
    return providers, receivers, food_listings,claims

def run_query(query, params=()):
    conn = sqlite3.connect("food_wastage.db")
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------
providers, receivers, food_listings,claims = load_data()

# Handle missing City column gracefully
if "City" not in providers.columns:
    providers["City"] = "Unknown"
if "City" not in receivers.columns:
    receivers["City"] = "Unknown"
if "City" not in food_listings.columns:
    food_listings["City"] = "Unknown"

# -------------------------------------------------------
# Streamlit Page Config
# -------------------------------------------------------
st.set_page_config(
    page_title="🍽️ Food Wastage Dashboard",
    page_icon="🥗",
    layout="wide"
)

st.title("🍽️ Food Wastage & Donation Analysis Dashboard")
st.markdown("Gain insights into **providers, receivers, and food donation trends** across cities.")

# -------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------
menu = st.sidebar.radio(
    "📍 Navigate",
    ["Overview", "Providers", "Receivers", "Food Insights", "Map View",
     "Manage Providers", "Manage Receivers","Manage Claims","Manage Food Listings"]
)

# -------------------------------------------------------
# Overview Page
# -------------------------------------------------------
if menu == "Overview":
    st.subheader("📊 Project Overview")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Providers", len(providers))
    col2.metric("Total Receivers", len(receivers))
    col3.metric("Food Listings", len(food_listings))

    st.markdown("---")

    prov_city = providers["City"].value_counts().reset_index()
    prov_city.columns = ["City", "Providers"]

    fig1 = px.bar(prov_city.head(15), x="City", y="Providers", color="Providers",
                  title="Top 15 Cities with Most Providers")
    st.plotly_chart(fig1, use_container_width=True)


# -------------------------------------------------------
# Providers Page
# -------------------------------------------------------
elif menu == "Providers":
    st.subheader("🏙️ Providers Analysis")

    if providers.empty:
        st.warning("⚠️ No provider data available.")
    else:
        selected_city = st.selectbox("Select a City", options=providers["City"].unique())
        filtered = providers[providers["City"] == selected_city]
        st.write(f"### Providers in {selected_city}", filtered)

        prov_city = providers["City"].value_counts().reset_index()
        prov_city.columns = ["City", "Providers"]

        fig = px.bar(prov_city, x="City", y="Providers", color="Providers",
                     title="Providers by City")
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------
# Receivers Page
# -------------------------------------------------------
elif menu == "Receivers":
    st.subheader("👥 Receivers Analysis")

    if receivers.empty:
        st.warning("⚠️ No receiver data available.")
    else:
        selected_city = st.selectbox("Select a City", options=receivers["City"].unique())
        filtered = receivers[receivers["City"] == selected_city]
        st.write(f"### Receivers in {selected_city}", filtered)

        recv_city = receivers["City"].value_counts().reset_index()
        recv_city.columns = ["City", "Receivers"]

        fig = px.bar(recv_city, x="City", y="Receivers", color="Receivers",
                     title="Receivers by City")
        st.plotly_chart(fig, use_container_width=True)


# -------------------------------------------------------
# Food Insights Page with Filters (Final)
# -------------------------------------------------------
elif menu == "Food Insights":
    st.subheader("📊 Food Insights Dashboard")

    # basic empty guard
    if food_listings.empty or providers.empty or receivers.empty or claims.empty:
        st.warning("⚠️ One or more datasets are empty. Please add data first.")
    else:
        # -------------------- Filters --------------------
        st.subheader("🔎 Filter Options")

        # 🔹 City filter
        city_sources = []
        if "City" in food_listings.columns:
            city_sources.extend(food_listings["City"].dropna().unique().tolist())
        if "City" in providers.columns:
            city_sources.extend(providers["City"].dropna().unique().tolist())
        if "City" in receivers.columns:
            city_sources.extend(receivers["City"].dropna().unique().tolist())
        city_options = sorted(set(city_sources)) if city_sources else []
        city_filter = st.selectbox("🏙️ Select City", [""] + city_options)

        # 🔹 Provider filter
        prov_options = providers["Name"].dropna().unique().tolist() if "Name" in providers.columns else []
        prov_filter = st.selectbox("🏢 Select Provider", [""] + prov_options)

        # 🔹 Food type filter
        food_options = food_listings["Food_Type"].dropna().unique().tolist() if "Food_Type" in food_listings.columns else []
        food_filter = st.selectbox("🥗 Select Food Type", [""] + food_options)

        # 🔹 Meal type filter
        meal_options = food_listings["Meal_Type"].dropna().unique().tolist() if "Meal_Type" in food_listings.columns else []
        meal_filter = st.selectbox("🍽️ Select Meal Type", [""] + meal_options)

        # -------------------- Apply Filters --------------------
        filtered_listings = food_listings.copy()

        # City filter
        if city_filter != "":
            prov_in_city = providers[providers["City"] == city_filter]["Provider_ID"].tolist() if "City" in providers.columns else []
            recv_in_city = receivers[receivers["City"] == city_filter]["Receiver_ID"].tolist() if "City" in receivers.columns else []

            if "Provider_ID" in filtered_listings.columns:
                filtered_listings = filtered_listings[
                    filtered_listings["Provider_ID"].isin(prov_in_city) |
                    (filtered_listings["Receiver_ID"].isin(recv_in_city) if "Receiver_ID" in filtered_listings.columns else False)
                ]

        # Provider filter
        if prov_filter != "" and "Provider_ID" in filtered_listings.columns:
            prov_id = providers.loc[providers["Name"] == prov_filter, "Provider_ID"].values
            if len(prov_id) > 0:
                filtered_listings = filtered_listings[filtered_listings["Provider_ID"] == prov_id[0]]

        # Food type filter
        if food_filter != "" and "Food_Type" in filtered_listings.columns:
            filtered_listings = filtered_listings[filtered_listings["Food_Type"] == food_filter]

        # Meal type filter
        if meal_filter != "" and "Meal_Type" in filtered_listings.columns:
            filtered_listings = filtered_listings[filtered_listings["Meal_Type"] == meal_filter]

        # -------------------- KPIs --------------------
        c1, c2, c3 = st.columns(3)

        # Providers count
        unique_providers = filtered_listings["Provider_ID"].nunique() if "Provider_ID" in filtered_listings.columns else providers.shape[0]
        c1.metric("🏢 Providers", unique_providers)

        # Receivers count
        unique_receivers = filtered_listings["Receiver_ID"].nunique() if "Receiver_ID" in filtered_listings.columns else (receivers.shape[0] if not receivers.empty else 0)
        c2.metric("🤝 Receivers", unique_receivers)

        # Food Listings count
        c3.metric("🍱 Food Listings", filtered_listings.shape[0])

        # -------------------- Charts & Insights --------------------
        city_col = "City" if "City" in filtered_listings.columns else None

        # 1) Food Type Distribution
        if "Food_Type" in filtered_listings.columns and not filtered_listings.empty:
            ft = filtered_listings["Food_Type"].value_counts().reset_index()
            ft.columns = ["Food_Type", "Count"]
            st.subheader("🥗 Food Type Distribution")
            st.plotly_chart(px.pie(ft, names="Food_Type", values="Count", hole=0.4), use_container_width=True)

        # 2) Availability by City
        if city_col and "Food_Type" in filtered_listings.columns:
            city_food = filtered_listings.groupby([city_col, "Food_Type"]).size().reset_index(name="Count")
            st.subheader("🏙️ Food Type Availability by City")
            st.plotly_chart(px.bar(city_food, x=city_col, y="Count", color="Food_Type", barmode="group"), use_container_width=True)

        # 3) Top Providers by Listings
        if "Provider_ID" in filtered_listings.columns and "Provider_ID" in providers.columns:
            top_prov = filtered_listings.groupby("Provider_ID").size().reset_index(name="Total_Listings") \
                        .merge(providers[["Provider_ID", "Name"]], on="Provider_ID", how="left")
            st.subheader("⭐ Top Providers by Listings")
            st.dataframe(top_prov.sort_values("Total_Listings", ascending=False).head(5), use_container_width=True)

        # 4) Top Receivers by Claims
        if "Receiver_ID" in claims.columns and "Receiver_ID" in receivers.columns:
            filtered_claims = claims.merge(filtered_listings[["Food_ID"]], on="Food_ID", how="inner")
            top_recv = filtered_claims.groupby("Receiver_ID").size().reset_index(name="Total_Claims") \
                        .merge(receivers[["Receiver_ID", "Name"]], on="Receiver_ID", how="left")
            st.subheader("🙌 Top Receivers by Claims")
            st.dataframe(top_recv.sort_values("Total_Claims", ascending=False).head(5), use_container_width=True)

        # 5) Meal Type Popularity
        if "Meal_Type" in filtered_listings.columns and not filtered_listings.empty:
            meal = filtered_listings["Meal_Type"].value_counts().reset_index()
            meal.columns = ["Meal_Type", "Count"]
            st.subheader("🍽️ Meal Type Popularity")
            st.bar_chart(meal.set_index("Meal_Type"))

        # 6) Expired vs Valid Listings
        if "Expiry_Date" in filtered_listings.columns:
            tmp = filtered_listings.copy()
            tmp["Expiry_Date"] = pd.to_datetime(tmp["Expiry_Date"], errors="coerce")
            today = pd.Timestamp.today().normalize()
            tmp["Expiry_Status"] = tmp["Expiry_Date"].apply(lambda d: "Expired" if pd.notna(d) and d < today else "Valid")
            exp_status = tmp["Expiry_Status"].value_counts().reset_index()
            exp_status.columns = ["Status", "Count"]
            st.subheader("⏳ Expired vs Valid Listings")
            st.plotly_chart(px.pie(exp_status, names="Status", values="Count", hole=0.35), use_container_width=True)

        # 7) Donations Over Time
        if "Listing_Date" in filtered_listings.columns:
            don_time = filtered_listings.copy()
            don_time["Listing_Date"] = pd.to_datetime(don_time["Listing_Date"], errors="coerce")
            don_time = don_time.dropna(subset=["Listing_Date"]).groupby("Listing_Date").size().reset_index(name="Count")
            st.subheader("📅 Donations Over Time")
            st.plotly_chart(px.line(don_time, x="Listing_Date", y="Count"), use_container_width=True)

        # 8) Claims Over Time
        if "Claim_Date" in claims.columns:
            clm_time = claims.copy()
            clm_time["Claim_Date"] = pd.to_datetime(clm_time["Claim_Date"], errors="coerce")
            clm_time = clm_time.dropna(subset=["Claim_Date"]).groupby("Claim_Date").size().reset_index(name="Count")
            st.subheader("📅 Claims Over Time")
            st.plotly_chart(px.line(clm_time, x="Claim_Date", y="Count"), use_container_width=True)

        # 9) Most Wasted Food Types
        if "Expiry_Date" in filtered_listings.columns and "Food_Type" in filtered_listings.columns:
            tmp = filtered_listings.copy()
            tmp["Expiry_Date"] = pd.to_datetime(tmp["Expiry_Date"], errors="coerce")
            wasted = tmp[tmp["Expiry_Date"] < today].groupby("Food_Type").size().reset_index(name="Expired_Count")
            if not wasted.empty:
                st.subheader("🚮 Most Wasted Food Types")
                st.bar_chart(wasted.set_index("Food_Type"))

        # 10) Claims by City
        if "Receiver_ID" in claims.columns and "City" in receivers.columns:
            claims_city = claims.merge(receivers[["Receiver_ID", "City"]], on="Receiver_ID", how="left") \
                                .groupby("City").size().reset_index(name="Claims")
            if city_filter != "":
                claims_city = claims_city[claims_city["City"] == city_filter]
            st.subheader("🌍 Claims by City")
            st.bar_chart(claims_city.set_index("City"))

        # 11) Providers Contribution %
        if "Provider_ID" in filtered_listings.columns and "Provider_ID" in providers.columns:
            prov_share = filtered_listings.groupby("Provider_ID").size().reset_index(name="Total_Listings") \
                          .merge(providers[["Provider_ID", "Name"]], on="Provider_ID", how="left")
            prov_share["Share %"] = (prov_share["Total_Listings"] / prov_share["Total_Listings"].sum()) * 100 if prov_share["Total_Listings"].sum() > 0 else 0
            st.subheader("📊 Providers Contribution %")
            st.dataframe(prov_share.sort_values("Share %", ascending=False)[["Name", "Total_Listings", "Share %"]], use_container_width=True)

        # 12) Receivers Contribution %
        if "Receiver_ID" in claims.columns and "Receiver_ID" in receivers.columns:
            recv_share = claims.merge(filtered_listings[["Food_ID"]], on="Food_ID", how="inner") \
                               .groupby("Receiver_ID").size().reset_index(name="Total_Claims") \
                               .merge(receivers[["Receiver_ID", "Name"]], on="Receiver_ID", how="left")
            recv_share["Share %"] = (recv_share["Total_Claims"] / recv_share["Total_Claims"].sum()) * 100 if recv_share["Total_Claims"].sum() > 0 else 0
            st.subheader("📊 Receivers Contribution %")
            st.dataframe(recv_share.sort_values("Share %", ascending=False)[["Name", "Total_Claims", "Share %"]], use_container_width=True)

        # 13) Listings by Provider Type
        if "Provider_Type" in filtered_listings.columns:
            prov_type = filtered_listings.groupby("Provider_Type").size().reset_index(name="Donations")
            st.subheader("🏭 Listings by Provider Type")
            st.bar_chart(prov_type.set_index("Provider_Type"))

        # 14) Quantity by City
        if city_col and "Quantity" in filtered_listings.columns:
            qty_city = filtered_listings.groupby(city_col)["Quantity"].sum().reset_index()
            st.subheader("📦 Total Quantity by City")
            st.plotly_chart(px.bar(qty_city, x=city_col, y="Quantity"), use_container_width=True)

        # 15) Quantity by Food Type
        if "Food_Type" in filtered_listings.columns and "Quantity" in filtered_listings.columns:
            qty_ft = filtered_listings.groupby("Food_Type")["Quantity"].sum().reset_index()
            st.subheader("📦 Total Quantity by Food Type")
            st.plotly_chart(px.bar(qty_ft, x="Food_Type", y="Quantity"), use_container_width=True)

# -------------------------------------------------------
# Manage Providers (CRUD)
# -------------------------------------------------------
elif menu == "Manage Providers":
    st.subheader("📝 Manage Providers (CRUD Operations)")

    choice = st.radio("Choose Operation", ["Add", "View", "Update", "Delete"])

    if choice == "Add":
        with st.form("add_provider"):
            name = st.text_input("Provider Name")
            ptype = st.text_input("Provider Type (e.g., Restaurant, NGO)")
            address = st.text_area("Address")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            submit = st.form_submit_button("Add Provider")

            if submit:
                run_query(
                    "INSERT INTO Providers (Name, Type, Address, City, Contact) VALUES (?, ?, ?, ?, ?)", 
                    (name, ptype, address, city, contact)
                )
                st.success("✅ Provider Added Successfully!")

    elif choice == "View":
        conn = sqlite3.connect("food_wastage.db")
        df = pd.read_sql_query("SELECT * FROM Providers;", conn)
        st.dataframe(df, use_container_width=True)
        conn.close()

    elif choice == "Update":
        provider_id = st.number_input("Enter Provider ID to Update", min_value=1)
        with st.form("update_provider"):
            new_name = st.text_input("New Provider Name")
            new_type = st.text_input("New Type")
            new_address = st.text_area("New Address")
            new_city = st.text_input("New City")
            new_contact = st.text_input("New Contact")
            submit_update = st.form_submit_button("Update")
            if submit_update:
                run_query(
                    "UPDATE Providers SET Name=?, Type=?, Address=?, City=?, Contact=? WHERE Provider_ID=?", 
                    (new_name, new_type, new_address, new_city, new_contact, provider_id)
                )
                st.success(f"✅ Provider {provider_id} Updated Successfully!")

    elif choice == "Delete":
        provider_id = st.number_input("Enter Provider ID to Delete", min_value=1)
        if st.button("Delete Provider"):
            run_query("DELETE FROM Providers WHERE Provider_ID=?", (provider_id,))
            st.success(f"❌ Provider {provider_id} Deleted Successfully!")


# -------------------------------------------------------
# Manage Receivers (CRUD)
# -------------------------------------------------------
elif menu == "Manage Receivers":
    st.subheader("📝 Manage Receivers (CRUD Operations)")

    choice = st.radio("Choose Operation", ["Add", "View", "Update", "Delete"])

    if choice == "Add":
        with st.form("add_receiver"):
            name = st.text_input("Receiver Name")
            rtype = st.text_input("Receiver Type (e.g., Shelter, NGO)")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            submit = st.form_submit_button("Add Receiver")

            if submit:
                run_query(
                    "INSERT INTO Receivers (Name, Type, City, Contact) VALUES (?, ?, ?, ?)", 
                    (name, rtype, city, contact)
                )
                st.success("✅ Receiver Added Successfully!")

    elif choice == "View":
        conn = sqlite3.connect("food_wastage.db")
        df = pd.read_sql_query("SELECT * FROM Receivers;", conn)
        st.dataframe(df, use_container_width=True)
        conn.close()

    elif choice == "Update":
        receiver_id = st.number_input("Enter Receiver ID to Update", min_value=1)
        with st.form("update_receiver"):
            new_name = st.text_input("New Receiver Name")
            new_type = st.text_input("New Type")
            new_city = st.text_input("New City")
            new_contact = st.text_input("New Contact")
            submit_update = st.form_submit_button("Update")
            if submit_update:
                run_query(
                    "UPDATE Receivers SET Name=?, Type=?, City=?, Contact=? WHERE Receiver_ID=?", 
                    (new_name, new_type, new_city, new_contact, receiver_id)
                )
                st.success(f"✅ Receiver {receiver_id} Updated Successfully!")

    elif choice == "Delete":
        receiver_id = st.number_input("Enter Receiver ID to Delete", min_value=1)
        if st.button("Delete Receiver"):
            run_query("DELETE FROM Receivers WHERE Receiver_ID=?", (receiver_id,))
            st.success(f"❌ Receiver {receiver_id} Deleted Successfully!")

# -------------------------------------------------------
# Manage Claims (CRUD) with Auto Food Update
# -------------------------------------------------------
elif menu == "Manage Claims":
    st.subheader("📝 Manage Claims (CRUD Operations)")

    choice = st.radio("Choose Operation", ["Add", "View", "Update", "Delete"])

    # ---------------- Add Claim ----------------
    if choice == "Add":
        conn = sqlite3.connect("food_wastage.db")
        
        # Fetch Receivers
        receivers = pd.read_sql_query("SELECT Receiver_ID, Name, City FROM Receivers", conn)
        receiver_options = {
            f"{row['Name']} ({row['City']})": row['Receiver_ID'] for _, row in receivers.iterrows()
        }

        # Fetch Food
        food_items = pd.read_sql_query("SELECT Food_ID, Food_Type, Quantity FROM Food_Listings", conn)
        food_options = {
            f"{row['Food_Type']} (Available: {row['Quantity']})": row['Food_ID'] for _, row in food_items.iterrows()
        }

        conn.close()

        with st.form("add_claim"):
            food_choice = st.selectbox("Select Food", list(food_options.keys()))
            receiver_choice = st.selectbox("Select Receiver", list(receiver_options.keys()))
            status = st.selectbox("Status", ["Pending", "Approved", "Rejected"])
            submit = st.form_submit_button("Add Claim")

            if submit:
                run_query(
                    "INSERT INTO Claims (Food_ID, Receiver_ID, Status, Timestamp) VALUES (?, ?, ?, datetime('now'))", 
                    (
                        food_options[food_choice], 
                        receiver_options[receiver_choice],  
                        status
                    )
                )
                st.success("✅ Claim Added Successfully!")

    # ---------------- View Claims ----------------
    elif choice == "View":
        conn = sqlite3.connect("food_wastage.db")
        query = """
            SELECT 
                c.Claim_ID,
                r.Name AS Receiver_Name,
                r.City AS Receiver_City,
                f.Food_Type,
                f.Quantity AS Available_Quantity,
                c.Status,
                c.Timestamp
            FROM Claims c
            JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID
            JOIN Food_Listings f ON c.Food_ID = f.Food_ID;
        """
        df = pd.read_sql_query(query, conn)
        st.dataframe(df, use_container_width=True)
        conn.close()

    # ---------------- Update Claim ----------------
    elif choice == "Update":
        claim_id = st.number_input("Enter Claim ID to Update", min_value=1)
        with st.form("update_claim"):
            new_status = st.selectbox("Update Status", ["Pending", "Approved", "Rejected"])
            submit_update = st.form_submit_button("Update Claim")

            if submit_update:
                # Fetch food linked to claim
                conn = sqlite3.connect("food_wastage.db")
                claim = pd.read_sql_query("SELECT * FROM Claims WHERE Claim_ID=?", conn, params=(claim_id,))
                
                if not claim.empty:
                    food_id = claim.at[0, "Food_ID"]
                    current_status = claim.at[0, "Status"]

                    if current_status != "Approved" and new_status == "Approved":
                        # Reduce food stock
                        food = pd.read_sql_query("SELECT Quantity FROM Food_Listings WHERE Food_ID=?", conn, params=(food_id,))
                        if not food.empty:
                            available_qty = food.at[0, "Quantity"]
                            if available_qty > 0:
                                run_query("UPDATE Food_Listings SET Quantity = Quantity - 1 WHERE Food_ID=?", (food_id,))
                            else:
                                st.error("⚠️ Not enough stock to approve this claim!")
                                conn.close()
                                st.stop()

                    run_query("UPDATE Claims SET Status=? WHERE Claim_ID=?", (new_status, claim_id))
                    st.success(f"✅ Claim {claim_id} Updated Successfully!")
                else:
                    st.error("❌ Claim ID not found!")
                conn.close()

    # ---------------- Delete Claim ----------------
    elif choice == "Delete":
        claim_id = st.number_input("Enter Claim ID to Delete", min_value=1)
        if st.button("Delete Claim"):
            run_query("DELETE FROM Claims WHERE Claim_ID=?", (claim_id,))
            st.success(f"❌ Claim {claim_id} Deleted Successfully!")


# -------------------------------------------------------
# Manage Food Listings (CRUD)
# -------------------------------------------------------
elif menu == "Manage Food Listings":
    st.subheader("📝 Manage Food Listings (CRUD Operations)")

    choice = st.radio("Choose Operation", ["Add", "View", "Update", "Delete"])

    if choice == "Add":
        with st.form("add_food"):
            food_name = st.text_input("Food Name")
            quantity = st.number_input("Quantity", min_value=1)
            expiry_date = st.date_input("Expiry Date")
            provider_id = st.number_input("Provider ID", min_value=1)
            provider_type = st.text_input("Provider Type")
            location = st.text_input("Location")
            food_type = st.text_input("Food Type")
            meal_type = st.text_input("Meal Type")
            submit = st.form_submit_button("Add Food")

            if submit:
                run_query("INSERT INTO Food_Listings (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                          (food_name, quantity, str(expiry_date), provider_id, provider_type, location, food_type, meal_type))
                st.success("✅ Food Listing Added Successfully!")

    elif choice == "View":
        conn = sqlite3.connect("food_wastage.db")
        df = pd.read_sql_query("SELECT * FROM Food_Listings;", conn)
        st.dataframe(df, use_container_width=True)
        conn.close()

    elif choice == "Update":
        food_id = st.number_input("Enter Food ID to Update", min_value=1)
        with st.form("update_food"):
            new_quantity = st.number_input("New Quantity", min_value=1)
            new_expiry = st.date_input("New Expiry Date")
            submit_update = st.form_submit_button("Update")
            if submit_update:
                run_query("UPDATE Food_Listings SET Quantity=?, Expiry_Date=? WHERE Food_ID=?",
                          (new_quantity, str(new_expiry), food_id))
                st.success(f"✅ Food Listing {food_id} Updated Successfully!")

    elif choice == "Delete":
        food_id = st.number_input("Enter Food ID to Delete", min_value=1)
        if st.button("Delete Food"):
            run_query("DELETE FROM Food_Listings WHERE Food_ID=?", (food_id,))
            st.success(f"❌ Food Listing {food_id} Deleted Successfully!")
