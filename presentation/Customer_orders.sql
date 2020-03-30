--
-- Select orders from a customer
--
SELECT
    customer.email,
    customer_order.order_date,
    status.name
FROM customer_order
JOIN customer ON customer.id = customer_order.customer_id
JOIN status ON status.id = customer_order.status_id
WHERE 
    customer_id = 
        (
            SELECT id
            FROM customer
            WHERE email = 'eugene.auger@berthelot.fr'
        );
