"""Seed the pokemon table"""
import pandas as pd
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


def populate_type_assignments() -> None:
    """Populate the type_assignment table with the Pokémon types from the CSV"""
    try:
        # Get DataFrame from the CSV
        df = csv_to_dataframe()
        df = clean_names(df)

        # Connect to the database
        conn = get_connection()
        cur = conn.cursor()

        # Loop through each row in the dataframe
        for _, row in df.iterrows():
            pokemon_name = row['Name']
            types = [row['Type 1'], row['Type 2']]  # Types for the Pokémon

            # Get pokemon_id from the pokemon_name
            cur.execute(
                "SELECT pokemon_id FROM pokemon WHERE pokemon_name = %s", (pokemon_name,))
            pokemon_id = cur.fetchone()

            if pokemon_id:
                pokemon_id = pokemon_id[0]  # Extract the pokemon_id
            else:
                print(f"Pokémon {pokemon_name} not found in the database.")
                continue  # Skip if Pokémon isn't found

            # Loop through the types (ignore empty types)
            for type_name in types:
                if pd.notna(type_name):  # Only process non-empty types
                    cur.execute(
                        "SELECT type_id FROM pokemon_type WHERE type_name = %s", (type_name,))
                    type_id = cur.fetchone()

                    if type_id:
                        type_id = type_id[0]  # Extract the type_id
                        # Insert into type_assignment table
                        cur.execute(
                            "INSERT INTO type_assignment (pokemon_id, type_id) VALUES (%s, %s)",
                            (pokemon_id, type_id)
                        )
                    else:
                        print(f"Type {type_name} not found in the database.")

        # Commit the changes to the database
        conn.commit()
        cur.close()
        conn.close()

        print("Type assignment table populated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    conn = get_connection()
    try:
        app_cursor = get_cursor(conn)
        seed_pokemon_table(app_cursor)
        populate_type_assignments()
    finally:
        app_cursor.close()
        conn.close()
