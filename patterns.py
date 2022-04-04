from functools import partial
from typing import Protocol

class Singleton:

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

class SharedState:

    __shared_state__ = {}

    def __new__(cls, *args, **kwargs):
        instance = super(SharedState, cls).__new__(cls, *args, **kwargs)
        instance.__dict__ = cls.__shared_state__
        return instance


class LazyProxy:
    def __init__(self, cls, *args, **kwargs):
        self.__dict__['_cls'] = cls
        self.__dict__['args'] = args
        self.__dict__['kwargs'] = kwargs
        self.__dict__['_object'] = None
    @property
    def value(self):
        if self.__dict__['_object'] is None:
            self.__dict__['_object'] = self.__dict__['_cls'](
                *self.__dict__['args'],
                **self.__dict__['kwargs']
            )
        return self.__dict__['_object']
    def __getattr__(self, key):
        return getattr(self.value, key)
    def __setattr__(self, key, value):
        return setattr(self.value, key, value)
    def __delattr__(self, key):
        return delattr(self.value, key)

class Subscriber(Protocol):
    def __update__(self, message):
        ...

class Publisher:
    def __init__(self):
        self.subscribers = set()
        
    def __register__(self, sub):
        self.subscribers.add(sub)
        
    def __unregister__(self, sub):
        self.subscribers.discard(sub)
        
    def __list_subscribers__(self):
        return self.subscibers()   
        
    def dispatch_message(self, message):
        for subscriber in self.subscribers:
            subscriber.__update__(message)

