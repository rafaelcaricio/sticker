from typing import Dict, List, Any, Callable, Optional
import yaml
import importlib


class SpecOperation:
    def __init__(self, method_type: str, definition: Dict[str, Any]):
        self.method_type = method_type
        self.definition = definition

    def http_method(self) -> str:
        return self.method_type.upper()

    def function_fullpath(self) -> Optional[str]:
        return self.definition.get('operationId')

    def resolve_function(self) -> Callable:
        module, func = self.function_fullpath().rsplit('.', 1)
        return getattr(importlib.import_module(module), func)


class SpecPath:
    def __init__(self, path: str, definition: Dict[str, dict]):
        self.path = path
        self.definition = definition

    def url_path(self) -> str:
        return self.path

    def operations(self) -> List[SpecOperation]:
        available_operations: List[SpecOperation] = []
        for method_type, op_def in self.definition.items():
            available_operations.append(SpecOperation(method_type, op_def))
        return available_operations


class OpenAPISpec:
    def __init__(self, spec_text: str):
        self.definition = yaml.safe_load(spec_text)

    def paths(self) -> List[SpecPath]:
        available_paths: List[SpecPath] = []
        for url_path, path_def in self.definition.get('paths', {}).items():
            available_paths.append(SpecPath(path=url_path, definition=path_def))
        return available_paths
