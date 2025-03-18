"""Script that will visualise transformed data using Streamlit."""

import streamlit as st
from database import get_pokemon_names, get_location_names, add_entry_to_database, get_primary_type


def location_box(location_list: list[str]) -> str:
    selected_location = st.selectbox(
        "Choose a location:", options=location_list, index=0)

    return selected_location


def pokemon_name_box(pokemon_list: list[str], player_number: int) -> str:
    selected_pokemon = st.selectbox(
        f"Player {player_number} Pokémon:",
        options=pokemon_list,
        index=0
    )

    return selected_pokemon


def home_page() -> None:
    """Home page for the Streamlit application."""
    location_list = get_location_names()
    pokemon_list = get_pokemon_names()

    # Create two columns for the two players' dropdowns
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        location = location_box(
            location_list
        )
    # Player 1's Pokémon selection
    with col2:
        player1_pokemon = pokemon_name_box(
            pokemon_list, player_number=1)

    # Player 2's Pokémon selection
    with col3:
        player2_pokemon = pokemon_name_box(
            pokemon_list, player_number=2)

    player1_primary_type = get_primary_type(player1_pokemon)
    player2_primary_type = get_primary_type(player2_pokemon)

    with col4:
        if player1_primary_type and player2_primary_type:
            if player1_primary_type == player2_primary_type:
                st.write("❌")
                disable_button = True
            else:
                st.write("✅")
                disable_button = False
        else:
            st.write("Please select Pokémon to check types.")
            disable_button = True

    with col5:
        if st.button("Add Entry"):
            # Call function to add the matchup to the database
            add_entry_to_database(location, player1_pokemon, player2_pokemon)


if __name__ == "__main__":
    home_page()
