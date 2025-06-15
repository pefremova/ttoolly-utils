import re
import sys
import traceback
from typing import Any, Generator


class continue_on_fail:
    """
    Context manager: collect errors and continue on specified exceptions.

    Args:
        errors: List to collect error messages.
        *title: Optional title for error messages.
        exc_types: Exception types to catch (default: AssertionError).
    """

    def __init__(
        self,
        errors: list[str],
        *title: Any,
        exc_types: tuple[type[BaseException], ...] = (AssertionError,),
    ) -> None:
        self.title = " ".join([str(t) for t in title])
        self.errors = errors
        self.exc_types = exc_types

    def __enter__(self) -> "continue_on_fail":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        traceback: Any,
    ) -> bool | None:
        if exc_type and issubclass(exc_type, self.exc_types):
            self.errors.append(self.title + "\n" + get_error())
            return True


def convert_size_to_bytes(size: int | str) -> int:
    """
    Convert size string to number in bytes.

    Args:
        size: Size as int or string (e.g. '2K', '5M').
    Returns:
        Size in bytes.
    """
    SYMBOLS = ["", "K", "M", "G"]
    size, symbol = re.findall(r"([\d\.]+)(\w?)", str(size))[0]
    size = float(size) * 1024 ** SYMBOLS.index(symbol if symbol in SYMBOLS else "")
    return int(size)


def get_error(tr_limit: int | None = None) -> str:
    """
    Return current exception traceback as string.

    Args:
        tr_limit: Optional traceback limit.
    Returns:
        Traceback string.
    """
    etype, value, tb = sys.exc_info()
    err = ""
    if any([etype, value, tb]):
        err = "".join(
            [
                str(el)
                for el in traceback.format_exception(etype, value, tb, limit=tr_limit)
            ]
        )

    return err


def get_all_subclasses(cls: type) -> Generator[type, None, None]:
    """Yield all subclasses of a class recursively."""
    for subclass in cls.__subclasses__():
        yield from get_all_subclasses(subclass)
        yield subclass
