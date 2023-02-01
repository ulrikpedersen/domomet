from abc import ABCMeta, abstractmethod


class Publisher(metaclass=ABCMeta):
    @abstractmethod
    def start_collecting(self) -> None:
        pass

    @abstractmethod
    def stop_collecting(self) -> None:
        pass

    @abstractmethod
    def get_reading(self, timeout: float = 5 * 60.0) -> dict:
        pass
