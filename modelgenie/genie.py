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
    def get_definition(cls, model):
        """Convert a model to model_definition
        """
        return cls._proxy.get_definition(model)

    @classmethod
    def get_model(cls, model_def):
        """Convert a ModelDefinition to a ModelImpl
        """
        return cls._proxy.get_model(model_def)

    @classmethod
    def get_instance(cls, model_def):
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
        print '**definition = {}'.format(definition)
        if "_id" not in definition or definition['_id'] == None:
            saved_definition = cls._save_definition(definition)
            print 'saved_definition is {}'.format(saved_definition)
        inst["_definition"]= {"_id": saved_definition["_id"]}
        saved = cls._db.save(inst)
        print 'saved is {}'.format(saved)
        return saved

    @classmethod
    def _save_definition(cls, definition):
        """Save the definition of a model
        """
        if type(definition) != dict:
            definition = definition.serialize()
        # TODO(cc) save property definitions indivisually
        saved = cls._db.save(definition, 'ModelDefinition')
        return saved

    @classmethod
    def get(cls, id=None): 
        """Get a model instance
        Return the last inst if id is not provided
        """
        inst = cls._db.get(id, "Model")
        print 'inst = {}'.format(inst)
        definition_id = inst["_definition"]["_id"]
        definition = cls._get_definition(definition_id)
        inst['_definition'] = definition
        return inst

    @classmethod
    def _get_definition(cls, id):
        """Get model definition
        """
        return cls._db.get(id, 'ModelDefinition')

    @classmethod
    def list(cls, model_type=None): 
        """List all instances for a model type
        """
        instances = cls._db.list(model_type)
        return instances
