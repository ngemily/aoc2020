from itertools import islice
from utils.utils import two_sum

import pudb  # noqa

TARGET = 2020


with open("input.txt") as f:
    lines = map(lambda s: s.strip(), f.readlines())
    nums = list(map(int, lines))

# 2 sum
x, y = two_sum(list(nums), target=TARGET)
print(x * y)


def slicer(iterable):
    for i in range(len(iterable)):
        yield islice(iterable, i, None)


# 3 sum
# [9], [43, 1, 34, 90, 8]
# ., [43], [1, 34, 90, 8]
# ....., [1], [34, 90, 8]
# ........, [34], [90, 8]
# ...
it = zip(
    nums,
    map(
        lambda it: two_sum(it, target=TARGET - next(it)),
        slicer(nums),
    ),
)
x, (y, z) = next(filter(lambda t: t[1] is not None, it))
print(x * y * z)
