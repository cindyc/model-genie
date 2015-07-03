"""ModelGenie
"""
import json
from collections import OrderedDict
import inspect

from schematics.models import Model
# these imports are necessary for globals() to work
# they'll be fixed
from schematics.types.base import *
from schematics.types.compound import *

from model.definitions import ModelDefinition, PropertyDefinition
from model.proxy.schematics_proxy import SchematicsProxy
from archiver import FilebasedTypeArchiver


class PersistableModel(Model):
    """A wrapper for Model that makes a Model *class* serializable
    """
    type_meta = None
    type_name = None
    archiver = FilebasedTypeArchiver()

    @classmethod
    def serialize_type(cls):
        """Serialize a custom type
        """
        # pop the validators for now
        serializable_fields = OrderedDict()

        for field_name, field_type in cls._fields.iteritems():
            serializable_field = OrderedDict()
            serializable_field['type_name'] = cls._get_type_name(field_type)
            for k, v in field_type.__dict__.iteritems():
                if k is 'owner_model':
                    serializable_field[k] = cls.__name__
                elif k is 'validators': # ignore validators for now
                    pass
                else:
                    serializable_field[k] = v
            serializable_fields[field_name] = serializable_field
        serializables = {
                'type_name': cls.__name__,
                'fields': serializable_fields
                }
        return serializables

    @classmethod
    def create_type(cls, data):
        """Create a schematic Model dynamically
        """
        class_name = data['type_name']
        cls_attrs = {}
        for field_name, serialized_field in data['fields'].iteritems():
            field_type_name = serialized_field['type_name'].split('.')[-1]
            # TODO (cc) fix this part
            field_type = globals()[field_type_name]
            if field_type_name in ('ListType', 'ModelType'):
                # TODO (cc) fix this: get the type for ModelType from data
                # cls_attrs[field_name] = field_type(ModelType(Person))
                pass
            else:
                cls_attrs[field_name] = field_type()
        klass = type(class_name, (Model, ), cls_attrs)
        return klass

    @classmethod
    def load_type(cls, name=None, data=None):
        """Load a Model type
        """
        if name:
            data = cls.archiver.query({'type_name': name})
        klass = cls.create_type(data)
        return klass

    @classmethod
    def list_types(cls, filters=None, serialized=True):
        """List types
        """
        matched = cls.archiver.query(filters=filters)
        klasses = []
        for data in matched:
            if serialized:
                klasses += (data,)
            else:
                klasses += (cls.create_type(data), )
        return klasses

    @classmethod
    def get_type_name(cls, obj):
        return '.'.join([inspect.getmodule(obj).__name__,
                         type(obj).__name__])


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
    _proxy = SchematicsProxy

    @classmethod
    def get_definition(cls, model):
        """Get ModelDefinition from a model class
        """
        return cls._proxy.get_definition(model)

    @classmethod
    def get_model(cls, model_def):
        """Convert a ModelDefinition to a model class
        """
        return cls._proxy.get_model(model_def)

    @classmethod
    def create_model(cls, model_def):
        """Convert a ModelDefinition to a Model
        """
        return cls._proxy.create_model(model_def)
