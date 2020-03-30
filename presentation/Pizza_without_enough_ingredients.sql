--
-- Select pizza with not enought ingredient in a restaurant
--
SELECT
    restaurant.name AS restaurant_name,
    pizza.name AS pizza_name
FROM restaurant
JOIN stock ON stock.restaurant_id = restaurant.id
JOIN ingredient ON ingredient.id = stock.ingredient_id
JOIN recipe ON recipe.ingredient_id = ingredient.id
JOIN pizza ON pizza.id = recipe.pizza_id
WHERE (stock.quantity - recipe.quantity) <= 0
GROUP BY restaurant.name, pizza.name
ORDER BY restaurant.name, pizza.name;
