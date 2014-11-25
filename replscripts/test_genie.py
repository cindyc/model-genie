from modelgenie.base import SchematicsModelGenie, ArchivableModel
from modelgenie.builtins import (Person, Place, Event)
from modelgenie.definitions import (ModelDefinition, FieldDefinition, 
                                    TypeDefinition, CollectionDefinition)

event_model = ModelDefinition(name='Event', type='Event')

string_type_def = TypeDefinition(is_model=False, type='String')
person_model_def = ModelDefinition(name='Person', type='Person',
                                   field_definitions=[
                                        FieldDefinition(name='first_name', type='String'),
                                        FieldDefinition(name='last_name', type='String'),
                                    ],
                                  )
model_type_def = TypeDefinition(is_model=True, type='Person', 
                                model_def=person_model_def.serialize())

attendees_collection = CollectionDefinition(name='attendees_collection',
                              type='List', 
                              allow_type=model_type_def)

attendees_field = FieldDefinition(name='attendees',
                                  type='Collection',
                                  collection_definition=attendees_collection)
event_model.field_definitions.append(attendees_field)


def test_convert_def_to_model():
    model = SchematicsModelGenie.create_model(event_model)
    return model

def test_create_model():
    model_def = SchematicsModelGenie.get_definition(Person)
    model = SchematicsModelGenie.create_model(model_def)
    return model

def test_get_definition():
    """Test get_definition()
    """
    model_def = SchematicsModelGenie.get_definition(Person)
    return model_def
