--
-- Select all ingredients for a restaurant
--
SELECT
    ingredient.name AS 'ingredient',
    stock.quantity,
    ingredient.unit
FROM restaurant
JOIN stock ON stock.restaurant_id = restaurant.id
JOIN ingredient ON ingredient.id = stock.ingredient_id
WHERE restaurant.name = 'Faure'
ORDER BY restaurant.name, ingredient.name;