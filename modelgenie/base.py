"""Extend the schematics Model to make it persistable
"""
import json
from collections import OrderedDict
import inspect

from schematics.models import Model
# these imports are necessary for globals() to work
# they'll be fixed 
from schematics.types.base import * 
from schematics.types.compound import *

from modelgenie.definitions import ModelDefinition, FieldDefinition
from archiver import FilebasedTypeArchiver

"""
TODOs:
    1. logging needs to be added
    2. Refactor functions in SchematicsModelGenie to parent 
"""

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

class SchematicsModelGenie(ModelGenie):

    # TODO (cc) complete this 
    field_type_mapping = {
        'String': 'schematics.types.base.StringType',
        'Int': 'schematics.types.base.IntType',
        'List': 'schematics.type.compound.ListType',
    }

    # mapping the FieldDefnition keys to the schematics field definition
    # keys
    field_def_key_mapping = {
        'owner_model': 'owner_model',
        'is_required': 'required',
        'choices': 'choices',
        'messages': 'messages',
        'min_size': 'min_size',
        'max_size': 'max_size',
        'min_length': 'min_length',
        'max_length': 'max_length',
        'default': '_default',
    }

    @classmethod
    def get_definition(cls, model):
        """Given a Schematics model, inspect its model and fields and make a 
        model_definition
        """
        model_type = model.__name__
        model_def = ModelDefinition(name=model_type, type=model_type)
        for field_name, field_type in model._fields.iteritems():
            # get the schematics field type and convert to our field type
            field_def = FieldDefinition(name=field_name, 
                                        type=cls._to_type_def(field_type))
            field_type_data = field_type.__dict__
            for def_name, getter_key in cls.field_def_key_mapping.iteritems():
                if getter_key in field_type_data:
                    field_value = field_type_data[getter_key]
                    setattr(field_def, def_name, field_value)
                else:
                    print 'Warning: key {} does not exist'.format(def_name)
            model_def.field_definitions.append(field_def)
        return model_def
    
    @classmethod
    def create_model(cls, model_def):
        """Create a schematic Model based on model_defintion 
        """
        # model_def can be passed in as ModelDefinition or dict
        if isinstance(model_def, ModelDefinition):
            model_def = model_def.serialize()

        cls_attrs = {}
        for field_def in model_def['field_definitions']:
            field_impl = cls._to_field_impl(field_def)
            cls_attrs[field_def['name']] = field_impl
        class_name = model_def['name']
        klass = type(class_name, (Model, ), cls_attrs)
        return klass

    @classmethod
    def _to_field_impl(cls, field_def):
        """Given a FieldDefinition, convert to to a impl specific Field
        """
        if isinstance(field_def, FieldDefinition):        
            field_def = field_def.serialize()

        field = cls._to_type_impl(field_def)

        for def_key, value in field_def.iteritems():
            if def_key not in ('name', 'type', 'collection_definition'):
                impl_key = cls.field_def_key_mapping[def_key]
                setattr(field, impl_key, value)
        return field

    @classmethod
    def _to_type_def(cls, imp_field_type):
        """Given a schematic field type, return a ModelGenie field type
        """
        imp_type_name = cls.get_type_name(imp_field_type)
        # it's unfortunate that field_type_mapping has to be inverted
        inverted_field_type_mapping = dict(zip(cls.field_type_mapping.values(), 
                                          cls.field_type_mapping.keys()))
        if imp_type_name in inverted_field_type_mapping: 
            return inverted_field_type_mapping[imp_type_name]
        else:
            return imp_type_name

    @classmethod
    def _to_type_impl(cls, field_def):
        """Given a type definition, return a schematics type
        """
        if field_def['type'] == 'Collection':
            return cls._to_compound_type_impl(field_def)
        else:
            return cls._to_base_type_impl(field_def)

    @classmethod
    def _to_base_type_impl(cls, field_def):
        """Given a type definition, turn it into a impl specific type
        """
        if field_def['type'] in cls.field_type_mapping:
            impl_type_name = cls.field_type_mapping[field_def['type']]
        else:
            impl_type_name = field_def['type']
        field_type = globals()[impl_type_name.split('.')[-1]]
        print 'field_type is {}'.format(field_type)
        return field_type()

    @classmethod
    def _to_compound_type_impl(cls, field_def):
        """give a field definition , turn it into a impl specific compound type
        """
        collection_def = field_def['collection_definition']
        collection_type_name = collection_def['type']
        if collection_type_name in cls.field_type_mapping:
            col_impl_type_name = cls.field_type_mapping[collection_type_name]
        else:
            col_impl_type_name = collection_type_name
        print 'col_impl_type_name is {}'.format(col_impl_type_name)
        col_impl_type = globals()[col_impl_type_name.split('.')[-1]]
        allowed_type = collection_def['allow_type']
        print 'allowed_type is {}'.format(allowed_type)
        if not allowed_type['is_model']:
            # if it's String, Int etc 
            allowed_type_impl = cls._to_type_impl(allowed_type)
        else:
            model_type_impl = globals()['ModelType']
            # I don't know what to do here 
            allowed_type_impl = model_type_impl()

        print 'allowed_type_impl is {}'.format(allowed_type_impl)
        return col_impl_type(allowed_type_impl)

    @classmethod
    def get_type_name(cls, obj): 
        return '.'.join([inspect.getmodule(obj).__name__, 
                         type(obj).__name__])

    @classmethod
    def get_class_name(cls, obj):
        return obj.__name__


class ArchivableModel(Model):
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
            serializable_field['type_name'] = cls.get_type_name(field_type)
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
        """Create a schematic Model based dynamically
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
