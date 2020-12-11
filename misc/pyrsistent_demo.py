""" Pyrsistent demo
"""

from pyrsistent import pvector

import attr


@attr.s(frozen=True)
class Point:
    x = attr.ib()
    y = attr.ib()

    def __attrs_post_init__(self):
        print("ctor", self.x, self.y)


l1 = pvector([Point(0, 1), Point(5, 3), Point(1, 6)])
print(l1)
l2 = l1.set(1, Point(9, 9))  # only one more Point object is created
print(l1)                    # l1 unchanged
print(l2)                    # l2 is same as l1 expect for second element
