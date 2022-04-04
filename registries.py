import uuid
import weakref

# core dict where we store all the registries, I make so we cannot replace the registry once created for safety
registries = {}

class Registry:
    # register to the core registries
    def __init__(self, cls):
        registries[cls] = self
        self.cls = cls # they type of objects being regiistered
        self.objects = weakref.WeakValueDictionary() # weak ref dict to avoud dangling refs

    def add(self, obj):
        if not isinstance(obj, self.cls):
            raise TypeError("Object must be of type %s" % self.cls)
        self.objects[obj.uuid] = obj

    def remove(self, obj):
        if obj.uuid in self.objects:
            del self.objects[obj.uuid]

    def get(self, uuid):
        if uuid in self.objects:
            return self.objects[uuid]
        else:
            return None

    def get_all(self):
        return self.objects.values()

    def get_all_uuids(self):
        return self.objects.keys()

    def __iter__(self):
        return iter(self.objects.values())

    def __len__(self):
        return len(self.objects)

    def __contains__(self, item):
        return item in self.objects.values()

    @classmethod
    def register(cls, to_register):

        registry = cls(to_register)
        to_register.registry = registry

        def wrapper(func):
            def wrapper_new(*args, **kwargs):
                obj = func(*args, **kwargs)
                obj.uuid = str(uuid.uuid4())[:8]
                print(f"\t-> Registering {obj.__class__.__name__} with uuid {obj.uuid} to registry {registry.cls.__name__} registry")
                registry.add(obj)
                return obj
            return wrapper_new
        to_register.__new__ = wrapper(to_register.__new__)
