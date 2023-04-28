class Storage:
    def __init__(self) -> None:
        self.storage = None

    def get_item(self, key):
        pass

    def save_item(self, value):
        pass


class Cache(Storage):
    def __init__(self):
        self.storage = dict()


    def get_item(self, key):
        return self.storage.get(key)
    

    def save_item(self, key, value):
        self.storage[key] = value