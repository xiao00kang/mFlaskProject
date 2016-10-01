# encoding = utf-8

import pymongo


def db_text():
    db = get_db()
    coll = get_collection(db)
    insert_doc(coll)
    get_doc(coll)


def get_db():
    client = pymongo.MongoClient()
    db = client.shiye_db2
    return db


def get_collection(db):
    coll = db['zhiwei_info']
    return coll


def insert_doc(coll, info, url):
    info = {'info': info, 'url': url}
    coll.insert(info)


def find(coll, info):
    if coll.find_one({'info': info}):
        return True


def get_doc(coll):
    print(coll.find_one())

