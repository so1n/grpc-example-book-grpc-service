from functools import wraps
from typing import Any, Callable


def grpc_client_func_wrapper(*args: Any, **kwargs: Any) -> Callable:

    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def _wrapper(*_args: Any, **_kwargs: Any) -> Any:
            if "metadata" not in _kwargs:
                _kwargs["metadata"] = []
            return func(*_args, **_kwargs)
        return _wrapper
    return wrapper


def auto_load_wrapper_by_stub(stub: Any, wrapper: Callable) -> None:
    for stub_method in dir(stub):
        if stub_method.startswith("__"):
            continue
        grpc_handler: Callable = getattr(stub, stub_method)
        setattr(stub, stub_method, wrapper()(grpc_handler))
