from pymongo.mongo_client import MongoClient
import urllib 

# Encode the username and password for safe URL usage
username = urllib.parse.quote_plus("")  # Add your MongoDB username
password = urllib.parse.quote_plus("")  # Add your MongoDB password

# MongoDB connection URI (Replace <appName> with your actual MongoDB cluster/app name)
uri = "mongodb+srv://{}:{}@<appName>.scone.mongodb.net/?retryWrites=true&w=majority&appName=<appName>".format(username, password)

# Create a new MongoDB client and establish a connection to the server
client = MongoClient(uri)

# Specify the database to use
mydb = client["user_database"]

# Specify the collection (table equivalent in MongoDB) to store user data
users_collection = mydb["users"]
