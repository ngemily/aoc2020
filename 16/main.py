from utils.utils import chunker, and_lists
from itertools import islice, chain
from toolz.curried import map, reduce, pipe, filter
from toolz.dicttoolz import merge, keyfilter, valfilter
from operator import mul

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


def parse_ticket(ticket):
    return list(map(int, ticket.split(",")))


def get_all_valid_ranges(rules):
    return chain.from_iterable(rules.values())


def process_my_ticket(ticket):
    return parse_ticket(ticket)


def process_nearby_ticket(valid_ranges, ticket):
    def is_invalid(value):
        return not any(map(lambda r: value in r, valid_ranges))

    return pipe(
        [0] + list(ticket),
        reduce(lambda acc, value: acc + value if is_invalid(value) else acc),
    )


chunks = chunker(lines)
rules = pipe(
    next(chunks),
    map(lambda rule: process_rule(rule)),
    reduce(lambda acc, d: merge(acc, d)),
)
all_valid_ranges = list(get_all_valid_ranges(rules))
my_ticket = process_my_ticket(next(chunks)[1])
nearby_tickets = pipe(
    next(chunks)[1:],
    map(parse_ticket),
)
valid_tickets = pipe(
    nearby_tickets,
    filter(lambda ticket: process_nearby_ticket(all_valid_ranges, ticket) == 0),
)

# produce a mask for each field, indicating whether or not
# each index of all nearby tickets is valid for that field
fields = rules.keys()
masks = {field: [True] * len(fields) for field in fields}
for ticket in valid_tickets:

    def get_field_mask(field, ticket):
        def is_valid(field, value):
            return any(map(lambda _range: value in _range, rules[field]))

        return [is_valid(field, value) for value in ticket]

    masks = {
        field: and_lists(masks[field], get_field_mask(field, ticket))
        for field in fields
    }

# analyze data to find index of each field
result = {field: None for field in fields}
for i in range(len(fields)):
    found = list(valfilter(lambda v: v.count(True) == 1, masks).items())
    assert len(found) == 1
    field, v = found[0]

    # update in our result
    result[field] = v.index(True)

    # invalidate this index for all other fields, as it is now taken
    mask = [not elem for elem in v]
    masks = {field: and_lists(masks[field], mask) for field in fields}
# ensure that we have found an index for each field
assert None not in result.values()

# read my ticket
result = pipe(
    keyfilter(lambda key: "departure" in key, result).values(),
    map(lambda index: my_ticket[index]),
    reduce(mul),
)
print(result)
assert result == 589685618167
