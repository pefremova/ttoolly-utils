[![codecov](https://codecov.io/github/pefremova/ttoolly-utils/graph/badge.svg?token=DYH9Y5SVH0)](https://codecov.io/github/pefremova/ttoolly-utils)


# ttoolly_utils

# About
ttoolly_utils provides some useful tools for testing

# Getting started

Installation

```
pip install ttoolly-utils
```

# Usage Examples

## 1. Asserts

### assert_status_code

```python
from ttoolly_utils.asserts import assert_status_code

assert_status_code(404, 200)

# Output: AssertionError: Status code 404. Expected 200
```

### assert_dict_equal

```python
from ttoolly_utils.asserts import assert_dict_equal

d1 = {'a': 1, 'b': 2, 'c': 3}
d2 = {'b': 3, 'd': 4, 'c': {'c1': 2}}
assert_dict_equal(d1, d2)

# Output:
AssertionError: Not in first dict: ['d']
Not in second dict: ['a']
[b]: 2 != 3
[c]:
  [c][c1]: 1 != 2

```

### assert_list_equal

```python
from ttoolly_utils.asserts import assert_list_equal

l1 = [1, 2, 3]
l2 = [1, 4, 3]
assert_list_equal(l1, l2)

# Output: AssertionError: [line 1]: 2 != 4
```

---

## 2. Randomizer

### get_randname

```python
from ttoolly_utils.randomizer import get_randname

print(get_randname(8, 'w'))  # e.g. 'aBcDeFgH'
print(get_randname(10, 'd')) # e.g. '1234567890'
print(get_randname(5, 'p'))  # e.g. ';@$..'
print(get_randname(5, 's'))  # e.g. '\x0b\n  \n'
print(get_randname())        # e.g. 'oNC<H%|`^\t
```

### get_random_color

```python
from ttoolly_utils.randomizer import get_random_color

print(get_random_color('rgb'))  # e.g. 'rgb(123, 45, 67)'
print(get_random_color('hex'))  # e.g. '#1a2b3c'
```

### get_random_datetime_value

```python
from ttoolly_utils.randomizer import get_random_datetime_value

print(get_random_datetime_value())  # e.g. '2025-06-15 12:34:56.123456'
```

### get_random_domain_value

```python
from ttoolly_utils.randomizer import get_random_domain_value

print(get_random_domain_value(10))  # e.g. 'tf.vl.PRSh'
```

### get_random_email_value

```python
from ttoolly_utils.randomizer import get_random_email_value

print(get_random_email_value(10))  # e.g. 'ae\\;1@c.xh'
print(get_random_email_value(10, safe=True))  # e.g. '30o@dr.lxr'
```

---

## 3. Utils

### continue_on_fail

```python
from ttoolly_utils.utils import continue_on_fail

errors = []
with continue_on_fail(errors, "Test block"):
    assert 1 == 2, "Numbers do not match"
print(errors)
# Output: ['Test block\nTraceback (most recent call last): ... AssertionError: Numbers do not match']
```

### convert_size_to_bytes

```python
from ttoolly_utils.utils import convert_size_to_bytes

print(convert_size_to_bytes('2K'))  # Output: 2048
print(convert_size_to_bytes('5M'))  # Output: 5242880
```

### get_all_subclasses

```python
from ttoolly_utils.utils import get_all_subclasses

class A: pass
class B(A): pass
class C(B): pass

print(list(get_all_subclasses(A)))  # Output: [<class '__main__.C'>, <class '__main__.B'>]
```
