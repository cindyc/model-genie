from modelgenie.builtins import (Person, Place, Event)
from modelgenie.archiver import FilebasedTypeArchiver

archiver = FilebasedTypeArchiver()

serialized_type = Person.serialize_type()
saved = archiver.save(Person)

filters = {'type_name': 'Person'}
loaded = archiver.query(filters)



