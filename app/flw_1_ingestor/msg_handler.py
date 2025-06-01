import json
from loguru import logger
from pprint import pformat

class MsgHandler:
    def __init__(self, msg):
        self.msg = msg

    def handle(self):
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass
    
    def __del__(self):
        pass
    
    def __str__(self):
        return pformat(self.msg)
    
    def __repr__(self):
        return pformat(self.msg)
    
    def __len__(self):
        return len(self.msg)
    
    def __getitem__(self, key):
        return self.msg[key]
    
    def __setitem__(self, key, value):
        self.msg[key] = value
    
    def __delitem__(self, key):
        del self.msg[key]
    
    def __iter__(self):
        return iter(self.msg)
    
    def __next__(self):
        return next(self.msg)
    
    def __contains__(self, item):
        return item in self.msg