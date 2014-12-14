"""Proxy for Schematics
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
from modelgenie.proxy.base import ModelProxy, Types


class SchematicsProxy(ModelProxy):

    _Model = Model

    # TODO (cc) complete this 
    field_type_mapping = {
        Types.String: 'schematics.types.base.StringType',
        Types.Int: 'schematics.types.base.IntType',
        Types.Boolean: 'schematics.types.base.BooleanType',
        Types.Time: 'schematics.types.base.DateTimeType',
        Types.List: 'schematics.types.compound.ListType',
        Types.Model: 'schematics.types.compound.ModelType',
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
    def _to_collection_type_impl(cls, field_def):
        """Turn a field_def into a impl specific List or Dict type
        """
        # handle the compound type, i.e. ListType, etc
        collection_type_name = field_def['type']
        if collection_type_name in cls.field_type_mapping:
            collection_impl_type_name = cls.field_type_mapping[collection_type_name]
        else:
            collection_impl_type_name = collection_type_name
        collection_impl_type = cls._load_class(collection_impl_type_name)
        print 'collection_impl_type is {}'.format(collection_impl_type)

        allowed_type = field_def['compound_type']['allow_type']
        print 'allow_type is {}'.format(allowed_type)

        # handle the model embedded in the type, i.e. the Person in
        # ModelType(Person)
        #allowed_types = collection_def['allow_types']
        if allowed_type['type'] not in cls.field_type_mapping:
            # find the ORM modeltype, i.e. schematics.types.compound.ModelType
            model_type_impl_name = cls.field_type_mapping['Model']
            model_type_impl = cls._load_class(model_type_impl_name)
            # it gets complicated when its a custom model here (i.e.
            # ModelType(Person), the model_def should be embedded
            model_def = allowed_type
            model_class = cls.get_model(model_def)
            allowed_type_impl = model_type_impl(model_class) 
        else:
            # it's a primitive type, like String, Int etc 
            allowed_type_impl = cls._to_type_impl(allowed_type)

        # put compound type and its embedded content together
        compound_type = collection_impl_type(allowed_type_impl)
        return compound_type
