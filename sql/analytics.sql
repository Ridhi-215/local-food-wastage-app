-- 1. Number of food providers per city
SELECT City, COUNT(*) AS Total_Providers
FROM Providers
GROUP BY City;

-- 2. Number of receivers per city
SELECT City, COUNT(*) AS Total_Receivers
FROM Receivers
GROUP BY City;

-- 3. Provider type that contributes the most food
SELECT Provider_Type, SUM(Quantity) AS Total_Food
FROM Food_Listings
GROUP BY Provider_Type
ORDER BY Total_Food DESC;

-- 4. Contact information of providers in a specific city (example: Hyderabad)
SELECT Name, Contact
FROM Providers
WHERE City = 'Hyderabad';

-- 5. Receivers who claimed the most food
SELECT r.Name, COUNT(c.Claim_ID) AS Total_Claims
FROM Receivers r
JOIN Claims c ON r.Receiver_ID = c.Receiver_ID
GROUP BY r.Name
ORDER BY Total_Claims DESC;

-- 6. Total quantity of food available
SELECT SUM(Quantity) AS Total_Available_Food
FROM Food_Listings;

-- 7. City with the highest number of food listings
SELECT Location, COUNT(*) AS Listings
FROM Food_Listings
GROUP BY Location
ORDER BY Listings DESC;

-- 8. Most common food types available
SELECT Food_Type, COUNT(*) AS Count_Available
FROM Food_Listings
GROUP BY Food_Type
ORDER BY Count_Available DESC;

-- 9. Number of food claims per food item
SELECT f.Food_Name, COUNT(c.Claim_ID) AS Claims_Made
FROM Claims c
JOIN Food_Listings f ON c.Food_ID = f.Food_ID
GROUP BY f.Food_Name
ORDER BY Claims_Made DESC;

-- 10. Provider with the highest number of successful claims
SELECT p.Name, COUNT(*) AS Successful_Claims
FROM Claims c
JOIN Food_Listings f ON c.Food_ID = f.Food_ID
JOIN Providers p ON f.Provider_ID = p.Provider_ID
WHERE c.Status = 'Completed'
GROUP BY p.Name
ORDER BY Successful_Claims DESC;

-- 11. Percentage of claims by status
SELECT Status, 
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM Claims), 2) AS Percentage
FROM Claims
GROUP BY Status;

-- 12. Average quantity of food claimed per receiver
SELECT r.Name, ROUND(AVG(f.Quantity), 2) AS Avg_Quantity_Claimed
FROM Claims c
JOIN Food_Listings f ON c.Food_ID = f.Food_ID
JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID
GROUP BY r.Name;

-- 13. Most claimed meal type
SELECT f.Meal_Type, COUNT(*) AS Total_Claims
FROM Claims c
JOIN Food_Listings f ON c.Food_ID = f.Food_ID
GROUP BY f.Meal_Type
ORDER BY Total_Claims DESC;

-- 14. Total quantity of food donated by each provider
SELECT p.Name, SUM(f.Quantity) AS Total_Donated
FROM Food_Listings f
JOIN Providers p ON f.Provider_ID = p.Provider_ID
GROUP BY p.Name
ORDER BY Total_Donated DESC;

-- 15. City-wise completed claims
SELECT r.City, COUNT(*) AS Completed_Claims
FROM Claims c
JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID
WHERE c.Status = 'Completed'
GROUP BY r.City
ORDER BY Completed_Claims DESC;
