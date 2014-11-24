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
#from modelgenie.builtins import *

from archiver import FilebasedTypeArchiver

class ArchivableModel(Model):
    """A wrapper for Model that makes a Model *class* serializable
    """
    type_meta = None
    type_name = None
    archiver = FilebasedTypeArchiver()

    @classmethod
    def serialize_type(cls):
        """Serialize a Schematic model *class*
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
            print 'field_type_name = -->{}<--'.format(field_type_name)
            # TODO (cc) fix this part
            field_type = globals()[field_type_name]
            print 'field_type is {}'.format(field_type)
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
            print 'loading type with name = {}'.format(name)
            data = cls.archiver.query({'type_name': name})
        klass = cls.create_type(data)
        return klass

    @classmethod
    def list_types(cls, filters=None):
        """List types
        """
        matched = cls.archiver.query(filters=filters)
        klasses = []
        for data in matched: 
            klasses += (cls.create_type(data), )
        return klasses

    @classmethod
    def get_type_name(cls, obj): 
        return '.'.join([inspect.getmodule(obj).__name__, 
                         type(obj).__name__])
