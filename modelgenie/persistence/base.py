import os
import uuid
import json

ID = 'id'


class DbConfig(object):
    data_dir = os.path.join(os.path.abspath('.'), 'data')

class PersistenceException(Exception):
    pass


class Persistence(object):

    def to_json(self, obj):
        """Serialize an object with json
        """
        _dict = obj._to_dict()
        if ID not in _dict or _dict[ID] is None:
            _dict[ID] = str(uuid.uuid4())
        json_str = json.dumps(_dict, indent=4)
        return json_str
