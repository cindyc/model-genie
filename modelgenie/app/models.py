from modelgenie.base import ModelGenie
from modelgenie.definitions import (ModelDefinition, FieldDefinition, 
                                    TypeDefinition, ListTypeDefinition,
                                    ModelTypeDefinition, CollectionDefinition,
                                   )


location_def = ModelDefinition(name='Location', type='Location',
                    field_definitions=[
                        FieldDefinition(name='street', type='String'),
                        FieldDefinition(name='city', type='String'),
                        FieldDefinition(name='state', type='String'),
                        FieldDefinition(name='country', type='String'),
                ])

daytime_range_def = ModelDefinition(name='DayTimeRange', type='DayTimeRange',
                    field_definitions=[
                        FieldDefinition(name='weekday', type='String'),
                        FieldDefinition(name='begin_hour', type='Time'),
                        FieldDefinition(name='end_hour', type='Time'),
                ])

admission_def = ModelDefinition(name='Admission', type='Admission',
                    field_definitions=[
                        FieldDefinition(name='category', type='String'),
                        FieldDefinition(name='price', type='Int'),
                ])

attraction_def = ModelDefinition(name='Attraction', type='Attraction',
                    field_definitions=[
                        FieldDefinition(name='address', 
                                        type='Model',
                                        compound_type=location_def._to_model_type(),
                                        ),
                        FieldDefinition(name='category', 
                                        type='String'),
                        FieldDefinition(name='hours', type='List', 
                                        compound_type=daytime_range_def._to_list_type(),
                                        ),
                        FieldDefinition(name='admission', type='List',
                                        compound_type=admission_def._to_list_type(),
                                        ),
                ])

d1 = attraction_def
m1 = ModelGenie.get_model(d1)
d2 = ModelGenie.get_definition(m1)
m2 = ModelGenie.get_model(d2)
d3 = ModelGenie.get_definition(m2)
