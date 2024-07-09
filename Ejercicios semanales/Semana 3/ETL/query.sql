SELECT(EXTRACT(YEAR FROM fecha_evento)::int / 10) * 10 AS decada,
COUNT(*) AS cantidad_eventos,
AVG(dias_faltantes) as dias_promedio,
SUM(CASE
     WHEN nombre_evento LIKE 'D%' THEN 1 ELSE 0 END) as eventos_d,
SUM(CASE
     WHEN nombre_evento LIKE 'A%' THEN 1 ELSE 0 END ) as eventos_a
FROM prediccion_fin_mundo
GROUP BY decada