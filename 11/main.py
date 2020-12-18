from collections import namedtuple
from itertools import chain, product
from toolz.curried import reduce, map, pipe
from operator import add
from pyrsistent import pvector
from utils.utils import print_2d_array

import pudb  # noqa

with open("input.txt") as f:
    lines = f.readlines()

EMPTY_SEAT = "L"
OCCUPIED_SEAT = "#"


class Point(namedtuple("Point", ["x", "y"])):
    def neighbours(self):
        for p in product(range(self.x - 1, self.x + 2), range(self.y - 1, self.y + 2)):
            if p != self:
                yield Point(*p)


seats = pvector(map(lambda line: pvector(line.strip()), lines))


def is_occupied(seat):
    return seat == OCCUPIED_SEAT


def is_empty(seat):
    return seat == EMPTY_SEAT


def get_occupied_adjacent_seats(seats, i, j):
    """ Return number of occupied seats adajacent to seat[i][j] """
    occupied = 0
    for coord in Point(i, j).neighbours():
        try:
            if coord.x >= 0 and coord.y >= 0:
                occupied += is_occupied(seats[coord.x][coord.y])
        except IndexError:
            pass
    return occupied


def update_seats(seats):
    """ Update seats according to rules, returning new seat grid """

    # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    # Otherwise, the seat's state does not change.

    new_seats = seats
    for i, row in enumerate(seats):
        for j, seat in enumerate(row):
            num_occupied = get_occupied_adjacent_seats(seats, i, j)
            if is_empty(seat):
                if num_occupied == 0:
                    # seat becomes occupied
                    new_seats = new_seats.set(i, new_seats[i].set(j, OCCUPIED_SEAT))
            elif is_occupied(seat):
                if num_occupied >= 4:
                    # seat becomes empty
                    new_seats = new_seats.set(i, new_seats[i].set(j, EMPTY_SEAT))

    return new_seats


def count_occupied_seats(seats):
    return pipe(chain(*seats), map(is_occupied), reduce(add))


while True:
    new_seats = update_seats(seats)
    if new_seats == seats:
        occupied_seats = count_occupied_seats(new_seats)
        print(occupied_seats)
        break
    seats = new_seats
