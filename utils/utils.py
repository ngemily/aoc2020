from collections import namedtuple
from itertools import tee, product

import pudb # noqa


def two_sum(nums, target=0):
    """
    Returns first pair of numbers in `nums` that sum to `target`
    """
    nums1, nums2 = tee(nums)
    complements = list(sorted(map(lambda x: target - x, nums1)))
    try:
        result = next(filter(lambda num: num in complements, nums2))
    except StopIteration:
        return None
    return (result, target - result)


def chunker(col, delim=""):
    """Chunks the items in collection `col` by delimiter `delim`"""
    chunk = []
    for item in col:
        if item == delim:
            yield chunk
            chunk.clear()
        else:
            chunk.append(item)
    yield chunk


def print_2d_array(a):
    for row in a:
        print(row)
    print()


def and_lists(l1, l2):
    """ `and` two lists element-wise """
    return [a and b for a, b in zip(l1, l2)]


class Point2D(namedtuple("Point", ["x", "y"])):
    def neighbors(self):
        for p in product(range(self.x - 1, self.x + 2), range(self.y - 1, self.y + 2)):
            if p != self:
                yield Point2D(*p)


class Point3D(namedtuple("Point", ["x", "y", "z"])):
    def neighbors(self):
        for p in product(
            range(self.x - 1, self.x + 2),
            range(self.y - 1, self.y + 2),
            range(self.z - 1, self.z + 2),
        ):
            if p != self:
                yield Point3D(*p)


class Point4D(namedtuple("Point", ["x", "y", "z", "w"])):
    def neighbors(self):
        for p in product(
            range(self.x - 1, self.x + 2),
            range(self.y - 1, self.y + 2),
            range(self.z - 1, self.z + 2),
            range(self.w - 1, self.w + 2),
        ):
            if p != self:
                yield Point4D(*p)
