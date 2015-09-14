from modelgenie.genie import ModelGenie
from modelgenie.definitions import (ModelDefinition, PropertyDefinition)
from modelgenie.persistence.mongo import MongoDbProvider

entitydef_id = '555fd2ac58a9637083365026'
host = 'localhost'
port = 27017
db_name = 'datanarra'
db = MongoDbProvider(host, port, db_name, "ModelDefinition")

#d=db.get(entitydef_id)

person_md = ModelDefinition(name="Person", type="Person")
pd_name = PropertyDefinition(name="Name", type="String")
pd_age = PropertyDefinition(name="Age", type="Int")
person_md.property_definitions = [pd_name, pd_age]

PERSON_MODEL_DATA = {
    "name": "Person",
    "property_definitions": [
        {"name": "Person",
         "type": "String",
        },
        {"name": "Age",
         "type": "Int",
        }
    ]
}

def create_model_definition_from_dict(data=PERSON_MODEL_DATA): 
    """Test creating a model definition
    """
    return ModelGenie.create_definition(data)

def save_model_definition():
    """Test saving a model definition
    """
    saved = ModelGenie.save_definition(person_md)
    return saved

def get_model_definition(md_id):
    """Get a model definition by id
    """
    model_md = ModelGenie.get_definition(md_id)
    return model_md

def update_model_definition():
    """Update a model definition
    """
    pass

def delete_model_definition():
    """Delete a model definition
    """
    pass


def fix_properties(data):
    pdefs = data['property_definitions']
    i = 0
    for p in pdefs:
        if p['type'] == 'string':
            p['type'] = 'String'
        if p['type'] == 'number':
            p['type'] = 'Int'
        pdefs[i] = p
        i += 1
    data['properties'] = pdefs
    return data
