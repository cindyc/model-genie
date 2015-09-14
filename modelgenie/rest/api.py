from flask import Flask,request
from flask.ext import restful
from flask_cors import CORS

from modelgenie.genie import ModelGenie

from modelgenie.common.util import json_loads, json_dumps

app = Flask(__name__)
cors = CORS(app, allow_headers=['Content-Type'])

api = restful.Api(app)


class ModelDefinitionsApi(restful.Resource):
    """APIs for list of model definitions
    """

    def get(self):
        """GET list of model definitions
        """
        return ModelGenie.list("ModelDefinition")

    def post(self):
        """Create a new model definition
        """
        data = json_loads(request.get_json(force=True))
        print 'data is {}'.format(data)
        model_def = ModeGenie.create_definition(**data)
        print 'model_def is {}'.format(model_def)
        return ModelGenie.save_definition(model_def)


api.add_resource(ModelDefinitionsApi, '/definitions')


class ModelDefinitionApi(restful.Resource):

    def get(self, id):
        """GET an model definition by id or list of model definitions
        """
        print 'ModelDefinition:GET: id={}'.format(id)
        return ModelGenie.get_definition(id)

api.add_resource(ModelDefinitionApi, '/definitions/<id>')


class ObjectCreateApi(restful.Resource):

    def get(self, definition_id):
        """Initialize an object based on definition id
        """
        print 'ObjectCreateApi:GET: definition={}'.format(definition_id)
        definition = ModelGenie.get_definition(definition_id)
        print 'definition is {}'.format(definition)
        model = ModelGenie.create_model(definition)
        return model()


api.add_resource(ObjectCreateApi, '/objects/create/<definition_id>')


class ObjectListApi(restful.Resource):

    def post(self):
        """Saved an object
        """
        print 'ObjectListApi:POST: request.json is {}'.format(request.json)
        _obj = request.json
        definition = data["definition"]
        _obj["definition"] = {"_id": definition["_id"]}
        saved = ModelGenie.save_object(_obj)
        print 'saved is {}'.format(saved)
        return saved

    def get(self):
        """Get a list of objects
        """
        print "EntitiesApi:GET: request.args={}".format(request.args)
        definition_id = request.args.get("definition")
        print "definition_id is {}".format(definition_id)
        objects = ModelGenie.list_objects(definition_id)
        return objects


api.add_resource(ObjectListApi, '/objects')


class ObjectApi(restful.Resource):

    def get(self, obj_id):
        """Get an object by id
        """
        print "ObjectApi:GET: id={}".format(obj_id)
        _obj = ModelGenie.get_object(id);
        return _obj

    def delete(self, obj_id):
        """DELETE object
        """
        print "ObjectApi:DELETE: id={}".format(obj_id)
        result = ModelGenie.delete_object(obj_id)
        return result


api.add_resource(ObjectApi, '/objects/<id>')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
