#standard imports
import os
import glob
import json
import uuid

from modelgenie.persistence.base import (Persistence, PersistenceException,
                                         DbConfig)

ID = 'id'
KIND = 'kind'

class FileBasedPersistence(Persistence):

    def __init__(self):
        self.data_dir = DbConfig.data_dir

    def save(self, obj):
        """Save an obj
        """
        _dict = obj._to_dict()
        print '_dict is {}'.format(_dict)
        json_str = json.dumps(_dict, indent=4)
        json_filename = '{}.{}.json'.format(obj.name, _dict['id'])
        with open(os.path.join(self.data_dir, json_filename), 'w') as json_file:
            json_file.write(json_str)
        return _dict

    def get(self, id): 
        """Get a persisted object by id
        """
        fn_filter = '*.{}.json'.format(id)
        print 'fn_filter is {}'.format(fn_filter)
        json_files = glob.glob1(DbConfig.data_dir, fn_filter)
        if not json_files:
            raise PersistenceException("No Json file found")
        with open(os.path.join(DbConfig.data_dir, json_files[0]), 'r') as json_file:
            _dict = json.loads(json_file.read(), object_hook=self._decode_dict)
        return _dict

    def get_by_metadata(self, metadata):
        """Get a saved object by id
        """
        if not ID in metadata and not KIND in metadata:
            raise PersistenceException("Either id or kind needs to be specified")
        if ID in metadata:
            fn_filter = '*{}.json'.format(metadata[ID])
        else:
            fn_filter = '{}*.json'.format(metadata[KIND])
        json_files = glob.glob1(DbConfig.data_dir, fn_filter)
        if not json_files:
            raise PersistenceException("No json file found")
        with open(os.path.join(DbConfig.data_dir, json_files[0]), 'r') as json_file:
            _dict = json.loads(json_file.read(), object_hook=self._decode_dict)
        return _dict

    # TODO(cc): improve this
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
