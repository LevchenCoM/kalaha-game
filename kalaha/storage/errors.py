class StorageException(Exception):
    pass


class DoesNotExist(StorageException):
    pass


class NotUnique(StorageException):
    pass
