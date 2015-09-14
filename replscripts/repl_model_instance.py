from modelgenie.genie import ModelGenie
from modelgenie.definitions import (ModelDefinition, PropertyDefinition)
from modelgenie.persistence.mongo import MongoDbProvider

host = 'localhost'
port = 27017
db_name = 'datanarra'
db = MongoDbProvider(host, port, db_name, "ModelDefinition")

#d=db.get(entitydef_id)

md_person = ModelDefinition(name="Person", type="Person")
pd_name = PropertyDefinition(name="Name", type="String")
pd_age = PropertyDefinition(name="Age", type="Int")
md_person.property_definitions = [pd_name, pd_age]


def save_model_definition(): 
    """Test saving a model definition
    """
    saved = ModelGenie.save_model_definition(md_person)
    return saved

def create_model():
    """Create a model instance
    """
    md_id = save_model_definition()["_id"]
    person_model = ModelGenie.create_model(md_person)
    return person_model

def save_model():
    """Save a model
    """
    pass

def update_model():
    """Update a model definition
    """
    pass

def delete_model():
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
