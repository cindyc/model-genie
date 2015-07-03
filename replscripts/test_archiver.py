from modelgenie.base import SchematicsModelGenie, ArchivableModel
from modelgenie.builtins import (Person, Place, Event)
from modelgenie.archiver import FilebasedTypeArchiver


archiver = FilebasedTypeArchiver()

def test_create_model():
    model_def = SchematicsModelGenie.get_definition(Person)
    model = SchematicsModelGenie.create_model(model_def)
    return model

def test_get_definition():
    """Test get_definition()
    """
    model_def = SchematicsModelGenie.get_definition(Person)
    return model_def

def test_save_and_load():
    serialized_type = Person.serialize_type()
    #saved = archiver.save(Person)
    #archiver.save(Place)
    archiver.save(Event)

    filters = {'type_name': 'Person'}
    loaded = archiver.query(filters)
    return loaded
