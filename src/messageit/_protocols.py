from typing import Any, List, Mapping, Protocol, runtime_checkable


@runtime_checkable
class MessageHandlerProtocol(Protocol):
    """Message Handler"""

    def __call__(self, message: Any) -> Any:
        ...


@runtime_checkable
class ResolverProtocol(Protocol):
    def __call__(self, message: Any) -> List[Any]:
        ...

@runtime_checkable
class KeyFunctionProtocol(Protocol):
    """Function which maps objecto to a key"""
    def __call__(self, object: Any) -> Any: ...

@runtime_checkable
class LoggerProtocol(Protocol):
    def debug(
        msg: object,
        *args: object,
        exc_info: Any = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Mapping[str, object] | None = ...
    ) -> None:
        ...

    def info(
        msg: object,
        *args: object,
        exc_info: Any = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Mapping[str, object] | None = ...
    ) -> None:
        ...

    def warning(
        msg: object,
        *args: object,
        exc_info: Any = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Mapping[str, object] | None = ...
    ) -> None:
        ...

    def exception(
        msg: object,
        *args: object,
        exc_info: Any = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Mapping[str, object] | None = ...
    ) -> None:
        ...

    def error(
        msg: object,
        *args: object,
        exc_info: Any = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Mapping[str, object] | None = ...
    ) -> None:
        ...
