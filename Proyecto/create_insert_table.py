import pandas as pd
import psycopg2
from psycopg2 import sql

def create_insert_table(df, table_name, db_params):
  
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()


    columns = ", ".join([f"{col} {dtype}" for col, dtype in zip(df.columns, df.dtypes.replace({'object': 'VARCHAR', 'int64': 'INTEGER', 'float64': 'FLOAT'}).items())])
    create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
        sql.Identifier(table_name),
        sql.SQL(columns)
    )
    cursor.execute(create_table_query)


    for i, row in df.iterrows():
        insert_query = sql.SQL("INSERT INTO {} VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(sql.Placeholder() * len(row))
        )
        cursor.execute(insert_query, tuple(row))
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Tabla '{table_name}' creada exitosamente.")
