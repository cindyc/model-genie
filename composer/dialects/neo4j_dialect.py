import sys
import json
from bulbs.neo4jserver import Graph, Config, NEO4J_URI
from bulbs.property import String, Integer, DateTime, Dictionary
from bulbs.model import Node, Relationship

sys.path.append('/Users/cindy.cao/proj/type-composer')

from composer.models import CompositeNode


class Dialect(object):
    pass


class DialectException(Exception):
    pass


class Neo4jDialect(Dialect): 
    """Neo4j server dialect
    """
    config = Config(NEO4J_URI, "", "")
    _graph = Graph(config)
    _graph.add_proxy('CompositeNode', CompositeNode)

    @classmethod
    def save(cls, model):
        """
        """
        model_def = model.definition
        field_defs = model_def.field_defintions
        serialized = model.serialized()
        serialized_fields = serialized.pop('_fields')

        model_node = cls._graph.CompositeNode.create(_serialized=serialized)

        for serialized_field in serialized_fields:
            field_node = cls._graph.CompositeNode.create(_serialized=serialized_field)
            print 'field_node is {}'.format(field_node)
            relation = cls._graph.edges.create(model_node, 'has', field_node)
        return model_node

    @classmethod
    def load(cls, node_id):
        """Given a root_node_id, which contains the descriptions
        of what relationships to pull, assemble the parts
        of a model
        """
        composites = {}
        root_node = _graph.CompositeNode.index.lookup(uuid=node_id)
        descriptor = root_node.descriptor
        print 'descriptor is {}'.format(descriptor)
        for relationship in descriptor['relationships']:
            print 'assembling relation: {}'.format(relationship)
            composites[relationship] = cls.get_related(relationship)
        return composites
        
    @classmethod
    def get_related(cls, node_id, relationship_type):
        """Get related vertices
        """
        related = {}
        vertices = g.vertices.get(node_id)
        return related

