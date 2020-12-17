from utils.utils import chunker
from itertools import islice, chain
from toolz.curried import map, reduce, pipe, accumulate
from toolz.dicttoolz import merge

import re
import pudb  # noqa

with open("input.txt") as f:
    lines = map(lambda line: line.strip(), f.readlines())


def process_rule(rule):
    match = re.match("([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)", rule)  # noqa
    field, r1_start, r1_stop, r2_start, r2_stop = match.groups()
    return {
        field: (
            range(int(r1_start), int(r1_stop) + 1),
            range(int(r2_start), int(r2_stop) + 1),
        )
    }


def get_all_valid_ranges(rules):
    return chain.from_iterable(rules.values())


def process_my_ticket(ticket):
    print(ticket)


def process_nearby_ticket(valid_ranges, ticket):
    def is_invalid(value):
        return not any(map(lambda r: value in r, valid_ranges))

    return pipe(
        [0] + ticket.split(","),
        map(int),
        reduce(lambda acc, value: acc + value if is_invalid(value) else acc),
    )


chunks = chunker(lines)
rules = pipe(
    next(chunks),
    map(lambda rule: process_rule(rule)),
    reduce(lambda acc, d: merge(acc, d)),
)
all_valid_ranges = list(get_all_valid_ranges(rules))
my_ticket = process_my_ticket(next(chunks))
nearby_ticket_errors = pipe(
    islice(next(chunks), 1, None),
    map(lambda ticket: process_nearby_ticket(all_valid_ranges, ticket)),
    sum,
)
print(nearby_ticket_errors)
