import pudb # noqa


def parse_password(entry):
    rule, password = entry.split(":")

    range_str, char = rule.split()
    x_str, y_str = range_str.split("-")
    x, y = int(x_str), int(y_str)

    return x, y, char, password.strip()


def valid_password(entry):
    x, y, char, password = parse_password(entry)

    return (password[x - 1] == char) != (password[y - 1] == char)


def valid_password1(entry):
    min_count, max_count, char, password = parse_password(entry)

    char_count = password.count(char)
    return min_count <= char_count <= max_count


with open("input.txt") as f:
    lines = map(lambda s: s.strip(), f.readlines())


num_valid_passwords = sum(map(lambda s: valid_password(s), lines))
print(num_valid_passwords)
