from modelgenie.base import ArchivableModel
from modelgenie.builtins import (Person, Place, Event)
from modelgenie.archiver import FilebasedTypeArchiver


archiver = FilebasedTypeArchiver()

def test_save_and_load():
    serialized_type = Person.serialize_type()
    #saved = archiver.save(Person)
    #archiver.save(Place)
    archiver.save(Event)

    filters = {'type_name': 'Person'}
    loaded = archiver.query(filters)
    return loaded



