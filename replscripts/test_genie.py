from modelgenie.base import SchematicsModelGenie, ArchivableModel
from modelgenie.builtins import (Person, Place, Event)


def test_create_model():
    model_def = SchematicsModelGenie.get_definition(Person)
    model = SchematicsModelGenie.create_model(model_def)
    return model

def test_get_definition():
    """Test get_definition()
    """
    model_def = SchematicsModelGenie.get_definition(Person)
    return model_def
