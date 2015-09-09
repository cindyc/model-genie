from modelgenie.genie import ModelGenie
from modelgenie.definitions import (PropertyDefinition, ModelDefinition)

prop_def1 = PropertyDefinition(name='first_name', type='String')
prop_def2 = PropertyDefinition(name='age', type='Int')
model_def = ModelDefinition(name='Person', type='Person')
model_def.property_definitions = (prop_def1, prop_def2)

model = ModelGenie.create_model(model_def)
p = model()
p.first_name = 'Cindy'
p.age = 10

model_id = '55ad1e385641af3f371c2f92'
def_id = '55ad1e385641af3f371c2f91'


