import uuid
import os
import json
import glob
import inspect

ID = 'id'


class DbConfig(object):
    data_dir = os.path.join(os.path.abspath('.'), 'modelgenie', 'data')

class TypeArchiverException(Exception):
    pass

class TypeArchiver(object):
    pass

class ArchiverEncoder(json.JSONEncoder):

    def default(self, obj):
        if self._is_type:
            print 'obj is type {}'.format(obj)
            return self._encode_type(obj)
        elif isinstance(obj, dict):
            return self._encode_dict(obj)
        elif isinstance(obj, list):
            return self._encode_list(obj)
        return json.JSONEncoder.default(self, obj)

    def _is_type(self, data):
        type_classes = inspect.getmembers(schematics.types, inspect.isclass)
        class_name = type(data).__name__
        is_type = class_name in [classname for (classname, fullname) in type_classes] 
        return is_type

    def _encode_type(self, data):
        encoded = '.'.join([inspect.getmodule(data).__name__ , type(data).__name__])
        print 'encode_type(), encoded={}'.format(encoded)
        return encoded

    def _encode_list(self, data):
        rv = []
        for item in data:
            if isinstance(item, unicode):
                item = item.encode('utf-8')
            if self._is_type(item):
                item = self._encode_type(item)
            elif isinstance(item, list):
                item = self._encode_list(item)
            elif isinstance(item, dict):
                item = self._encode_dict(item)
            rv.append(item)
        return rv

    def _encode_dict(self, data):
        rv = {}
        for key, value in data.iteritems():
            if self._is_type(key):
                key = self._encode_type(key)
            if self._is_type(value):
                value = self._encode_type(value)
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = self._encode_list(value)
            elif isinstance(value, dict):
                value = self._encode_dict(value)
            rv[key] = value
        return rv

class FilebasedTypeArchiver(TypeArchiver):

    def __init__(self):
        self.data_dir = DbConfig.data_dir

    def save(self, model):
        """Save an obj
        """
        data = model.serialize_type()
        existed = self.query(filters={'type_name': data['type_name']})
        print 'existed = {}'.format(existed)
        if existed:
            data[ID] = existed[0][ID]
        elif ID not in data or data[ID] is None:
            data[ID] = str(uuid.uuid4())
        print 'data is {}'.format(data)
        json_str = json.dumps(data, indent=4, cls=ArchiverEncoder)
        json_filename = '{}.{}.json'.format(data['type_name'], data[ID])
        with open(os.path.join(self.data_dir, json_filename), 'w') as json_file:
            json_file.write(json_str)
        return data

    def query(self, filters=None): 
        """Get a persisted object by id
        """
        if not filters:
            fn_filter = '*.json'
        elif 'id' in filters:
            fn_filter = '*.{}.json'.format(filters['id'])
        elif 'type_name' in filters: 
            fn_filter = '{}.*.json'.format(filters['type_name'])
        else:
            raise TypeArchiverException("Query by key {} is not supported".format(key))

        print 'fn_filter is {}'.format(fn_filter)
        json_filenames = glob.glob1(DbConfig.data_dir, fn_filter)
        matched = []
        for json_filename in json_filenames:
            with open(os.path.join(DbConfig.data_dir, json_filename), 'r') as json_file:
                data = json.loads(json_file.read(), object_hook=self._decode_dict)
            matched += (data, )
        return matched

    # TODO (cc) move these to ArchiverDecoder 

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
