from functools import reduce
from utils.utils import chunker

with open("input.txt") as f:
    lines = map(lambda s: s.strip(), f.readlines())


def process_form1(form):
    """returns count of all unique characters in form"""
    return len(set("".join(form)))


def process_form2(form):
    """returns count of all unique charcters common to all entries in form"""
    sets = (set(s) for s in form)
    return len(reduce(lambda acc, s: acc.intersection(s), sets, next(sets)))


forms = chunker(lines)
form_totals = map(lambda form: process_form2(form), forms)
total = reduce(lambda total, form_total: total + form_total, form_totals, 0)
print(total)
