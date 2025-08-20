# Local Food Wastage Management System

## Project Overview
Food wastage is a significant issue, with many households and restaurants discarding surplus food while numerous people struggle with food insecurity.  
The **Local Food Wastage Management System** connects food providers to those in need through a structured platform, reducing waste and enhancing food accessibility.

This project uses **Python, SQL, and Streamlit** to build an interactive web application for managing local food donations and claims.

## Features
- Add, update, and remove food listings and claims (**CRUD operations**)
- Filter food donations by **location, provider, food type, and meal type**
- Display contact details of food providers for direct coordination
- Visualize food wastage trends using **15 SQL queries**
- Deployable web app accessible online

## Skills Learned
- Python programming
- SQL database management
- Streamlit app development
- Data analysis and visualization
- Domain knowledge in food management and social good

## Tech Stack
- **Backend & Database:** Python, SQLite  
- **Frontend:** Streamlit  
- **Data Analysis:** SQL queries, Pandas  

## Problem Statement
Many households and restaurants discard surplus food while numerous people face food insecurity. This project aims to create a system where:
- Restaurants and individuals can list surplus food.
- NGOs or individuals in need can claim the food.
- SQL stores available food details and locations.
- A Streamlit app enables interaction, filtering, CRUD operations, and visualization.

## Business Use Cases
- Efficient redistribution of surplus food to those in need  
- Reducing food waste in communities  
- Easy access via location-based filtering  
- Insightful analysis of food wastage patterns for better decision-making  

## Project Approach
1. **Data Preparation:** Clean and standardize datasets.  
2. **Database Creation:** Store food availability data in SQL tables, implement CRUD operations.  
3. **Data Analysis:** Identify trends based on categories, locations, and expiry dates.  
4. **Application Development:** Build a Streamlit interface displaying outputs of 15 SQL queries, filtering options, and provider contact details.  
5. **Deployment:** Host the Streamlit app for real-time access.

## Dataset
- `providers_data.csv` – Details of food providers  
- `receivers_data.csv` – Details of receivers  
- `food_listings_data.csv` – Food items available for claim  
- `claims_data.csv` – Food claims by receivers  

## Key SQL Questions & Analysis
- Count of providers and receivers by city  
- Providers contributing the most food  
- Contact details of providers by city  
- Total quantity of food available  
- Most commonly available food types  
- Food claim statistics and completion rates  
- Average quantity claimed per receiver  
- Most claimed meal type (Breakfast, Lunch, Dinner, Snacks)  

## Results
- Fully functional **Streamlit app** with filtering and CRUD functionality  
- SQL-powered insights into food wastage trends, provider contributions, and high-demand locations  

## Deployment
The app is deployed on Streamlit Cloud and accessible [here](https://local-food-wastage-app.streamlit.app/).  

## How to Run Locally
1. Clone the repository:
```bash
git clone https://github.com/Ridhi-215/local-food-wastage-app.git

Navigate to the project directory:
cd local-food-wastage-app

Install dependencies:
pip install -r requirements.txt

Run the app:
streamlit run app.py
