from typing import Generic, Type, TypeVar
from kalaha.storage.crud.base import BaseCrud

CrudType = TypeVar("CrudType", bound=BaseCrud)


class BaseService(Generic[CrudType]):
    CRUD_CLASS: Type[CrudType]

    def __init__(self):
        self._crud: CrudType = self.CRUD_CLASS.__call__()
