from collections import OrderedDict

from schematics.models import Model
from schematics.types.base import (StringType, IntType,
                                   BooleanType)
from schematics.types.compound import ListType, DictType, ModelType
from schematics.types.serializable import serializable

"""
@TODO:
- Don't use schematics for validating and serializing definitions, this
  is just for prototyping

"""

class Definition(Model):
    """Base class of definitions.
    We need validation and serialization of the definitions,
    so definitions need to be models, for now just use schematics.
    Definitions can be persisted just like other models.
    """
    _id = StringType()
    name = StringType()
    type = StringType()

    def __init__(self, **kwargs):
        """Initialize the Definition
        """
        super(Definition, self).__init__()
        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                # this is a hack to allow passing EntityDefinition() instead of
                # EntityDefinition().serialize()
                if value:
                    if type(self._fields[key]) == DictType and type(value) != dict:
                        setattr(self, key, value.serialize())
                    else:
                        setattr(self, key, value)

    def _set_custom_attrs(self, attrs):
        pass

class DefinitionError(Exception):
    pass

class TypeDefinition(Definition):
    """Turns a Model into a ModelType
    """
    pass


class ModelTypeDefinition(TypeDefinition):
    type = 'Model'
    model_def = DictType(StringType(), StringType())


class ListTypeDefinition(TypeDefinition):
    """Definition for list of models
    """
    type = 'List'
    is_ordered = BooleanType()
    # need to support allowing a list of types
    allow_type = DictType(StringType(), StringType())


class CollectionDefinition(Definition):
    """Defines a Collection
    """
    # collection type can be list or dict
    is_ordered = BooleanType()
    allow_types = ListType(DictType(StringType(), StringType()))

class PropertyDefinition(Definition):
    """Defines a Field
    """
    owner_model = StringType()
    is_required = BooleanType()
    choices = ListType(StringType())
    min_size = IntType()
    max_size = IntType()
    messages = DictType(StringType(), ListType(StringType))
    compound_type = DictType(StringType(), StringType())


class EntityDefinition(Definition):
    """Defines a Model
    """
    bases = ListType(StringType(), default=[])
    property_definitions = ListType(ModelType(PropertyDefinition), default=[])

    def init(self, **attrs):
        if "name" not in attrs:
            raise DefinitionError("Name for an entity must be defined")
        self.name = attrs["name"]
        self.type = attrs["type"] if "type" in attrs else attrs["name"]
        if "property_definitions" in attrs:
            for property_data in attrs["property_definitions"]:
                property_def = PropertyDefinition(**property_data)
                self.property_definitions += (property_def, )

    def _to_model_type(self):
        return ModelTypeDefinition(type='{}Type'.format(self.name),
                                   model_def=self
                                  )
    def _to_list_type(self):
        return ListTypeDefinition(type='{}ListType'.format(self.name),
                                  allow_type=self
                                 )
