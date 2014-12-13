from modelgenie.base import SchematicsModelGenie, ArchivableModel
from modelgenie.definitions import (ModelDefinition, FieldDefinition, 
                                    TypeDefinition, ListTypeDefinition,
                                    ModelTypeDefinition, CollectionDefinition,
                                    to_model_type, to_list_type)
from schematics.models import ModelType


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
                        FieldDefinition(name='price', type='Number', unit='$'),
                ])

loc_type_def = ModelTypeDefinition(type='LocationType', 
                                   model_def=location_def,
                                  )

hours_type_def = ListTypeDefinition(type='HoursType',
                                    is_ordered=True,
                                    model_def=daytime_range_def,
                                   )
admission_type_def = ModelTypeDefinition(is_model=True, type='Admission',
                                    model_def=admission_def, 
                                   )

attraction_def = ModelDefinition(name='Attraction', type='Attraction',
                    field_definitions=[
                        FieldDefinition(name='address', 
                                        type='Model',
                                        compound_type=to_model_type(location_def),
                                        ),
                        FieldDefinition(name='category', 
                                        type='String'),
                        FieldDefinition(name='hours', type='List', 
                                        compound_type=to_list_type(daytime_range_def),
                                        ),
                        FieldDefinition(name='admission', type='List',
                                        compound_type=to_model_type(admission_def),
                                        ),
                ])
