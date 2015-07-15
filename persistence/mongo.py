from pymongo import MongoClient
from bson.objectid import ObjectId


# TODO(cc) Move these out
class DbProvider(object):
    pass

class DbProviderError(Exception):
    pass


class MongoDbProvider(DbProvider):
    """DbProvider using mongo
    """
    db_host = None
    db_port = None
    db_name = None
    _db = None
    _collection = None

    def __init__(self, db_host, db_port, db_name, model_type):
        """Initialize the db_client
        """
        _db_client = MongoClient(db_host, db_port)
        self._db = _db_client[db_name]
        self._collection = self._db[model_type]

    def get(self, id, model_type=None):
        """Get an obj by id
        created
        """
        # If collection is not specified, use the collection when this client is
        if not model_type:
            collection = self._collection
        else:
            collection = self._db[model_type]

        print 'mongo.get(): id={}'.format(id)
        if id:
            obj = collection.find_one({'_id': ObjectId(id)})
            if not obj:
                raise DbProviderError("DB record for {} is not found".format(id))
            obj['_id'] = str(obj['_id'])
        else:
            obj = {}
        return obj

    def list(self, model_type="Model"):
        """List all model instances
        """
        self._collection = self._db[model_type]
        print 'mongo.list()'
        objs = list(self._collection.find())
        print 'objs are {}'.format(objs)
        result = []
        # hack to convert uuid to string
        for obj in objs:
            obj['_id'] = str(obj['_id'])
            result += [obj, ]
        return objs

    def list_by_definition(self, definition):
        """Find the entities by their definition
        definition can be a string (uuid) or a dict 
        """
        print 'list_by_definition: definition is {}'.format(definition)
        if type(definition) == dict: 
            def_id = definition["_id"]
        elif type(definition) == str: 
            def_id = definition
        else: 
            raise DbProviderError("Invalid definition, can be either str(UUID) or dict")
        print 'find_by_definition: def_id={}='.format(def_id)
        objs = list(self._collection.find({"_definition._id": def_id}))
        result = []
        for obj in objs:
            obj["_id"] = str(obj['_id'])
            result += [obj, ]
        return objs

    def save(self, data, model_type=None):
        """Create a new record or update
        """
        print 'data is {}'.format(data)
        collection = self._db[model_type] if model_type else self._collection
        if type(data) == list:
            result = collection.insert_many(obj).inserted_ids
        elif type(data) != dict:
            obj = data.serialize()
        else:
            obj = data
        #if not hasattr(obj, '_id') or not obj._id:
        if not "_id" in obj or not obj["_id"]:
            print 'obj does not exist in db: {}'.format(obj)
            # this is necessary for mongodb to auto-generate the _id field
            if "_id" in obj:
                obj.pop('_id')
            # TODO(cc) is there anyway to have insert_one() return the doc?
            inserted_id = collection.insert_one(obj).inserted_id
            print 'inserted_id is {}'.format(inserted_id)
            result = self.get(inserted_id, model_type)
        else:
            print 'obj exists: {}'.format(obj)
            updated = collection.find_and_modify({'_id': ObjectId(obj._id)}, obj)
            result = updated
            print 'update result is {}'.format(result)
        return result

    def delete(self, id):
        """Delete a document by id
        """
        result = self._collection.remove({'_id': ObjectId(str(id))})
        # result is {u'n': 1, u'ok': 1} if deleted
        # TODO (cc) use constants for return codes and messages
        if result['ok'] == 1 and result['n'] == 1:
            return {'result': 'SUCCESS', 'msg': "Delete was successful", 'id': id}
        else:
            # TODO(cc) handle object not found error
            return {'result': 'FAILED', 'msg': 'Record not found in DB', 'id': id}
