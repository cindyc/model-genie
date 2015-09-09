from flask import Flask,request
from flask.ext import restful
from flask_cors import CORS

from modelgenie.genie import ModelGenie

from common.util import json_loads, json_dumps

app = Flask(__name__)
cors = CORS(app, allow_headers=['Content-Type'])

api = restful.Api(app)


class ModelDefinitionListApi(restful.Resource):
    """APIs for list of entity definitions
    """

    def get(self):
        """GET list of entity definitions
        """
        return ModelGenie.list("ModelDefinition")

    def post(self):
        """Create a new entity definition
        """
        print 'EntityDefinitionListApi: POST: request.json is {}'.format(request.json)
        data = request.json
        entity_def = EntityDefinition(**data)
        print 'entity_def is {}'.format(entity_def)
        return ModelGenie.save_definition(entity_def)


class EntityDefinitionApi(restful.Resource):

    def get(self, id):
        """GET an entity definition by id or list of entity definitions
        """
        print 'EntityDefinition:GET: id={}'.format(id)
        return ModelGenie.get_definition(id)

api.add_resource(EntityDefinitionApi, '/entitydefs/<id>')
api.add_resource(EntityDefinitionListApi, '/entitydefs')


class EntityCreateApi(restful.Resource):

    def get(self, definition_id):
        """Initialize an entity based on definition id
        """
        print 'EntityCreateApi:GET: definition={}'.format(definition_id)
        definition = ModelGenie.get_definition(entitydef_id)
        print 'definition is {}'.format(definition)
        model = ModelGenie.create_model(definition)
        return model


class EntityListApi(restful.Resource):

    def post(self):
        """Saved an entity
        """
        print 'EntityListApi:POST: request.json is {}'.format(request.json)
        entity = request.json["entity"]
        entity_def = request.json["entity_def"]
        entity["entity_definition"] = {"_id": entity_def["_id"]}
        saved = ModelGenie.save(entity)
        print 'saved is {}'.format(saved)
        return saved

    def get(self):
        """Get a list of entities
        """
        print "EntitiesApi:GET: request.args={}".format(request.args)
        definition_id = request.args.get("entitydefId")
        print "definition_id is {}".format(definition_id)
        entities = ModelGenie.list_by_definition(definition_id)
        return entities


class EntityApi(restful.Resource):

    def get(self, id):
        """Get an entity by id
        """
        print "EntityApi:GET: id={}".format(id)
        entity = ModelGenie.get(id);
        return entity

    def delete(self, id):
        """DELETE entity
        """
        print "EntityApi:DELETE: id={}".format(id)
        result = ModelGenie.delete(id)
        return result


api.add_resource(EntityCreateApi, '/entities/create/<entitydef_id>')
api.add_resource(EntityApi, '/entities/<id>')
api.add_resource(EntityListApi, '/entities')


class ConnectorsApi(restful.Resource):
    _db = MongoDbProvider(host, port, db_name, "Connector")

    def get(self):
        """List all connectors
        """
        return {"result": self._db.list()}

    def post(self):
        """Save a Connector
        """
        data = request.json
        print "ConnectorApi:POST: data is {}".format(data)
        # TODO(cc): fix this: should support generic Connector
        connector = JsonConnector(**data)
        result = self._db.save(connector)
        return {"result": result}

class ConnectorApi(restful.Resource):
    _db = MongoDbProvider(host, port, db_name, "Connector")

    def get(self, id):
        """Get a Connector
        """
        result = self._db.get(id, "Connector")
        return result

    def post(self, id):
        """Execute a Connector
        """
        print 'request.json is {}'.format(request.json)
        if request.json["action"] == "list": 
            model_name = request.json["entitydefName"]
            data = self._db.get(id, "Connector")
            # TODO (cc) fix this, move all these to a seperate module
            connector = JsonConnector()
            datasource_data = self._db.get(data["datasource"]["_id"], "DataSource")
            connector.datasource = JsonDataSource(**datasource_data) 
            definitions = {}
            for (model_name, definition) in data["definitions"].iteritems():
                definition_data = self._db.get(definition["_id"], "EntityDefinition")
                print "definition_data is {}".format(definition_data)
                entity_definition = EntityDefinition(**definition_data)
                #entity_definition.init(**definition_data)
                print "**** entity_definitiion._id = {}".format(entity_definition._id)
                definitions[model_name] = entity_definition
            connector.definitions = definitions
            # TODO (cc) really bad, get camelcase<->cform conversion working
            for (model_name, mapping) in data["mappings"].iteritems():
                if "resourcePath" in mapping:
                    resource_path = mapping["resourcePath"]
                    data["mappings"][model_name]["resource_path"] = resource_path
            connector.mappings = data["mappings"]
            entity_objs = connector.list(model_name)
            entities = []
            for entity_obj in entity_objs:
                properties = entity_obj.serialize()
                entity_definition = definitions[model_name].serialize();
                entity = {"entity_definition": entity_definition,
                          "_id": "",
                          "name": entity_definition["name"],
                          "properties": properties
                }
                entities.append(entity)
            return {"entities": entities}
        else:
            return ("Unsupported operation for POST",)


api.add_resource(ConnectorsApi, '/connectors')
api.add_resource(ConnectorApi, '/connectors/<id>')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
