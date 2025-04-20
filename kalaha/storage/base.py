from abc import ABC, abstractmethod


class BaseStorageModel(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError()
