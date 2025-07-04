from typing import Type, TypeVar


T = TypeVar("T")

def static_singleton(cls: Type[T]) -> T:
    return cls()