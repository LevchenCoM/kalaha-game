from kalaha.storage.storage import Storage


class BaseCrud:
    def __init__(self):
        self._storage: Storage = Storage()
