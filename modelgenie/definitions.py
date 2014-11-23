from schematics.models import Model
from schematics.types import StringType
from schematics.types.compound import ListType, ModelType

class Definition(Model):
    name = StringType()
    kind = StringType()

    def __init__(self, **kwargs):
        """Initialize the Definition
        """
        super(Definition, self).__init__()
        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)

class FieldDefinition(Definition):
    pass

class ModelDefinition(Definition):
    field_definitions = ListType(ModelType(FieldDefinition))


