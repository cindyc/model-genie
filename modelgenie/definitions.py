from collections import OrderedDict

from schematics.models import Model
from schematics.types.base import (StringType, IntType, 
                                   BooleanType)
from schematics.types.compound import ListType, DictType, ModelType


class Definition(Model):
    """Base class of definitions. 
    We need validation and serialization of the definitions, 
    so definitions need to be models, for now just use schematics.
    Definitions can be persisted just like other models.
    """
    name = StringType()
    type = StringType()

    def __init__(self, **kwargs):
        """Initialize the Definition
        """
        super(Definition, self).__init__()
        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)


class TypeDefinition(Definition):
    is_model = BooleanType()


class CollectionDefinition(Definition): 
    """Defines a Collection
    """
    # collection type can be list or dict
    is_ordered = BooleanType()
    allow_type = ModelType(TypeDefinition)


class FieldDefinition(Definition):
    """Defines a Field
    """
    owner_model = StringType()
    is_required = BooleanType()
    choices = ListType(StringType())
    min_size = IntType()
    max_size = IntType()
    messages = DictType(StringType(), ListType(StringType))
    collection_definition = ModelType(CollectionDefinition)


class ModelDefinition(Definition):
    """Defines a Model
    """
    bases = ListType(StringType(), default=[])
    field_definitions = ListType(ModelType(FieldDefinition), default=[])
