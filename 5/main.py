from functools import reduce
from more_itertools import windowed

import pudb  # noqa

NUM_ROWS = 128
NUM_SEATS = 8


def halve_range(r, code):
    """return either the upper half or lower half of a range, given a code"""
    if code in "FL":
        r = range(r.start, r.stop - int(len(r) / 2))
    elif code in "BR":
        r = range(r.start + int(len(r) / 2), r.stop)
    else:
        raise ValueError
    return r


def compute_seat_id(boarding_pass):
    row_code, seat_code = boarding_pass[0:7], boarding_pass[7:]

    row_range = reduce(lambda acc, c: halve_range(acc, c), row_code, range(0, NUM_ROWS))
    assert len(row_range) == 1
    row = row_range.start

    seat_range = reduce(
        lambda acc, c: halve_range(acc, c), seat_code, range(0, NUM_SEATS)
    )
    assert len(seat_range) == 1
    seat = seat_range.start

    return row * 8 + seat


with open("input.txt") as f:
    lines = f.readlines()

boarding_passes = map(lambda s: s.strip(), lines)
seat_ids = map(lambda boarding_pass: compute_seat_id(boarding_pass), boarding_passes)
max_seat_id = reduce(max, seat_ids)
print(max_seat_id)

boarding_passes = map(lambda s: s.strip(), lines)
seat_ids = map(lambda boarding_pass: compute_seat_id(boarding_pass), boarding_passes)
for (x, y) in windowed(sorted(seat_ids), 2):
    if y - x > 1:
        print(y - 1)
        break
