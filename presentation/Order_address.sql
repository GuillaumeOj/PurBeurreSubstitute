--
-- Select the delivery address for an order even if the customer have change her·his own
--
SELECT
    customer.email,
    CONCAT(
        customer.address_street_number,
        ' ',
        customer.address_street_name,
        ' ',
        customer.address_postal_code,
        ' ',
        customer.address_city) AS customer_current_address,
    customer_order.order_date,
    CONCAT(
        customer_order.address_street_number,
        ' ',
        customer_order.address_street_name,
        ' ',
        customer_order.address_postal_code,
        ' ',
        customer_order.address_city) AS delivery_address,
    status.name
FROM customer_order
JOIN customer ON customer.id = customer_order.customer_id
JOIN status ON status.id = customer_order.status_id
WHERE
    customer.email = 'emmanuelle.gros@arnaud.fr' AND
    customer.address_street_name != customer_order.address_street_name;