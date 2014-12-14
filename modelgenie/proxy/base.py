import importlib
import inspect
from modelgenie.definitions import ModelDefinition, FieldDefinition


class Types(object):
    String = 'String'
    Int = 'Int'
    Boolean = 'Boolean'
    Time = 'Time'
    List = 'List'
    Model = 'Model'


class ModelProxy(object):
    """Base class of ModelProxy
    """
    # The subclass will assign this
    _Model = None

    @classmethod
    def get_definition(cls, model):
        """Extract ModelDefinition from a Schematics Model
        """
        model_def = ModelDefinition(name=model.__name__, type=model.__name__)
        for field_name, field_type in model._fields.iteritems():
            # get the schematics field type and convert to our field type
            field_type_data = field_type.__dict__
            _type, _compound_type = cls._to_type_def(field_type)
            field_def = FieldDefinition(name=field_name, 
                                        type=_type, 
                                        compound_type=_compound_type
                                       )
            for def_name, getter_key in cls.field_def_key_mapping.iteritems():
                if getter_key in field_type_data:
                    field_value = field_type_data[getter_key]
                    # temporary hack, owner_model is a class and it's not
                    # serializable
                    if getter_key == 'owner_model':
                        field_value = ''
                    setattr(field_def, def_name, field_value)
            model_def.field_definitions.append(field_def)
        return model_def


    @classmethod
    def get_model(cls, model_def):
        """Create a Model based on ModelDefinition
        """
        # model_def can be passed in as ModelDefinition or dict
        if isinstance(model_def, ModelDefinition):
            model_def = model_def.serialize()

        cls_attrs = {}
        for field_def in model_def['field_definitions']:
            field_impl = cls._to_field_impl(field_def)
            cls_attrs[field_def['name']] = field_impl
        class_name = model_def['name']
        klass = type(class_name, (cls._Model, ), cls_attrs)
        return klass


    @classmethod
    def _to_field_impl(cls, field_def):
        """Given a FieldDefinition, convert to to a impl specific Field
        """
        if isinstance(field_def, FieldDefinition):        
            field_def = field_def.serialize()

        field = cls._to_type_impl(field_def)

        for def_key, value in field_def.iteritems():
            if def_key not in ('name', 'type', 'compound_type'):
                impl_key = cls.field_def_key_mapping[def_key]
                setattr(field, impl_key, value)
        return field


    @classmethod
    def _to_type_def(cls, field):
        """Given a impl field, return a ModelGenie FieldDefinition
        """
        imp_type_name = cls._get_type_name(field)
        # it's unfortunate that field_type_mapping has to be inverted
        inverted_field_type_mapping = dict(zip(cls.field_type_mapping.values(), 
                                          cls.field_type_mapping.keys()))
        if imp_type_name in inverted_field_type_mapping: 
            field_type_def = inverted_field_type_mapping[imp_type_name]
        else:
            raise Exception("imp_type_name {} not in mapping".format(imp_type_name))

        if imp_type_name.split('.')[-1] in ('ListType', 'ModelType'):
            return (field_type_def, cls._to_compound_type_def(field))
        else:
            return (field_type_def, {'model_def': field_type_def})

    @classmethod
    def _to_compound_type_def(cls, field):
        """Give a compound schematics field type, return a ModelDefinition
        """
        field_type = field.__class__.__name__
        if field_type == 'ModelType':
            model_class = field.model_class
            model_def = cls.get_definition(model_class)
            return model_def._to_model_type()
        elif field_type == 'ListType':
            model_class = field.field.model_class
            model_def = cls.get_definition(model_class)
            return model_def._to_list_type()
        else:
            return None

    @classmethod
    def _to_type_impl(cls, field_def):
        """Given a type definition, return a impl type
        """
        if field_def['type'] in ('Model', 'List', 'Collection'):
            return cls._to_compound_type_impl(field_def)
        else:
            return cls._to_base_type_impl(field_def)

    @classmethod
    def _to_base_type_impl(cls, field_def):
        """Given a type definition, turn it into a impl specific type
        """
        if field_def['type'] in cls.field_type_mapping:
            impl_type_name = cls.field_type_mapping[field_def['type']]
        else:
            impl_type_name = field_def['type']
        field_type = cls._load_class(impl_type_name)
        return field_type()

    @classmethod
    def _to_compound_type_impl(cls, field_def):
        """Turn a field_def into a impl specific compound type
        """
        if field_def['type'] == 'Model':
            model_def = field_def['compound_type']['model_def']
            model_class = cls.get_model(model_def)
            model_impl_type_name = cls.field_type_mapping['Model']
            model_impl_type = cls._load_class(model_impl_type_name)
            return model_impl_type(model_class)
        elif field_def['type'] in ('List', 'Collection'):
            return cls._to_collection_type_impl(field_def)

    @classmethod
    def _load_class(cls, class_name):
        """Load a class
        """
        module_name = '.'.join(class_name.split('.')[:-1])
        class_name = class_name.split('.')[-1]
        module = importlib.import_module(module_name)
        klass = getattr(module, class_name)
        return klass

    @classmethod
    def _get_type_name(cls, obj): 
        return '.'.join([inspect.getmodule(obj).__name__, 
                         type(obj).__name__])

    @classmethod
    def _get_class_name(cls, obj):
        return obj.__name__
