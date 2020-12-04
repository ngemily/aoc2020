from toolz.itertoolz import concat
from toolz.curried import map, filter, pipe

from itertools import chain

import pudb  # noqa

REQUIRED_ENTRIES = set(
    [
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
    ]
)


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


with open("input.txt") as f:
    lines = map(lambda s: s.strip(), f.readlines())
    passports = map(lambda entries: parse_passport(entries), chunker(lines))


def parse_passport(entries):
    entries = concat(map(lambda s: s.split(), chain(entries)))
    passport = {k: v for (k, v) in map(lambda entry: entry.split(":"), entries)}
    return passport


def has_required_entries(passport):
    present_entries = set(passport.keys())
    present_entries.discard("cid")
    return present_entries == REQUIRED_ENTRIES


def validate_passport_entries(passport):
    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    # hgt (Height) - a number followed by either cm or in:

    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.

    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    def valid_hgt(hgt_str):
        hgt_val, hgt_unit = hgt_str[0:-2], hgt_str[-2:]
        if hgt_unit == "cm":
            return 150 <= int(hgt_val) <= 193
        elif hgt_unit == "in":
            return 59 <= int(hgt_val) <= 76
        else:
            return False

    def valid_hcl(hcl_str):
        return (
            len(hcl_str) == 7
            and hcl_str[0] == "#"
            and all(map(lambda s: s in "0123456789abcdef", hcl_str[1:]))
        )

    def valid_pid(pid_str):
        return len(pid_str) == 9 and all(map(lambda c: c.isdigit(), pid_str))

    func_map = {
        "byr": lambda x: 1920 <= int(x) <= 2002,
        "iyr": lambda x: 2010 <= int(x) <= 2020,
        "eyr": lambda x: 2020 <= int(x) <= 2030,
        "hgt": valid_hgt,
        "hcl": valid_hcl,
        "ecl": lambda s: s in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
        "pid": valid_pid,
        "cid": lambda x: True,
    }
    return all([func_map[k](v) for k, v in passport.items()])


print(
    pipe(
        passports,
        filter(has_required_entries),
        map(validate_passport_entries),
        sum,
    )
)
