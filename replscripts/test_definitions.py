from modelgenie.definitions import (FieldDefinition, ModelDefinition,
                                    CollectionDefinition)

firstname_def = FieldDefinition(name='first_name', type='String')
age_def = FieldDefinition(name='age', type='Int')
person_def = ModelDefinition(name='Person', type='Person')
person_def.field_definitions = (age_def, firstname_def)

person_def.bases = ['base_model1', 'base_model2']
