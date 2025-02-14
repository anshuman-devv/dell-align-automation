from pymongo import MongoClient

# MONGO_URI = "mongodb+srv://khandelwalakshita041:zLpXcxnKMxB2dwm5@cluster0.9nyzw.mongodb.net"
MONGO_URI = "mongodb://localhost:27017"
conn = MongoClient(MONGO_URI)
db = conn.notes
coll = db["Notes"]

userdb = db["Users"]

comments_coll = db["comments"]


def get_collection(name: str):
    return db[name]