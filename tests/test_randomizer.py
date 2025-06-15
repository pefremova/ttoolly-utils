import re
import pytest
from ttoolly_utils.randomizer import (
    get_random_email_value,
    get_random_domain_value,
    get_randname,
)


def test_get_randname_short_d():
    value = get_randname(5, "d")
    assert len(value) == 5
    assert value.isdigit()


def test_get_randname_long_d():
    value = get_randname(25, "d")
    assert len(value) == 25
    assert value.isdigit()
    assert value[:10] == value[10:20]


def test_get_randname_long_with_chunk_length_d():
    value = get_randname(15, "d", 5)
    assert len(value) == 15
    assert value.isdigit()
    assert value[:5] == value[5:10] == value[10:]


def test_get_randname_short_w():
    value = get_randname(5, "w")
    assert len(value) == 5
    assert re.match(r"[a-zA-Z]{5}", value)


def test_get_randname_long_w():
    value = get_randname(25, "w")
    assert len(value) == 25
    assert re.match(r"([a-zA-Z]{10})\1[a-zA-Z]{5}", value)


def test_get_randname_long_with_chunk_length_w():
    value = get_randname(15, "w", 5)
    assert len(value) == 15
    assert re.match(r"([a-zA-Z]{5})\1\1", value)


def test_get_randname_short_p():
    value = get_randname(5, "p")
    assert len(value) == 5
    assert re.match(r'[\[!"#$%&\'\(\)*+,-./:;<=>?@[\\\]^_`{|}~\]]{5}', value)


def test_get_randname_short_s():
    value = get_randname(5, "s")
    assert len(value) == 5
    assert re.match(r"\s{5}", value)


def test_get_randname_short_custom():
    value = get_randname(5, "-")
    assert value == "-" * 5


def test_get_randname_long_all():
    value = get_randname(25, "a")
    assert len(value) == 25
    assert re.match(r"([\s\S]{10})\1[\s\S]{5}", value, re.MULTILINE)


def test_get_randname_long_with_chunk_length_all():
    value = get_randname(15, "a", 5)
    assert len(value) == 15
    assert re.match(r"([\s\S]{5})\1\1", value, re.MULTILINE)


def test_get_randname_long_all_default():
    value = get_randname(25)
    assert len(value) == 25
    assert re.match(r"([\s\S]{10})\1[\s\S]{5}", value, re.MULTILINE)


@pytest.mark.parametrize("length", [10, 62, 63, 500])
def test_get_random_domain_value(length):
    value = get_random_domain_value(length)
    assert len(value) == length
    assert re.match(
        r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]",
        value,
        re.IGNORECASE,
    )


@pytest.mark.parametrize("length", [3, 10, 254, 255, 256, 500])
def test_get_random_email_value(length):
    value = get_random_email_value(length)
    """https://www.rfc-editor.org/rfc/rfc3696"""
    "https://www.ietf.org/rfc/rfc3696.txt"
    assert len(value) == length
    assert re.match(
        r"(^([a-zA-Z0-9!#$%&\'*+\-/=?^_`{|}~]|(\\ )|(\\)|(\\\")|(\\\()|(\\\))|(\\,)|(\\:)|(\\;)|(\\<)|(\\>)|(\\@)|(\\\[)|(\\\]))(([a-zA-Z0-9!#$%&\'*+\-/=?^_`{|}~.]|(\\ )|(\\)|(\\\")|(\\\()|(\\\))|(\\,)|(\\:)|(\\;)|(\\<)|(\\>)|(\\@)|(\\\[)|(\\\])){0,63})"
        r'|(^"[a-zA-Z0-9!#$%&\'*+\-/=?^_`{|}~.\\(),:;<>@\[\] ]{1,62}"))'
        r"@(((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9])|([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?))",
        value,
    )
    assert ".." not in value
    assert ".@" not in value


def test_get_random_email_value_too_short():
    with pytest.raises(ValueError) as exc_info:
        get_random_email_value(2)
    assert str(exc_info.value) == "Email length cannot be less than 3"
