import pymongo





from pymongo import MongoClient

# replace <username>, <password>, and <clustername> with your own values
username = "gaurang1"
password = "gaurang123"
clustername = "cluster0"

# replace the <password> placeholder with the actual password, and surround it with double-quotes

# Create the MongoDB connection string
uri = f"mongodb+srv://{username}:{password}@{clustername}.qiy0wdm.mongodb.net/?retryWrites=true&w=majority"
print(uri)

# Create a new client and connect to the server
try:
    client = pymongo.MongoClient(uri)
    print('Successfully connected to MongoDB')
except Exception as e:
    print('Error connecting to MongoDB:', e)

# Insert data into the collection
data = {
    "name": "gauranggoro",
    "surname": "meghanathi",
    "subject": "nosql",
    "line" : "this is just a test"
}

database = client['myinfo']
collection = database['gau']

try:
    result = collection.insert_one(data)
    print('Data inserted with id:', result.inserted_id)
except Exception as e:
    print('Error inserting data:', e)
