--
-- Select the orders from a restaurant where status is 'pending'
--
SELECT
    customer.email,
    customer_order.order_date,
    status.name
FROM customer_order
JOIN customer ON customer.id = customer_order.customer_id
JOIN status ON status.id = customer_order.status_id
JOIN restaurant ON restaurant.id = customer_order.restaurant_id
WHERE
    restaurant.name = 'Faure' AND
    status.name = 'attente';