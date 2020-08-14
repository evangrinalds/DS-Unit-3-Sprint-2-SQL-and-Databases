import psycopg2
'''
# ## Titanic Data from PostgregDB
# ---
# 1- How many passengers survived, and how many died?
# 2- How many passengers were in each class?
# 3- How many passengers survived/died within each class?
# 4- What was the average age of survivors vs nonsurvivors?
# 5- What was the average age of each passenger class?
# 6- What was the average fare by passenger class? By survival?
# 7- How many siblings/spouses aboard on average, by passenger class?
#  By survival?
# 8- How many parents/children aboard on average, by passenger class?
#  By survival?
# - Do any passengers have the same name?
# - (Bonus! Hard, may require pulling and processing with Python)
#  How many married?
#   couples were aboard the Titanic? Assume that two people (one `Mr.` and one
#   `Mrs.`) with the same last name
# and with at least 1 sibling/spouse aboard are
#   a married couple.
'''
passenger_survived = '''
SELECT count(Survived) as passsenger_survived
From Titanic as c WHERE Survived = 1;'''
passenger_died = '''
SELECT count(Survived) as Died  From Titanic as c WHERE Survived = 0;'''
# Question 2 How many passengers were in each class?
passenger_count_class = '''
SELECT pclass, count(Survived) as People_died
From Titanic as c WHERE Survived = 0 GROUP by Pclass;'''
# Question 3
passenger_sur_class = '''
SELECT pclass, Survived ,count(*) as Passenger_count From Titanic as c
GROUP by Pclass , Survived;'''
# Question 4 What was the average age of survivors vs nonsurvivors?
Q4 = '''
SELECT Survived, round(avg(AGE),2) as Average_age From Titanic
as c GROUP by  Survived;'''
# Question 5 What was the average age of each passenger class?
Q5 = '''
SELECT Pclass, round(avg(AGE),2) as Average_age
From Titanic as c GROUP by  Pclass;'''
# Question 6 What was the average fare by passenger class?
Q6 = '''
SELECT Pclass, round(avg(Fare),2), Survived as Avg_fare
From Titanic as c GROUP by  Pclass, Survived;'''
# Question 6.5 By survival?
Q6_5 = '''
SELECT Pclass, round(avg(Fare),2) as AVG_fare, Survived
From Titanic as c GROUP by  Pclass, Survived;'''
# Question 7  How many siblings/spouses aboard on average,
# by passenger class? By survival?
Q7 = '''
SELECT Pclass, round(avg("Siblings/Spouses Aboard"),2) as Sib_N_Spouse
from titanic GROUP by Pclass;'''
# Question 7.5 By survival?
Q7_5 = '''
SELECT Survived, round(avg("Siblings/Spouses Aboard"),2) as AVG_Sib_N_Spouse
from titanic2 GROUP by Survived;'''
# Question 8 How many parents/children aboard on average,
# by passenger class? By survival?
Q8 = '''
SELECT Pclass, round(avg("Parents/Children Aboard"),2)
as Average_Parent_Children
from titanic2 group by Pclass;'''
# Question 8.5 By survival?
Q8_5 = '''
SELECT Survived, round(avg("Parents/Children Aboard"),2)
as Average_Parent_Children
from titanic2 group by Survived;'''

dbname = 'XXX'
user = 'XXX'
password = 'XXX'
host = 'ruby.db.elephantsql.com'
pg_conn = psycopg2.connect(dbname=dbname, user=user,
                           password=password, host=host)
pg_curs = pg_conn.cursor()


Q1 = '''
SELECT count(survived) as passsenger_survived
From Titanic WHERE survived = 1;'''

help(pg_curs.execute)

Q1 = """
SELECT COUNT(survived) as passsenger_survived
FROM Titanic WHERE survived = 1;"""
result = pg_curs.execute(Q1)


print('Q1 How many passenger survived?:')
print('Passenger Survived', pg_curs.fetchall()[0][0], '.')


print('Q1_5 How many passenger died?:')
passenger_died = '''
SELECT count(Survived) as Died
From Titanic as c WHERE Survived = 0;'''
pg_curs.execute(passenger_died)
print('Passenger Died', pg_curs.fetchall()[0][0], '.')

