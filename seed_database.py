"""Seed the pokemon table"""
import pandas
import psycopg2
from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor
from etl import csv_to_dataframe, clean_names


def get_connection() -> connection:
    """ Establishes a connection with database. """
    return psycopg2.connect(f"""dbname=pokemon user=fahad""")


def get_cursor(connect: connection) -> cursor:
    """ Create a cursor to send and receive data. """
    return connect.cursor(cursor_factory=RealDictCursor)


def insert_query(db_cursor: cursor, table: str, column: str, value: str) -> None:
    """ Insert query for database. """
    query = f"INSERT INTO {table} ({column}) VALUES (%s)"

    db_cursor.execute(query, (value,))


def seed_pokemon_table(db_cursor: cursor):
    """Will insert pokemon names into database"""
    pokemon_df = csv_to_dataframe()
    pokemon_df = clean_names(pokemon_df)
    print(pokemon_df)
    for name in pokemon_df['Name']:

        insert_query(db_cursor, 'pokemon', 'pokemon_name',
                     name)
    db_cursor.connection.commit()


if __name__ == "__main__":
    conn = get_connection()
    try:
        app_cursor = get_cursor(conn)
        seed_pokemon_table(app_cursor)
    finally:
        app_cursor.close()
        conn.close()
