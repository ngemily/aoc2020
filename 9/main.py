from collections import deque
from more_itertools import windowed
from utils.utils import two_sum

import pudb  # noqa

WINDOW_SIZE = 5

with open("input.txt") as f:
    lines = f.readlines()


class RunningSumDeque(deque):
    """Keeps a running sum of elements in the deque"""

    def __init__(self, target):
        self.__sum = 0
        self.__target = target

    def check_running_sum(self, num):
        """Returns true if inserting 'num' makes the sum of all numbers equal
        to self.target"""
        self.append(num)
        while self.__sum > self.__target:
            self.popleft()
        return self.__sum == self.__target

    def popleft(self):
        popped = super(RunningSumDeque, self).popleft()
        self.__sum -= popped
        return popped

    def append(self, num):
        super(RunningSumDeque, self).append(num)
        self.__sum += num


def find_first_invalid_num(nums, n=2):
    """Return the first number that is not the sum of any two of the previous N
    numbers
    """
    for window in windowed(nums, n + 1):
        number_pool = list(window)
        target = number_pool.pop()
        result = two_sum(number_pool, target)
        if result is None:
            return target


nums = map(lambda s: int(s.strip()), lines)
target = find_first_invalid_num(nums, WINDOW_SIZE)
print(target)

nums = map(lambda s: int(s.strip()), lines)
window = RunningSumDeque(target)

while not window.check_running_sum(next(nums)):
    pass
print(min(window) + max(window))


running_sum = 0
for num in nums:
    window.append(num)
    running_sum += num
    if running_sum == target:
        print("found target")
        print(max(window), min(window))
    elif running_sum > target:
        while running_sum > target:
            first = window.popleft()
            running_sum -= first
            if running_sum == target:
                print("found target")
                print(max(window), min(window))
    # need to check running_sum after each modification of target
