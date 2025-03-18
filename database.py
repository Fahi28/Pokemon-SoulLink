"""Script containing SQL queries for Streamlit Application"""

import pandas as pd
import streamlit as st
from etl import get_connection, get_cursor


def get_location_names() -> list:
    try:
        conn = get_connection()
        cur = get_cursor(conn)

        cur.execute("SELECT location_name FROM location;")
        location = [row['location_name'] for row in cur.fetchall()]

        cur.close()
        conn.close()

        return location

    except Exception as e:
        st.error(f"Error fetching location: {e}")
        return []


def get_pokemon_names() -> list:
    try:
        conn = get_connection()
        cur = get_cursor(conn)

        cur.execute("SELECT pokemon_name FROM pokemon;")
        pokemon = [row['pokemon_name'] for row in cur.fetchall()]

        cur.close()
        conn.close()

        return pokemon

    except Exception as e:
        st.error(f"Error fetching Pokémon: {e}")
        return []


def get_primary_type(pokemon_name: str) -> str:
    """Retrieve the primary type of the Pokémon."""
    try:
        conn = get_connection()
        cur = get_cursor(conn)

        # Get the primary type of the selected Pokémon
        query = """
            SELECT pt.type_name
            FROM pokemon p
            JOIN type_assignment ta ON p.pokemon_id = ta.pokemon_id
            JOIN pokemon_type pt ON ta.type_id = pt.type_id
            WHERE p.pokemon_name = %s
            LIMIT 1;  -- Assuming primary type is the first one
        """
        cur.execute(query, (pokemon_name,))
        primary_type = cur.fetchone()

        # Close the cursor and connection
        cur.close()
        conn.close()

        if primary_type:
            return primary_type['type_name']
        else:
            st.error(f"Primary type for {pokemon_name} not found.")
            return ""

    except Exception as e:
        st.error(f"Error retrieving primary type: {e}")
        return ""


def add_entry_to_database(location: str, player1_pokemon: str, player2_pokemon: str) -> None:
    """Function to insert selected matchup into the database."""
    try:
        conn = get_connection()
        cur = get_cursor(conn)

        # Get location_id
        cur.execute(
            "SELECT location_id FROM location WHERE location_name = %s;", (location,))
        location_id = cur.fetchone()
        if location_id:
            location_id = location_id['location_id']
        else:
            st.error(f"Location '{location}' not found.")
            return

        # Get player1_pokemon_id
        cur.execute(
            "SELECT pokemon_id FROM pokemon WHERE pokemon_name = %s;", (player1_pokemon,))
        player1_pokemon_id = cur.fetchone()
        if player1_pokemon_id:
            player1_pokemon_id = player1_pokemon_id['pokemon_id']
        else:
            st.error(f"Pokemon '{player1_pokemon}' not found for Player 1.")
            return

        # Get player2_pokemon_id
        cur.execute(
            "SELECT pokemon_id FROM pokemon WHERE pokemon_name = %s;", (player2_pokemon,))
        player2_pokemon_id = cur.fetchone()
        if player2_pokemon_id:
            player2_pokemon_id = player2_pokemon_id['pokemon_id']
        else:
            st.error(f"Pokemon '{player2_pokemon}' not found for Player 2.")
            return

        # Insert into pokemon_matchup table
        query = """
            INSERT INTO pokemon_matchup (location_id, player1_pokemon_id, player2_pokemon_id)
            VALUES (%s, %s, %s);
        """
        cur.execute(
            query, (location_id, player1_pokemon_id, player2_pokemon_id))

        # Commit changes
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()

        st.success("Matchup added successfully!")

    except Exception as e:
        st.error(f"Error adding matchup: {e}")


if __name__ == "__main__":
    names = get_pokemon_names()
    print(names)
