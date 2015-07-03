from bulbs.neo4jserver import Graph, Config, NEO4J_URI
from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime
from bulbs.utils import current_datetime

config = Config(NEO4J_URI, "", "")


class CompositeType(Node):
    _type = ""
    _fields = {}
    name = None
    description = None

    @classmethod
    def create(cls, **kwargs):
        """Create an instance for a type
        """
        for key, value in kwargs.iteritems():
            print '{}={}'.format(key, value)
        return model

    def __init__(self, **kwargs):
        """Create an instance of this type
        """
        for key, value in kwargs.iteritems(): 
            print 'key is {}, value is {}'.format(key, value)
            field = getattr(self, key)
            if not field: 
                print 'field {} does not exist'.format(field)
            print 'field is {}'.format(field)

class Person(CompositeType):
    first_name = String()
    last_name = String()

class Location(CompositeType):
    address = String()

class Event(CompositeType):
    attendee = Person()
    venue = Location()

class Has(Relationship):
    label = "has"

class TypeComposer(object):
    """Create composable types
    """

    @classmethod
    def get_model_class(cls, type_name):
        if type_name == 'Person': 
            model_class = Person
        elif type_name == 'Location':
            model_class = Location
        elif type_name == 'Person':
            model_class = Person
        class_attrs = {}
        for k, v in model_class.__dict__.iteritems():
            print 'k={}, v={}'.format(k, v)
            
        model_class = type(type_name, (CompositeType, ), attrs)
        return model_class

def create_event(): 
    person = Person.create(name='James Bond', first_name='James', last_name='Bond')
    location = Location.create(name='Mountain View Performance Art Center', 
                        address='500 Castro St, Mountain View, CA')
    event = Event.create(name='Meetup', attendee=person, venue=location)
    return event

