import json


class Config:

    def __init__(self, data=None):
        if data is None:
            data = {}
        self.data = data

    def load(self, filename):
        with open(filename) as f:
            self.data = json.load(f)

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=2)

    def __getattr__(self, name):
        try:
            return Config._wrap(self.data[name])
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name in ('filename', 'data'):
            super().__setattr__(name, value)
        else:
            keys = name.split('.')
            obj = self.data
            for key in keys[:-1]:
                if key not in obj:
                    obj[key] = {}
                obj = obj[key]
            obj[keys[-1]] = value

    def __delattr__(self, name):
        keys = name.split('.')
        obj = self.data
        for key in keys[:-1]:
            obj = obj[key]
        del obj[keys[-1]]

    @staticmethod
    def _wrap(value):
        if isinstance(value, dict):
            return Config(value)
        else:
            return value
