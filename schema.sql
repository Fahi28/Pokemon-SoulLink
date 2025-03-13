DROP TABLE IF EXISTS type_assignment;
DROP TABLE IF EXISTS pokemon_type;
DROP TABLE IF EXISTS pokemon;
DROP TABLE IF EXISTS location;

CREATE TABLE pokemon (
    pokemon_id INT GENERATED ALWAYS AS IDENTITY,
    pokemon_name VARCHAR(30) UNIQUE NOT NULL,
    PRIMARY KEY (pokemon_id)
);

CREATE TABLE pokemon_type(
    type_id INT GENERATED ALWAYS AS IDENTITY,
    type_name VARCHAR(30) UNIQUE NOT NULL,
    PRIMARY KEY (type_id)
);

CREATE TABLE type_assignment (
    type_assignment_id INT GENERATED ALWAYS AS IDENTITY,
    pokemon_id INT,
    type_id INT,
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
    FOREIGN KEY (type_id) REFERENCES pokemon_type(type_id),
    PRIMARY KEY (type_assignment_id)
);

CREATE TABLE location (
    location_id INT GENERATED ALWAYS AS IDENTITY,
    location_name VARCHAR(255) UNIQUE NOT NULL,
    PRIMARY KEY (location_id)
);

INSERT INTO pokemon_type
    (type_name)
VALUES
     ('Fighting'), ('Rock'), ('Psychic'), ('Normal'), ('Ghost'),
     ('Dragon'), ('Fire'), ('Dark'), ('Electric'), ('Bug'), ('Ice'),
     ('Water'), ('Grass'), ('Steel'), ('Poison'), ('Ground'), ('Flying'),
     ('Fairy');

INSERT INTO location (location_name)
VALUES
('Mystery Zone'), ('Faraway Place'), ('Vaniville Town'),
('Route 1'), ('Vaniville Pathway'), ('Aquacorde Town'),
('Route 2'), ('Avance Trail'), ('Santalune Forest'),
('Route 3'), ('Ouvert Way'), ('Santalune City'),
('Route 4'), ('Parterre Way'), ('Lumiose City'),
('Prism Tower'), ('Lysandre Labs'), ('Route 5'),
('Versant Road'), ('Camphrier Town'), ('Shabboneau Castle'),
('Route 6'), ('Palais Lane'), ('Parfum Palace'), ('Route 7'),
('Rivière Walk'), ('Cyllage City'), ('Route 8'), ('Muraille Coast'),
('Ambrette Town'), ('Route 9'), ('Spikes Passage'),
('Battle Chateau'), ('Route 10'), ('Menhir Trail'),
('Geosenge Town'), ('Route 11'), ('Miroir Way'),
('Reflection Cave'), ('Shalour City'), ('Tower of Mastery'),
('Route 12'), ('Fourrage Road'), ('Coumarine City'),
('Route 13'), ('Lumiose Badlands'), ('Route 14'),
('Laverre Nature Trail'), ('Laverre City'), ('Poké Ball Factory'),
('Route 15'), ('Brun Way'), ('Dendemille Town'), ('Route 16'),
('Mélancolie Path'), ('Frost Cavern'), ('Route 17'),
('Mamoswine Road'), ('Anistar City'), ('Route 18'),
('Vallée Étroite Way'), ('Couriway Town'), ('Route 19'),
('Grande Vallée Way'), ('Snowbelle City'), ('Route 20'),
('Winding Woods'), ('Pokémon Village'), ('Route 21'),
('Dernière Way'), ('Route 22'), ('Détourner Way'),
('Victory Road (Kalos)'), ('Pokémon League (Kalos)'),
('Kiloude City'), ('Battle Maison'), ('Azure Bay'),
('Dendemille Gate'), ('Couriway Gate'), ('Ambrette Gate'),
('Lumiose Gate'), ('Shalour Gate'), ('Coumarine Gate'),
('Laverre Gate'), ('Anistar Gate'), ('Snowbelle Gate'),
('Glittering Cave'), ('Connecting Cave'), ('Zubat Roost'),
('Kalos Power Plant'), ('Team Flare Secret HQ'), ('Terminus Cave'),
('Lost Hotel'), ('Chamber of Emptiness'), ('Sea Spirit''s Den'),
('Friend Safari'), ('Blazing Chamber'), ('Flood Chamber'),
('Ironworks Chamber'), ('Dragonmark Chamber'), ('Radiant Chamber'),
('Pokémon League Gate'), ('Lumiose Station'), ('Kiloude Station'),
('Ambrette Aquarium'), ('Unknown Dungeon');