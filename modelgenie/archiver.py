import uuid
import os
import json
import glob

ID = 'id'


class DbConfig(object):
    data_dir = os.path.join(os.path.abspath('.'), 'modelgenie', 'data')

class TypeArchiverException(Exception):
    pass

class TypeArchiver(object):
    pass


class FilebasedTypeArchiver(TypeArchiver):

    def __init__(self):
        self.data_dir = DbConfig.data_dir

    def save(self, model):
        """Save an obj
        """
        data = model.serialize_type()
        if ID not in data or data[ID] is None:
            data[ID] = str(uuid.uuid4())
        print 'data is {}'.format(data)
        json_str = json.dumps(data, indent=4)
        json_filename = '{}.{}.json'.format(data['type_name'], data[ID])
        with open(os.path.join(self.data_dir, json_filename), 'w') as json_file:
            json_file.write(json_str)
        return data

    def query(self, filters): 
        """Get a persisted object by id
        """
        if 'type_name' not in filters: 
            raise TypeArchiverException("Query by key {} is not supported".format(key))
        type_name = filters['type_name']

        fn_filter = '{}.*.json'.format(type_name)
        print 'fn_filter is {}'.format(fn_filter)
        json_files = glob.glob1(DbConfig.data_dir, fn_filter)
        if not json_files:
            raise TypeArchiverException("No Json file found")
        with open(os.path.join(DbConfig.data_dir, json_files[0]), 'r') as json_file:
            #_dict = json.loads(json_file.read(), object_hook=self._decode_dict)
            data = json.loads(json_file.read(), object_hook=self._decode_dict)
            print 'data is {}'.format(data)
        return data

    def _decode_list(self, data):
        rv = []
        for item in data:
            if isinstance(item, unicode):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = self._decode_list(item)
            elif isinstance(item, dict):
                item = self._decode_dict(item)
            rv.append(item)
        return rv

    def _decode_dict(self, data):
        rv = {}
        for key, value in data.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = self._decode_list(value)
            elif isinstance(value, dict):
                value = self._decode_dict(value)
            rv[key] = value
        return rv
