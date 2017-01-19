# http://api.mongodb.com/python/current/tutorial.html

from pymongo import MongoClient

import datetime
import logging
import pprint

client = MongoClient()
logger = logging.getLogger(__name__)

DB_NAME = "eventbot"
DB_COLLECTION_APPL_FORM_LOG = "application_form_log"


def write_appl_form_log(d):
    """ Write a new application form log entry to the database.
    """
    db = client[DB_NAME]
    coll = db[DB_COLLECTION_APPL_FORM_LOG]
    entry = {
        'values': d,
        'date': datetime.datetime.utcnow()
    }
    doc_id = coll.insert_one(entry).inserted_id
    logger.info("Wrote application form log entry: {}".format(doc_id))


def test():
    db = client.test_database

    collection = db.test_collection

    post = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}

    posts = db.posts

    post_id = posts.insert_one(post).inserted_id
    print post_id
    print db.collection_names(include_system_collections=False)
    print db.posts

    pprint.pprint(posts.find_one())
