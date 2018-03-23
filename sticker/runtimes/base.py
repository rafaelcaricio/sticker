from abc import abstractmethod
from typing import Callable


class BaseAPI:
    @staticmethod
    def read_file_contents(filename: str):
        with open(filename, encoding='utf-8') as file:
            return file.read()

    def wrap_handler(self, bare_function: Callable):
        def _wapper(*args, **kwargs):
            params = self.to_python_literals(*args, **kwargs)
            return self.back_to_framework(bare_function(params))
        return _wapper

    @abstractmethod
    def to_python_literals(self, *args, **kwargs):
        """
        Get flask parameters and build Python literals.

        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def back_to_framework(self, result):
        """
        Returns response values that Flask understand.

        :return:
        """
        raise NotImplementedError

