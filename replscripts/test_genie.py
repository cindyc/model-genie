from entity.base import ModelGenie, ArchivableModel
from entity.builtins import (Person, Place, Event)
from entity.definitions import (EntityDefinition, PropertyDefinition,
                                TypeDefinition, CollectionDefinition)

event_model_def = EntityDefinition(name='Event', type='Event')

string_type_def = TypeDefinition(is_model=False, type='String')
person_model_def = EntityDefinition(name='Person', type='Person',
                                    property_definitions=[
                                        {"name": 'first_name', "type":'String'},
                                        {"name":'last_name', "type":'String'},
                                    ],
                                  )
model_type_def = TypeDefinition(is_model=True, type='Person',
                                model_def=person_model_def.serialize())

attendees_collection = CollectionDefinition(name='attendees_collection',
                              type='List',
                              allow_type=model_type_def)

attendees_property = PropertyDefinition(name='attendees',
                                  type='Collection',
                                  collection_definition=attendees_collection)
event_model_def.property_definitions.append(attendees_property)


def test_convert_def_to_model():
    model = ModelGenie.get_model(event_model_def)
    return model

def test_create_model():
    model_def = ModelGenie.get_definition(Person)
    model = ModelGenie.get_model(model_def)
    return model

def test_get_definition():
    """Test get_definition()
    """
    model_def = ModelGenie.get_definition(Person)
    return model_def
