from typing import Any, Dict, List, Optional


def assert_status_code(response_status_code: int, expected_status_code: int) -> None:
    """
    Raise AssertionError if status codes differ.

    Args:
        response_status_code: Actual status code.
        expected_status_code: Expected status code.
    """
    if response_status_code != expected_status_code:
        raise AssertionError(
            f"Status code {response_status_code}. Expected {expected_status_code}"
        )


def _get_dict_diff(d1: Dict[Any, Any], d2: Dict[Any, Any], parent_key: str = "") -> str:
    """
    Return string diff between two dicts.

    Args:
        d1: First dictionary.
        d2: Second dictionary.
        parent_key: Key path for nested dicts.
    """
    text = []
    parent_key = "[%s]" % parent_key.strip("[]") if parent_key else ""
    not_in_second = set(d1.keys()).difference(d2.keys())
    not_in_first = set(d2.keys()).difference(d1.keys())
    if not_in_first:
        text.append(f"Not in first dict: {list(not_in_first)!r}")
    if not_in_second:
        text.append(f"Not in second dict: {list(not_in_second)!r}")
    for key in sorted(set(d1.keys()).intersection(d2.keys())):
        if d1[key] != d2[key]:
            if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                res = _get_dict_diff(d1[key], d2[key], parent_key + f"[{key}]")
                if res:
                    text.append(
                        parent_key + f"[{key}]:\n  " + "\n  ".join(res.splitlines())
                    )
            elif isinstance(d1[key], list) and isinstance(d2[key], list):
                list_diff = _get_list_diff(d1[key], d2[key])
                if list_diff:
                    text.append(
                        f"{parent_key if parent_key else ''}[{key}]:\n{list_diff}"
                    )
            else:
                d1_value = d1[key]
                d2_value = d2[key]
                if type(d1_value) is not type(d2_value):
                    d1_value = repr(d1_value)
                    d2_value = repr(d2_value)

                text.append(
                    f"{parent_key if parent_key else ''}[{key}]: {d1_value} != {d2_value}"
                )
    res = "\n".join(text)
    return res


def _get_list_diff(l1: List[Any], l2: List[Any]) -> str:
    """
    Return string diff between two lists.

    Args:
        l1: First list.
        l2: Second list.
    """
    errors = []
    for i in range(max(len(l1), len(l2))):
        if i >= len(l1):
            errors.append(f"[line {i}]: Not in first list")
            continue
        if i >= len(l2):
            errors.append(f"[line {i}]: Not in second list")
            continue

        l1_value = l1[i]
        l2_value = l2[i]
        if l1_value == l2_value:
            continue

        if isinstance(l1_value, dict) and isinstance(l2_value, dict):
            dict_diff = _get_dict_diff(l1_value, l2_value)
            if dict_diff:
                errors.append(f"[line {i}]: {dict_diff}")
        elif isinstance(l1_value, list) and isinstance(l2_value, list):
            list_diff = _get_list_diff(l1_value, l2_value)
            if list_diff:
                errors.append(f"[line {i}]: {list_diff}")
        else:
            if type(l1_value) is not type(l2_value):
                l1_value = repr(l1_value)
                l2_value = repr(l2_value)
            errors.append(f"[line {i}]: {l1_value} != {l2_value}")

    res = "\n".join(errors)
    return res


def assert_dict_equal(d1: Any, d2: Any, msg: Optional[str] = None) -> None:
    """
    Assert two dicts are equal.

    Args:
        d1: First dictionary.
        d2: Second dictionary.
        msg: Optional message prefix.
    """
    if not isinstance(d1, dict):
        raise AssertionError("First argument is not a dictionary")
    if not isinstance(d2, dict):
        raise AssertionError("Second argument is not a dictionary")

    msg = msg + ":\n" if msg else ""

    if d1 != d2:
        diff = _get_dict_diff(d1, d2)
        if diff:
            raise AssertionError(diff)


def assert_list_equal(l1: Any, l2: Any, msg: Optional[str] = None) -> None:
    """
    Assert two lists are equal.

    Args:
        l1: First list.
        l2: Second list.
        msg: Optional message prefix.
    """
    if not isinstance(l1, list):
        raise AssertionError("First argument is not a list")
    if not isinstance(l2, list):
        raise AssertionError("Second argument is not a list")

    msg = msg + ":\n" if msg else ""

    if l1 != l2:
        diff = _get_list_diff(l1, l2)
        if diff:
            raise AssertionError(diff)
