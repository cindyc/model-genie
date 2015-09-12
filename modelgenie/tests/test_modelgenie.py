from modelgenie.genie import ModelGenie
from modelgenie.definitions import (PropertyDefinition, ModelDefinition)

import pytest

class TestModelGenie(object):

    @pytest.fixture
    def model_def(self): 
        prop_def1 = PropertyDefinition(name='first_name', type='String')
        prop_def2 = PropertyDefinition(name='age', type='Int')
        _model_def = ModelDefinition(name='Person', type='Person')
        _model_def.property_definitions = (prop_def1, prop_def2)
        return _model_def

    def test_create_model_from_definition(self, model_def):
        """Test converting model_definition to model_impl
        """
        #prop_def1 = PropertyDefinition(name='first_name', type='String')
        #prop_def2 = PropertyDefinition(name='age', type='Int')
        #model_def = ModelDefinition(name='Person', type='Person')
        #model_def.property_definitions = (prop_def1, prop_def2)
        model = ModelGenie.create_model(model_def)
        assert model is not None

    def test_serialize_model_definition(self, model_def): 
        """Test serializing a model instance
        """
        model_instance = ModelGenie.create_instance(model_def)
        assert model_instance is not None
