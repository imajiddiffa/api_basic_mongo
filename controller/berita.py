import time
from datetime import datetime
from exceptions import BadRequest
from bson.objectid import ObjectId
from model import db, Berita

beritaModel = Berita()

class BeritaController(object):
    def get_berita(self, berita_type):
        try:
            result = beritaModel.get_all(False, berita_type)
        except:
            result = []
        
        for each_result in result:
            each_result['_id'] = str(each_result['_id'])

        return result

    def create_berita(self, **kwargs):
        berita_title = kwargs.get("berita_title")
        berita_category = kwargs.get("berita_category")
        berita_type = kwargs.get("berita_type")
        berita_content = kwargs.get("berita_content")
        slug = kwargs.get("berita_slug")

        created_time = str(datetime.now())
        created_time_timestamp = str(int(time.time()))

        result_object = {
            "title": berita_title,
            "slug": slug,
            "type": berita_type,
            "category": berita_category,
            "content": berita_content,
            "created_time": created_time,
            "created_time_timestamp": created_time_timestamp,
            "updated_time": "",
            "updated_time_timestamp": "",
            "is_deleted": False,
            "view": 0,
        }

        result = beritaModel.insert(result_object)

        result_object.update({"_id": str(result.inserted_id)})

        return result_object

    def get_berita_by_slug(self, berita_slug, berita_type):
        result_object = {}
        updated_time = ""
        updated_time_timestamp = ""

        try:
            result_db = db.db.berita.find({
                "is_deleted": False,
                "slug": berita_slug,
                "type": berita_type
            })[0]
        except:
            result_db = []

        if result_db:
            try:
                updated_time = result_db['updated_time']
                updated_time_timestamp = result_db['updated_time_timestamp']
            except:
                pass

            result_object = {
                "_id": str(result_db['_id']),
                "title": result_db['title'],
                "slug": result_db['slug'],
                "type": result_db['type'],
                "category": result_db['category'],
                "content": result_db['content'],
                "created_time": result_db['created_time'],
                "created_time_timestamp": result_db['created_time_timestamp'],
                "updated_time": updated_time,
                "updated_time_timestamp": updated_time_timestamp,
                "view": result_db['view'],
                "is_deleted": result_db['is_deleted'],
            }

        return result_object

    def update_berita(self, berita_id, berita_object):
        type_berita = ""

        updated_time = str(datetime.now())
        updated_time_timestamp = str(int(time.time()))

        berita_object.update({
            "updated_time": updated_time,
            "updated_time_timestamp": updated_time_timestamp
        })

        try:
            update_result = beritaModel.update(berita_id, False, berita_object)
            print("test")
            try:
                type_berita = update_result['value']['type']
            except:
                pass
        except:
            raise BadRequest("Something happen when updated data", 200, 1)

        if type_berita:
            result = beritaModel.get_all(False, type_berita)
        else:
            raise BadRequest("Data already same as updated object", 200, 1)

        for each_result in result:
            each_result['_id'] = str(each_result['_id'])

        return result

    def delete_berita(self, berita_id):
        try:
            # mongo.db.blog.delete_one({'_id': ObjectId(blog_id), 'user_id': user_id})
            db.db.berita.find_and_modify(
                query={
                    '_id': ObjectId(berita_id),
                    "is_deleted": False
                },
                update={'$set': {
                    "is_deleted": True
                }},
                upsert=False,
                full_response=True)
        except:
            raise BadRequest("Something happen when updated data", 200, 1)