from entity.definitions import (PropertyDefinition, EntityDefinition,)

firstname_def = PropertyDefinition(name='first_name', type='String')
age_def = PropertyDefinition(name='age', type='Int')
person_def = EntityDefinition(name='Person', type='Person')
person_def.property_definitions = (age_def, firstname_def)
