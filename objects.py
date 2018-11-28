class Item:
    def __init__(self, id=0, name=None, types=0, cost=0, store=None):
        self.id = id
        self.name = name
        self.types = types
        self.cost = cost
        self.store = store

class Store:
    def __init__(self, id=0, name=None):
        self.id = id
        self.name = name

