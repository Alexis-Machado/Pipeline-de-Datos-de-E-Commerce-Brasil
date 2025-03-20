WITH months AS (
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
),
orders_filtered AS (
  SELECT DISTINCT order_id,
         order_purchase_timestamp,
         order_delivered_customer_date,
         order_estimated_delivery_date,
         strftime('%m', order_purchase_timestamp) AS month_no,
         strftime('%Y', order_purchase_timestamp) AS year
  FROM olist_orders
  WHERE order_status = 'delivered'
    AND order_delivered_customer_date IS NOT NULL
)
SELECT 
  m.month_no,
  m.month,
  AVG(CASE WHEN of.year = '2016' THEN julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp) END) AS Year2016_real_time,
  AVG(CASE WHEN of.year = '2017' THEN julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp) END) AS Year2017_real_time,
  AVG(CASE WHEN of.year = '2018' THEN julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp) END) AS Year2018_real_time,
  AVG(CASE WHEN of.year = '2016' THEN julianday(order_estimated_delivery_date) - julianday(order_purchase_timestamp) END) AS Year2016_estimated_time,
  AVG(CASE WHEN of.year = '2017' THEN julianday(order_estimated_delivery_date) - julianday(order_purchase_timestamp) END) AS Year2017_estimated_time,
  AVG(CASE WHEN of.year = '2018' THEN julianday(order_estimated_delivery_date) - julianday(order_purchase_timestamp) END) AS Year2018_estimated_time
FROM months m
LEFT JOIN orders_filtered of ON m.month_no = of.month_no
GROUP BY m.month_no, m.month
ORDER BY m.month_no;


--------------------------------------------REALIZADO--------------------------------------------------------

-- TODO: Esta consulta devolverá una tabla con las diferencias entre los tiempos 
-- reales y estimados de entrega por mes y año. Tendrá varias columnas: 
-- month_no, con los números de mes del 01 al 12; month, con las primeras 3 letras 
-- de cada mes (ej. Ene, Feb); Year2016_real_time, con el tiempo promedio de 
-- entrega real por mes de 2016 (NaN si no existe); Year2017_real_time, con el 
-- tiempo promedio de entrega real por mes de 2017 (NaN si no existe); 
-- Year2018_real_time, con el tiempo promedio de entrega real por mes de 2018 
-- (NaN si no existe); Year2016_estimated_time, con el tiempo promedio estimado 
-- de entrega por mes de 2016 (NaN si no existe); Year2017_estimated_time, con 
-- el tiempo promedio estimado de entrega por mes de 2017 (NaN si no existe); y 
-- Year2018_estimated_time, con el tiempo promedio estimado de entrega por mes 
-- de 2018 (NaN si no existe).
-- PISTAS:
-- 1. Puedes usar la función julianday para convertir una fecha a un número.
-- 2. order_status == 'delivered' AND order_delivered_customer_date IS NOT NULL
-- 3. Considera tomar order_id distintos.
