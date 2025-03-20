WITH order_income AS (
    SELECT 
        oo.order_id,
        strftime('%m', oo.order_delivered_customer_date) AS month_no,
        strftime('%Y', oo.order_delivered_customer_date) AS year,
        oop.payment_value
    FROM olist_orders oo
    JOIN olist_order_payments oop 
        ON oo.order_id = oop.order_id
    WHERE oo.order_delivered_customer_date IS NOT NULL
      AND oo.order_status = 'delivered'
    GROUP BY oo.order_id, oo.customer_id, oo.order_delivered_customer_date
),
monthly_income AS (
    SELECT 
        month_no,
        SUM(CASE WHEN year = '2016' THEN payment_value ELSE 0 END) AS Year2016,
        SUM(CASE WHEN year = '2017' THEN payment_value ELSE 0 END) AS Year2017,
        SUM(CASE WHEN year = '2018' THEN payment_value ELSE 0 END) AS Year2018
    FROM order_income
    GROUP BY month_no
)
SELECT
    m.month_no,
    m.month,
    COALESCE(mi.Year2016, 0) AS Year2016,
    COALESCE(mi.Year2017, 0) AS Year2017,
    COALESCE(mi.Year2018, 0) AS Year2018
FROM (
    SELECT '01' AS month_no, 'Jan' AS month UNION ALL
    SELECT '02', 'Feb' UNION ALL
    SELECT '03', 'Mar' UNION ALL
    SELECT '04', 'Apr' UNION ALL
    SELECT '05', 'May' UNION ALL
    SELECT '06', 'Jun' UNION ALL
    SELECT '07', 'Jul' UNION ALL
    SELECT '08', 'Aug' UNION ALL
    SELECT '09', 'Sep' UNION ALL
    SELECT '10', 'Oct' UNION ALL
    SELECT '11', 'Nov' UNION ALL
    SELECT '12', 'Dec'
) m
LEFT JOIN monthly_income mi 
    ON m.month_no = mi.month_no
ORDER BY m.month_no;


--------------------------------------------REALIZADO--------------------------------------------------------

-- TODO: Esta consulta devolverá una tabla con los ingresos por mes y año.
-- Tendrá varias columnas: month_no, con los números de mes del 01 al 12;
-- month, con las primeras 3 letras de cada mes (ej. Ene, Feb);
-- Year2016, con los ingresos por mes de 2016 (0.00 si no existe);
-- Year2017, con los ingresos por mes de 2017 (0.00 si no existe); y
-- Year2018, con los ingresos por mes de 2018 (0.00 si no existe).
