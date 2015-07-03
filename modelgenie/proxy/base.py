import importlib
import inspect
from entity.definitions import EntityDefinition, PropertyDefinition


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
        """Extract EntityDefinition from a Schematics Model
        """
        entity_def = EntityDefinition(name=model.__name__, type=model.__name__)
        for field_name, field_type in model._fields.iteritems():
            # get the schematics field type and convert to our field type
            field_type_data = field_type.__dict__
            _type, _compound_type = cls._to_type_def(field_type)
            property_def = PropertyDefinition(name=field_name,
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
                    setattr(property_def, def_name, field_value)
            entity_def.property_definitions.append(property_def)
        return entity_def


    @classmethod
    def get_model(cls, entity_def):
        """Create a Model based on EntityDefinition
        """
        # entity_def can be passed in as EntityDefinition or dict
        if isinstance(entity_def, EntityDefinition):
            entity_def = entity_def.serialize()

        cls_attrs = {}
        for property_def in entity_def['property_definitions']:
            property_name = property_def['name']
            field_impl = cls._to_field_impl(property_def)
            cls_attrs[property_name] = field_impl
        # TODO(cc) fix this hack transform unicode to str
        class_name = str(entity_def['name'])
        klass = type(class_name, (cls._Model, ), cls_attrs)
        return klass

    @classmethod
    def create_model(cls, entity_def):
        """Create a model with embedded entity_definition
        """
        if isinstance(entity_def, EntityDefinition):
            entity_def = entity_def.serialize()
        entity = cls.get_model(entity_def)().serialize()
        entity["entity_definition"] = entity_def
        return entity


    @classmethod
    def _to_field_impl(cls, field_def):
        """Given a PropertyDefinition, convert to to a impl specific Field
        """
        if isinstance(field_def, PropertyDefinition):
            field_def = field_def.serialize()

        field = cls._to_type_impl(field_def)

        for def_key, value in field_def.iteritems():
            if def_key not in ('name', 'type', 'compound_type', '_id'):
                impl_key = cls.field_def_key_mapping[def_key]
                setattr(field, impl_key, value)
        return field


    @classmethod
    def _to_type_def(cls, field):
        """Given a impl field, return a ModelGenie PropertyDefinition
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
            return (field_type_def, {'entity_def': field_type_def})

    @classmethod
    def _to_compound_type_def(cls, field):
        """Give a compound schematics field type, return a EntityDefinition
        """
        field_type = field.__class__.__name__
        if field_type == 'ModelType':
            model_class = field.model_class
            entity_def = cls.get_definition(model_class)
            return entity_def._to_model_type()
        elif field_type == 'ListType':
            model_class = field.field.model_class
            entity_def = cls.get_definition(model_class)
            return entity_def._to_list_type()
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
            entity_def = field_def['compound_type']['entity_def']
            model_class = cls.get_model(entity_def)
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
