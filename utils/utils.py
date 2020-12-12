from itertools import tee

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
