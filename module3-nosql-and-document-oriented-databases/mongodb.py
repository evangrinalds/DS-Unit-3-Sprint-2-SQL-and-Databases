import pymongo

password = 'uZLDbYg2fwlyUZld' # Don't commit/share this! Reset it if it leak
dbname = 'test'
connection = client = ('mongodb+srv://egrinalds:' + password +
                       '@cluster0.mmghk.mongodb.net/' + dbname +
                       '?retryWrites=true&w=majority')

client = pymongo.MongoClient(connection)
db = client.test

db.test.insert_one({'x': 1})

db.test.count_documents({'x': 1})

db.test.insert_one({'x': 1})

db.test.count_documents({'x': 1})

db.test.insert_one({'x': 1})

curs = db.test.find({'x': 1})

list(curs)

# Let's add some more interesting documents

byrnes_doc = {
    'animal': 'manatee',
    'color': 'green',
    'number': 7
}

daves_doc = {
    'animal': 'bat',
    'color': 'red',
    'number': 1000
}

sasanas_doc = {
    'animal': 'orca',
    'color': 'blue',
    'number': 9
}

tylers_doc = {
    'animal': 'hippogryph',
    'cities': ['New York', 'Houston']
}

walters_doc = {
    'color': 'chartreuse',
    'animal': 'platypus'
}

aarons_doc = {
    'inner_dict': {
        'x': 2,
        'y': -4,
        'z': 'banana'
    },
    'another_key': (2, 6, 3)
}

# Let's put them all in a list for convenience
all_docs = [byrnes_doc, daves_doc, sasanas_doc, tylers_doc, walters_doc,
            aarons_doc]
len(all_docs)

db.test.insert_many(all_docs)

list(db.test.find())

db.test.find_one({'color': 'green'})

db.test.insert_one({
    'animal': 'tiger',
    'color': 'green',
    'city': 'Paris'
})

db.test.find_one({'color': 'green'})

list(db.test.find({'color': 'green'}))

more_docs = []
for i in range(10):
    doc = {'even': i % 2 == 0}
    doc['value'] = i
    more_docs.append(doc)

db.test.insert_many(more_docs)

list(db.test.find({'even': True, 'value': 0}))

list(db.test.find({'even': True, 'value': 7}))  # Doesn't exist!

list(db.test.find({'even': True}))

# We have both inserted (created) and found (read) entries in the database
# Mongo does CRUD
# Let's check out U: Update
# And D: Destroy (or Delete)
help(db.test.update_one)

result = db.test.update_one({'x': 1}, {'$inc': {'x': 3}})

result = db.test.update_one({'x': 100}, {'$inc': {'x': 300}})

list(db.test.find())


