import numpy as np
import pandas as pd
import sqlite3
import psycopg2


dir(psycopg2)


dbname = 'XXX'
user = 'XXX'
password = 'XXX'
host = 'ruby.db.elephantsql.com'
pg_conn = psycopg2.connect(dbname=dbname, user=user,
                           password=password, host=host)

pg_curs = pg_conn.cursor()  # Works the same as SQLite!
help(pg_curs.execute)
help(pg_curs.executemany)
create_table_statement = """
CREATE TABLE test_table (
  id SERIAL PRIMARY KEY,
  name varchar(40) NOT NULL,
  data JSONB
);
"""
# NOTE - these types are PostgreSQL specific. This won't work in SQLite
pg_curs.execute(create_table_statement)
pg_conn.commit()  # "Save" by committing

insert_statement = """
INSERT INTO test_table (name, data) VALUES
(
  'A row name',
  null
),
(
  'Another row, with JSON this time',
  '{ "a": 1, "b": ["dog", "cat", 42], "c": true }'::JSONB
)
"""

pg_curs.execute(insert_statement)
pg_conn.commit()

query = 'SELECT * FROM test_table;'
pg_curs.execute(query)

pg_curs

pg_curs.fetchall()


pg_curs.execute('INSERT INTO test_table (name, data) VALUES (null, null);')


# Step 1 - Extract, getting data out of SQLite3
sl_conn = sqlite3.connect('rpg_db.sqlite3')
sl_curs = sl_conn.cursor()

# Our goal - copy the charactercreator_character table
get_characters = 'SELECT * FROM charactercreator_character;'
characters = sl_curs.execute(get_characters).fetchall()
len(characters)  # Correct number of characters
characters[:5]
sl_curs.execute('PRAGMA table_info(charactercreator_character);').fetchall()
create_character_table = """
CREATE TABLE charactercreator_character (
  character_id SERIAL PRIMARY KEY,
  name VARCHAR(30),
  level INT,
  exp INT,
  hp INT,
  strength INT,
  intelligence INT,
  dexterity INT,
  wisdom INT
);
"""
pg_curs.execute(create_character_table)
pg_conn.commit()
for character in characters:
    insert_character = """
    INSERT INTO charactercreator_character
    (name, level, exp, hp, strength, intelligence, dexterity, wisdom)
    VALUES """ + str(character[1:]) + ";"
    pg_curs.execute(insert_character)
pg_curs.execute('SELECT * FROM charactercreator_character LIMIT 5;')
pg_curs.fetchall()
pg_conn.commit()

# We've done a basic ETL! How can we verify?
len(characters)  # characters from SQLite

pg_curs.execute('SELECT * FROM charactercreator_character;')
pg_characters = pg_curs.fetchall()

len(pg_characters)

pg_characters[0]

# We could do more spot checks, but let's loop and check them all
for character, pg_character in zip(characters, pg_characters):
  assert character == pg_character
