INSERT INTO prediccion_fin_mundo( id_evento, nombre_evento ,fecha_evento  ,descripcion_evento ,dias_faltantes ,fuente_predicción)
SELECT
id_evento,
nombre_evento ,
fecha_evento , 
descripcion_evento,
fecha_evento - CURRENT_DATE as dias_faltantes,
'No se que va aca'
FROM eventos_apocalipticos		