from schematics.models import Model
from schematics.types import StringType, DateTimeType
from schematics.transforms import blacklist

class PersistableType(Model):
    
    @classmethod
    def serialize_type(cls):
        print 'Serializing the model type'
        serialized = {
            'name': cls.__class__.name,
            'kind': cls.__class__.name,
        }

class Person(Model):
    first_name = StringType()
    last_name = StringType(default="unknown")

def serialize_type(modeltype=Person):
    serialized = {
        'name': modeltype.__class__.name,
        'kind': modeltype.__class__.name, 
    } 
