"""Takes the data from a CSV and puts it into a DataFrame"""

import pandas as pd
import psycopg2
from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor


def csv_to_dataframe() -> pd.DataFrame:
    """Puts CSV information into DataFrame"""
    pokemon_dataframe = pd.read_csv("All_Pokemon.csv")
    return pokemon_dataframe[['Name', 'Type 1', 'Type 2']]


def clean_names(pokemon_df: pd.DataFrame) -> pd.DataFrame:
    """Removes Mega pokemon from dataframe"""
    return pokemon_df[~pokemon_df['Name'].str.contains(
        'Mega', case=False, na=False)]


def get_connection() -> connection:
    """ Establishes a connection with database. """
    return psycopg2.connect(f"""dbname=pokemon user=fahad""")


def get_cursor(connect: connection) -> cursor:
    """ Create a cursor to send and receive data. """
    return connect.cursor(cursor_factory=RealDictCursor)


def get_foreign_key(db_cursor: psycopg2.extensions.cursor, attribute: str, table_name: str,
                    column_name: str, value: str) -> int:
    """ Gets foreign keys. """

    db_cursor.execute(
        f"SELECT {attribute} FROM {table_name} WHERE {column_name} = '{value}'")
    result = db_cursor.fetchone()
    if result:
        return result
    raise ValueError('Invalid Data!')


if __name__ == "__main__":
    df = csv_to_dataframe()
    print(df)
