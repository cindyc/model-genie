import json

import modelgenie.rest.api as rest_api
from replscripts.common import PERSON_MODEL_DATA


test_client = rest_api.app.test_client()


def post_create_definition(data=PERSON_MODEL_DATA):
    return test_client.post('/definitions',
                            headers={'content_type':'application/json'},
                            data=json.dumps(data))
