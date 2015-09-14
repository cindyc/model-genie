from modelgenie.definitions import (ModelDefinition, PropertyDefinition)
from modelgenie.persistence.mongo import MongoDbProvider

ENTITIY_ID = '555fd2ac58a9637083365026'
HOST = 'localhost'
PORT = 27017
DB_NAME = 'datanarra'
DB= MongoDbProvider(HOST, PORT, DB_NAME, "ModelDefinition")

#d=db.get(entitydef_id)

PERSON_MD = ModelDefinition(name="Person", type="Person")
NAME_PD= PropertyDefinition(name="Name", type="String")
AGE_PD = PropertyDefinition(name="Age", type="Int")
PERSON_MD.property_definitions = [NAME_PD, AGE_PD]

PERSON_MODEL_DATA = {
 '_id': None,
 'bases': [],
 'name': 'Person',
 'property_definitions': [{'_id': None,
   'choices': None,
   'compound_type': None,
   'is_required': None,
   'max_size': None,
   'messages': None,
   'min_size': None,
   'name': 'Name',
   'owner_model': None,
   'type': 'String'},
  {'_id': None,
   'choices': None,
   'compound_type': None,
   'is_required': None,
   'max_size': None,
   'messages': None,
   'min_size': None,
   'name': 'Age',
   'owner_model': None,
   'type': 'Int'}],
 'type': 'Person'}
