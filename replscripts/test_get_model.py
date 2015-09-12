from modelgenie.genie import ModelGenie
from modelgenie.definitions import (ModelDefinition, PropertyDefinition)
from modelgenie.persistence.mongo import MongoDbProvider

entitydef_id = '555fd2ac58a9637083365026'
host = 'localhost'
port = 27017
db_name = 'datanarra'
db = MongoDbProvider(host, port, db_name, "ModelDefinition")

#d=db.get(entitydef_id)

person_def = ModelDefinition(name="Person", type="Person")
name_def = PropertyDefinition(name="Name", type="String")
age_def = PropertyDefinition(name="Age", type="Int")
person_def.property_definitions = [name_def, age_def]
person_model = ModelGenie.create_model(person_def)


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

def create_model(entity_def=age_def):
    model = ModelGenie.get_model(entity_def)
    return model
