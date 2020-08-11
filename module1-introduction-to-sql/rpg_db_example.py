import sqlite3


def connect_to_db(db_name='rpg_db.sqlite3'):
    return sqlite3.connect(db_name)


def execute_query(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()


conn = connect_to_db()
curs = conn.cursor()


# Total Number of Characters
total_characters = """
    SELECT COUNT(*)
    FROM charactercreator_character;
    """
results1 = execute_query(curs, total_characters)
print(results1)
