from bulbs.model import Node
from bulbs.property import String, Integer, DateTime, Dictionary

class CompositeNode(Node):
    element_type = 'CompositeNode'
    _serialized = String()
