from collections import OrderedDict

from carbon.models import Model
from carbon.types.base import (StringType, IntType,
                               BooleanType)
from carbon.types.compound import ListType, DictType, ModelType


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


class ModelDefinition(Definition):
    """Defines a Model
    """
    bases = ListType(StringType(), default=[])
    property_definitions = ListType(ModelType(PropertyDefinition), default=[])

    def __init__(self, **kwargs): 
        """Definition of a model
        """
        super(ModelDefinition, self).__init__(**kwargs)
        _property_defs = []
        for property_def in self.property_definitions: 
            _property_defs.append(PropertyDefinition(**property_def))
        self.property_definitions = _property_defs

    def _to_model_type(self):
        return ModelTypeDefinition(type='{}Type'.format(self.name),
                                   model_def=self
                                  )
    def _to_list_type(self):
        return ListTypeDefinition(type='{}ListType'.format(self.name),
                                  allow_type=self
                                 )
