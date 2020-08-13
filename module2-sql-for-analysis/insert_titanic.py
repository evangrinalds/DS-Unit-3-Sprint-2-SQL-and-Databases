# imports
import psycopg2
import pandas as pd
from psycopg2.extras import execute_values

# Read in titanic
df = pd.read_csv('titanic.csv')

# Read into elephant
df['Siblings/Spouses Aboard'].rename('siblingsspouse', axis=1)
df['Parents/Children Aboard'].rename('parentschildren', axis=1)

# Clean data
df['Name'] = df['Name'].str.replace("'", "")

# Credential for cloud DB, password is TOP SECRET
dbname = 'XXX'
user = 'XXX'
password = 'XXX'
host = 'isilo.db.elephantsql.com'

# Connection to cloud
pg_conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)

# Cursor
pg_curs = pg_conn.cursor()

# Titanic Table
create_titanic_table = """
DROP TABLE IF EXISTS Titanic;
CREATE TABLE Titanic (
    index INT,
    Survived INT,
    Pclass INT,
    Name TEXT,
    Sex TEXT,
    Age REAL,
    siblingsspouse INT,
    parentschildren INT,
    Fare REAL
);
"""

# run table and commit table
pg_curs.execute(create_titanic_table)
pg_conn.commit()

# Using the execute_values function
execute_values(pg_curs, """
INSERT INTO Titanic
(Survived, Pclass, Name, Sex, Age, siblingsspouse, parentschildren, Fare)
VALUES %s;
""", [tuple(row) for row in df.values])

# commit
pg_conn.commit()

# Running to make sure works
pg_curs.execute("""
SELECT *
FROM Titanic
LIMIT 1;
""")

# printing to validate
print(pg_curs.fetchall())