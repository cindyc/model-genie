import re
import json

CAMEL_PATTERN = re.compile(r'([A-Z])')
UNDERSCORE_PATTERN = re.compile(r'_([a-z])')

class UtilException(Exception):
    """Exception from the util functions
    """
    pass


def _flatten(hkey="", d={}):
    """flattened a nested dict
    """
    items = []
    for key, value in d.items():
        new_key = '.'.join([hkey, key]) if hkey else key
        items.append((new_key, value))
        if type(value) == dict:
            items.extend(_flatten(new_key, value).items())
        elif type(value) == list:
            for i in range(0, len(value)):
                indexed_key = new_key + "".join(["[", str(i), "]"])
                items.extend(_flatten(indexed_key, value[i]).items())

    return dict(items)


def flatten(data):
    """Flat a nested dict or a list of nested dicts
    """
    if type(data) is list:
        return [_flatten(x) for x in data]
    elif type(data) is dict:
        return _flatten(d=data)
    else:
        raise UtilException("Cannot flatten data with type {}".format(type(data)))


def camel_to_underscore(name):
    return CAMEL_PATTERN.sub(lambda x: '_' + x.group(1).lower(), name)

def underscore_to_camel(name):
    return UNDERSCORE_PATTERN.sub(lambda x: x.group(1).upper(), name)

def convert_json(d, convert):
    new_d = {}
    for k, v in d.iteritems():
        new_d[convert(k)] = convert_json(v,convert) if isinstance(v,dict) else v
    return new_d

def json_load(*args, **kwargs):
    json_obj = json.load(*args, **kwargs)
    return convert_json(json_obj, camel_to_underscore)

def json_loads(json_obj):
    print 'type(json_obj) is {}'.format(type(json_obj))
    if type(json_obj) is str:
        json_obj = json.loads(json_obj)
    return convert_json(json_obj, camel_to_underscore)

def json_dump(*args, **kwargs):
    args = (convert_json(args[0], underscore_to_camel),) + args[1:]
    json.dump(*args, **kwargs)

def json_dumps(json_d):
    if type(json_d) is str:
        json_d = json.loads(json_d)
    new_d = convert_json(json_d, underscore_to_camel)
    json.dumps(newd_d)
