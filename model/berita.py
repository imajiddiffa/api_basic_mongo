from . import db
from bson.objectid import ObjectId

class Berita(object):
    filter_param = dict

    def get_all(self, is_deleted=False, _type=None):
        try:
            result = list(
                db.db.berita.find({
                    "is_deleted": is_deleted,
                    "type": _type,
                }))
        except:
            result = []
        
        return result
    
    def insert(self, data=None):
        try:
            result = db.db.berita.insert_one(data)
        except Exception:
            raise
        
        return result

    def update(self, _id=None, is_deleted=False, data=None):
        try:
            result = db.db.berita.find_and_modify(
                query={
                    '_id': ObjectId(_id),
                    "is_deleted": is_deleted
                },
                update={'$set': data},
                upsert=False,
                full_response=True)
        except Exception:
            raise
        
        return result

    
        