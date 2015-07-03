from bulbs.neo4jserver import Graph, Config, NEO4J_URI
from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime
from bulbs.utils import current_datetime


class Person(Node):
    element_type = "person"

    name = String(nullable=False)
    age = Integer()


class Knows(Relationship):
    label = "knows"
    created = DateTime(default=current_datetime, nullable=False)


config = Config(NEO4J_URI, "", "")

vertex_names = ["James", "Julie"]

def create_vertices(names=vertex_names): 
    g = Graph(config)
    for name in names:
        g.vertices.create(name=name)
    return g

def create_models(names=vertex_names):
    g = Graph(config)
    g.add_proxy("people", Person)
    g.add_proxy("knows", Knows)
    for name in names:
        model = g.people.create(name=name)

    return g

