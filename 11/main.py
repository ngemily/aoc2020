from itertools import chain
from toolz.curried import reduce, map, pipe
from operator import add
from pyrsistent import pvector
from utils.utils import Point2D

import pudb  # noqa

with open("input.txt") as f:
    lines = f.readlines()

EMPTY_SEAT = "L"
OCCUPIED_SEAT = "#"
FLOOR = "."


seats = pvector(map(lambda line: pvector(line.strip()), lines))


def is_floor(seat):
    return seat == FLOOR


def is_occupied(seat):
    return seat == OCCUPIED_SEAT


def is_empty(seat):
    return seat == EMPTY_SEAT


def get_occupied_adjacent_seats(seats, i, j):
    """ Return number of occupied seats adajacent to seat[i][j] """
    occupied = 0
    for coord in Point2D(i, j).neighbors():
        try:
            if coord.x >= 0 and coord.y >= 0:
                occupied += is_occupied(seats[coord.x][coord.y])
        except IndexError:
            pass
    return occupied


def update_seat(i, j, seat):
    num_occupied = get_occupied_adjacent_seats(seats, i, j)
    if is_empty(seat):
        if num_occupied == 0:
            # seat becomes occupied
            return OCCUPIED_SEAT
        else:
            # seat remains empty
            return seat
    elif is_occupied(seat):
        if num_occupied >= 4:
            # seat becomes empty
            return EMPTY_SEAT
        else:
            # seat remains occupied
            return seat
    elif is_floor(seat):
        return seat
    raise ValueError(i, j, seat)


def update_seats(seats):
    """ Update seats according to rules, returning new seat grid """

    # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    # Otherwise, the seat's state does not change.

    new_seats = seats
    for i, row in enumerate(seats):
        for j, seat in enumerate(row):
            new_seat = update_seat(i, j, seat)
            new_seats = new_seats.set(i, new_seats[i].set(j, new_seat))

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