passenger_count_class = '''
SELECT pclass, count(Survived) as People_died
From Titanic as c WHERE Survived = 0 GROUP by Pclass;'''
pg_curs.execute(passenger_count_class)
test = pg_curs.fetchall()
for people in test:
    print(f'Pclass: {people[0]}, People who died: {people[1]}.')

# How many passenger in each class?
print('Q2 How many passengers were in each class?:')
test = 'SELECT Pclass, count(*) from titanic GROUP by Pclass;'
pg_curs.execute(test)
test1 = pg_curs.fetchall()
for people in test1:
    print(f'Pclass: {people[0]}, # of people: {people[1]}.')

# How many passengers survived/died within each class?
print('Q3 How many passengers survived/died within each class?')
passenger_sur_class = '''
SELECT pclass, Survived ,count(*) as Passenger_count
From Titanic as c GROUP by Pclass , Survived Order by Pclass;'''
pg_curs.execute(passenger_sur_class)
test = pg_curs.fetchall()
for people in test:
    print(
        f'Pclass: {people[0]}, '
        f'Survived: {people[1]}, Passenger_count: {people[2]}.')

print('Question 4 What was the average age of survivors vs nonsurvivors?')
Q4 = '''
SELECT Survived, round(avg(AGE),2) as Average_age
From Titanic as c GROUP by  Survived;'''
pg_curs.execute(Q4)
test = pg_curs.fetchall()
for people in test:
    print(f'Survived: {people[0]}, Average_age: {people[1]}.')

print('Question 5 What was the average age of each passenger class?')
Q5 = '''
SELECT Pclass, round(avg(AGE),2) as Average_age
From Titanic as c GROUP by  Pclass;'''
pg_curs.execute(Q5)
test = pg_curs.fetchall()
for people in test:
    print(f'Pclass: {people[0]}, Average Age: {people[1]}.')


print("Question 6 What was the average fare by passenger class?")
Q6 = 'SELECT Pclass, avg(fare) as average_fare From Titanic  GROUP by  Pclass;'
pg_curs.execute(Q6)
test = pg_curs.fetchall()
for people in test:
    print(f'Pclass: {people[0]}, Average Fare: ${round(people[1],2)}.')

print('Question 6.5 By survival?')
Q6_5 = """
SELECT Survived ,avg(Fare) as AVG_fare
From Titanic as c GROUP by  Pclass, Survived;"""
pg_curs.execute(Q6)
test = pg_curs.fetchall()
for people in test:
    print(f'Pclass: {people[0]}, Average Fare: ${round(people[1],2)}.')

print('Question 7  How many siblings/spouses',
      'aboard on average, by passenger class?')
Q7 = '''
SELECT Pclass, round(avg(sibling_spouses_aboard),2)
as Average_Sibling_and_Spouse
from titanic GROUP by Pclass;'''
pg_curs.execute(Q7)
test = pg_curs.fetchall()
for people in test:
    print(
        f'Pcalss: {people[0]}, Average number of Sibling/ Spouse:'
        f'{round(people[1],2)}.')

print("Question 7.5 By survival?")
Q7_5 = '''
SELECT Survived, round(avg(sibling_spouses_aboard),2) as AVG_Sib_N_Spouse
from titanic GROUP by Survived;'''
pg_curs.execute(Q7_5)
test = pg_curs.fetchall()
for people in test:
    print(
        f'Survived: {people[0]}, Average number of Sibling/ Spouse:'
        f' {round(people[1],2)}.')

print("Question 8 How many parents/children ",
      "aboard on average, by passenger class? By survival?")
Q8 = '''
SELECT Pclass, round(avg(parent_children_aboard),2)
as  Average_Parent_Children
from titanic group by Pclass;'''
pg_curs.execute(Q8)
test = pg_curs.fetchall()
for people in test:
    print(
        f'Pclass: {people[0]}, ',
        f'Average number of Parent/Chidren: {round(people[1],2)}.')

print("Question 8.5 By survival?")
Q8_5 = '''
SELECT Survived, round(avg(parent_children_aboard),2)
as Average_Parent_Children from titanic group by Survived;'''
pg_curs.execute(Q8_5)
test = pg_curs.fetchall()
for people in test:
    print(
        f'Pclass: {people[0]},',
        f'Average number of Parent/Chidren: {round(people[1],2)}.')