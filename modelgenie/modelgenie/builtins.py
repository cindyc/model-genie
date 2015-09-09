from base import ArchivableModel

from schematics.types import StringType, IntType
from schematics.types.compound import ListType, ModelType

class Person(ArchivableModel):
    first_name = StringType()
    last_name = StringType()


class Place(ArchivableModel):
    location = StringType()
    zip_code = IntType()


class Event(ArchivableModel):
    venue = ModelType(Place)
    attendees = ListType(ModelType(Person))
