from modelgenie.definitions import (PropertyDefinition, EntityDefinition)

class TestModelGenie(object):

    def test_get_model_from_definition(self):
        """Test converting model_definition to model_impl
        """
        prop_def1 = PropertyDefinition(name='first_name', type='String')
        prop_def2 = PropertyDefinition(name='age', type='Int')
        model_def = ModelDefinition(name='Person', type='Person')
        model_def.property_definitions = (prop_def1, prop_def2)
        model = modelgenie.get_model(model_def)
