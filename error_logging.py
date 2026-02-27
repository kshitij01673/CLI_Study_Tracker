import json
import datetime
import inspect
import functools
from typing import Any, Callable, TypeVar, Dict, List, Optional, cast

T = TypeVar('T')

def _safe_serialize(obj: Any) -> Any:
    """Safely serialize objects to JSON-serializable format."""
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    if isinstance(obj, (list, tuple)):
        return [_safe_serialize(item) for item in obj]
    if isinstance(obj, dict):
        return {str(k): _safe_serialize(v) for k, v in obj.items()}
    if hasattr(obj, '__dict__'):
        return _safe_serialize(obj.__dict__)
    return str(obj)

def _create_error_entry(
    func: Callable[..., Any],
    error: Exception,
    args: tuple,
    kwargs: Dict[str, Any]
) -> Dict[str, Any]:
    """Create an error log entry dictionary."""
    try:
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "function": func.__name__,
            "module": func.__module__,
            "args": _safe_serialize(bound_args.arguments),
            "kwargs": _safe_serialize(kwargs),
            "error": str(error),
            "error_type": error.__class__.__name__
        }
    except Exception as e:
        # Fallback if we can't get the signature
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "function": func.__name__,
            "args": _safe_serialize(args),
            "kwargs": _safe_serialize(kwargs),
            "error": str(error),
            "error_type": error.__class__.__name__,
            "logging_error": f"Failed to get function signature: {str(e)}"
        }

def _read_error_logs(log_file: str) -> List[Dict[str, Any]]:
    """Read error logs from file."""
    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
            return logs if isinstance(logs, list) else [logs]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _write_error_logs(log_file: str, logs: List[Dict[str, Any]]) -> None:
    """Write error logs to file."""
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2, default=str)

def error_logging(fx: Optional[Callable[..., T]] = None, *, error_log_file: str = "error_log.json") -> Callable:
    """
    A decorator that logs any exceptions raised by the decorated function.
    
    Args:
        fx: The function to decorate (automatically passed by Python)
        error_log_file: Name of the file to store error logs
    
    Returns:
        The decorated function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_entry = _create_error_entry(func, e, args, kwargs)
                error_logs = _read_error_logs(error_log_file)
                error_logs.append(error_entry)
                _write_error_logs(error_log_file, error_logs)
                return f"{func.__name__} resulted in an error: {str(e)}"
        
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                error_entry = _create_error_entry(func, e, args, kwargs)
                error_logs = _read_error_logs(error_log_file)
                error_logs.append(error_entry)
                _write_error_logs(error_log_file, error_logs)
                print(f"{func.__name__} resulted in an error: {str(e)}")
                return f"{func.__name__} resulted in an error: {str(e)}"
        
        if inspect.iscoroutinefunction(func):
            return cast(Callable[..., T], async_wrapper)
        return cast(Callable[..., T], sync_wrapper)
    
    # Handle both @error_logging and @error_logging() syntax
    if fx is not None:
        return decorator(fx)
    return decorator
