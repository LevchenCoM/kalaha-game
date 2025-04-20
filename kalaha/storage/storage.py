from typing import Any
from kalaha.storage.errors import DoesNotExist, NotUnique
from kalaha.utils import Singleton


__all__ = ("Storage",)


class Storage(Singleton):
    """
    Simple In-memory storage implementation.
    """
    def __init__(self):
        if not hasattr(self, "_storage_map"):
            self._storage_map = dict()

    def store(self, key: str, value: Any):
        self._storage_map[key] = value

    def append(self, key: str, value: Any):
        try:
            duplicate = self.get_by_id(key, value.id)
        except DoesNotExist:
            duplicate = None

        if duplicate:
            raise NotUnique("Object with id {id} already exists.")

        stored_array = self._storage_map.get(key)

        if stored_array is None:
            stored_array = [value]
            self.store(key, stored_array)
        else:
            self._storage_map[key].append(value)

    def get(self, key: str):
        if key in self._storage_map:
            return self._storage_map[key]

        raise DoesNotExist(f"Key {key} does not exist in storage.")

    def get_last(self, key: str):
        if key in self._storage_map:
            array = self._storage_map[key]
            if len(array):
                return self._storage_map[key][-1]
            else:
                return None

        raise DoesNotExist(f"Key {key} does not exist in storage.")

    def get_by_id(self, key: str, id: int):
        objects = self.get(key)
        filtered = [o for o in objects if o.id == id]
        obj = filtered[0] if filtered else None

        if obj is not None:
            return obj

        raise DoesNotExist(f"Object with id {id} is not found for key {key}")

    def clear(self):
        self._storage_map.clear()
