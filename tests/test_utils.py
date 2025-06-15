import pytest
from ttoolly_utils.utils import (
    get_all_subclasses,
    continue_on_fail,
    convert_size_to_bytes,
)


@pytest.mark.parametrize(
    "text,expected",
    [
        (10, 10),
        (36192, 36192),
        ("2K", 1024 * 2),
        ("12M", 1024 * 1024 * 12),
        ("1G", 1024**3),
    ],
)
def test_convert_size_to_bytes(text, expected):
    assert convert_size_to_bytes(text) == expected


def test_continue_on_fail():
    errors = ["Existing error"]
    with continue_on_fail(errors):
        raise AssertionError("test")
    assert len(errors) == 2
    assert """\nAssertionError: test\n""" in errors[1]


def test_continue_on_fail_with_title():
    errors = []
    with continue_on_fail(errors, "Title text"):
        raise AssertionError("test")
    assert len(errors) == 1
    assert """\nAssertionError: test\n""" in errors[0]
    assert errors[0].startswith("Title text\n")


def test_continue_on_fail_with_custom_exception_type():
    errors = []
    with continue_on_fail(errors, exc_types=(ValueError,)):
        raise ValueError("test")
    assert len(errors) == 1
    assert """\nValueError: test\n""" in errors[0]


def test_continue_on_fail_with_custom_exception_type_other_type():
    errors = []
    with pytest.raises(AssertionError):
        with continue_on_fail(errors, exc_types=(ValueError,)):
            raise AssertionError("test")


def test_continue_on_fail_other_type():
    errors = []
    with pytest.raises(ValueError):
        with continue_on_fail(errors):
            raise ValueError("test")


def test_get_all_subclasses():
    class A:
        pass

    class B(A):
        pass

    class C(B):
        pass

    assert set(get_all_subclasses(A)).symmetric_difference([B, C]) == set()
