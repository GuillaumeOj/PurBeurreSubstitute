--
-- Select order's lines from a specific order
--
SELECT
    pizza.name AS pizza,
    size.name AS size,
    (order_line.tax_free_unit_price * order_line.vat_rate_100 + order_line.tax_free_unit_price) AS unit_price,
    order_line.quantity,
    -- order_line.tax_free_unit_price,
    -- order_line.vat_rate_100
    (order_line.quantity * (order_line.tax_free_unit_price * order_line.vat_rate_100 + order_line.tax_free_unit_price)) AS total_price
FROM order_line
JOIN pizza ON pizza.id = order_line.pizza_id
JOIN size ON size.id = order_line.size_id
WHERE
    order_id =
        (
            SELECT id FROM customer_order
            WHERE 
                customer_id = 
                    (
                        SELECT id
                        FROM customer
                        WHERE email = 'eugene.auger@berthelot.fr'
                    )
            LIMIT 1
        );