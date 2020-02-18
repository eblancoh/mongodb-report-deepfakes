import pymongo
import configparser
from watcher import get_logger


config = configparser.ConfigParser()
config.read("config.ini")

logger = get_logger("database")

def db_complete(response):
    # Nos conectamos a la base de datos en mongodb atlas
    user = config['mongodb']['user']
    password = config['mongodb']['passwd']
    db_name = config['mongodb']['database']

    client = pymongo.MongoClient("mongodb+srv://" + user + ":" + password + "@" + db_name + "-edgz5.azure.mongodb.net/test?retryWrites=true&w=majority")
    db = client.deepfakes
    collection = db.faceforensics

    post_id = collection.insert_one(response).inserted_id
    logger.info("_id {} document inserted in database".format(post_id))

def db_check(response):
    # reponse is a json.loads(response.text)
    # Nos conectamos a la base de datos en mongodb atlas
    user = config['mongodb']['user']
    password = config['mongodb']['passwd']
    db_name = config['mongodb']['database']

    client = pymongo.MongoClient("mongodb+srv://" + user + ":" + password + "@" + db_name + "-edgz5.azure.mongodb.net/test?retryWrites=true&w=majority")
    db = client.deepfakes
    collection = db.faceforensics

    
    if collection.find({
                        "$or": [
                            {'hash': response['hash']}, 
                            {'link': response['link']}, 
                            {'filename': response['filename']}
                            ]
                        }).count() == 0:
        return False
    else:
        for x in collection.find({
                        "$or": [
                            {'hash': response['hash']}, 
                            {'link': response['link']}, 
                            {'filename': response['filename']}
                            ]
                        }):
            
            status = x["fake"]
        return status

def db_read(query, collector):
    """
    query: i.e., {"link": "https://www.youtube.com/watch?v=VWrhRBb-1Ig"}
                 {"filename": "Bill Hader channels Tom Cruise [DeepFake].mp4"}
    collector: "facewarpingartifacts" | "faceforensics"
    """
    user = config['mongodb']['user']
    password = config['mongodb']['passwd']
    db_name = config['mongodb']['database']
    logger.info("Connecting and retrieving info from database {} and collection {}".format(db_name, collector))
    client = pymongo.MongoClient("mongodb+srv://" + user + ":" + password + "@" + db_name + "-edgz5.azure.mongodb.net/test?retryWrites=true&w=majority")
    db = client.deepfakes

    if collector == "facewarpingartifacts":
        collection = db.facewarpingartifacts
    elif collector == "faceforensics":
        collection = db.faceforensics
    elif collector == "headpose":
        collection = db.headposes

    cursor = collection.find(query)
    logger.info("Query {} retrieved from database.".format(query))
    
    # Devolvemos el resultado del query
    return cursor




