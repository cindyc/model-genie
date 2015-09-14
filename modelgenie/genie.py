"""ModelGenie
"""
import json
from collections import OrderedDict
import inspect

from modelgenie.definitions import ModelDefinition, PropertyDefinition
# TODO (cc) move this to plugins
from modelgenie.proxy.carbon_proxy import CarbonProxy
from persistence.mongo import MongoDbProvider

PROXY = CarbonProxy
DB = MongoDbProvider(db_host='localhost', db_port=27017, db_name='datanarra', model_type='Model')


class ModelGenie(object):
    """ModelGenie makes a Model's definition persistable
    It does multi-way conversions, validations and serializations
    - Define a model in json and turn it into a ModelDefinition
    - Define an ORM model (i.e. django, schematics, sqlalchemy) and turn it into a
      ModelDefinition
    - Define a ModelDefinition and serialize it to json
    - Define a ModelDefinition and turn it into an ORM model
    - Define a model in json and turn it into an ORM model

    Why do we need it?
    ==================
    - New models can be defined dynamically (even user owned) by calling the rest API with model
      definition json
    - ModelDefintions can be serialized to json and persisted to database, and
      be queried and turned into ORM model on-demand
    - Provides an universal API to define models, ORM systems supported through plugins
    - Supporting compound types
    """
    _proxy = PROXY
    _db = DB

    @classmethod
    def create_definition(cls, data):
        """Convert ModelDefinition from dict or a ModelImpl
        """
        if type(data) == dict: 
            md = ModelDefinition(**data)
        return md

    @classmethod
    def save_definition(cls, definition):
        """Save the definition of a model
        """
        if type(definition) != dict:
            definition = definition.serialize()
        # TODO(cc) save property definitions individually
        saved = cls._db.save(definition, 'ModelDefinition')
        return saved

    @classmethod
    def create_model(cls, model_def):
        """Convert a ModelDefinition to a ModelImpl
        """
        return cls._proxy.get_model(model_def)

    @classmethod
    def create_instance(cls, model_def):
        """Create an instance of based on model definition
        """
        return cls._proxy.get_instance(model_def)

    @classmethod
    def save(cls, inst):
        """Save a model instance
        """
        if type(inst) != dict:
            definition = inst.__class__._definition
            inst = inst.serialize()
        else:
            definition = inst["_definition"]
        print '**definition = {}'.format(definition)
        if "_id" not in definition or definition['_id'] == None:
            definition = cls.save_definition(definition)
            print 'saved definition is {}'.format(definition)
        inst["_definition"]= {"_id": definition["_id"]}
        saved = cls._db.save(inst)
        print 'saved is {}'.format(saved)
        return saved


    @classmethod
    def get(cls, id=None):
        """Get a model instance
        Return the last inst if id is not provided
        """
        inst = cls._db.get(id, "Model")
        print 'inst = {}'.format(inst)
        definition_id = inst["_definition"]["_id"]
        definition = cls.get_definition(definition_id)
        inst['_definition'] = definition
        return inst

    @classmethod
    def get_definition(cls, id):
        """Get model definition
        """
        return cls._db.get(id, 'ModelDefinition')

    @classmethod
    def list(cls, model_type="Model"):
        """List all instances for a model type
        """
        instances = cls._db.find(model_type)
        return instances

    @classmethod
    def list_by_definition(cls, definition):
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
        # Get the definition from db and add to each model
        definition = cls.get_definition(def_id)
        result = cls._db.find("Model", {"_definition._id": def_id})
        insts = []
        for data in result: 
            data["_definition"] = definition
            insts += [data, ]
        return insts

    @classmethod
    def delete(cls, id):
        """Delete a model by id
        """
        pass

    @classmethod
    def delete_definition(cls, id):
        """Delete a model definition by id
        """
        pass
