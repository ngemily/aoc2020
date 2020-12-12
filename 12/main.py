import pudb # noqa

with open("input.txt") as f:
    lines = f.readlines()


def parse_instruction(instruction, x, y, z):
    action, value = instruction[0], instruction[1:]

    def rotate(orientation, degrees, direction):
        steps = int(degrees / 90)
        l = ["N", "E", "S", "W", "N", "E", "S", "W"]
        if direction == "R":
            return l[l.index(orientation) + steps]
        else:
            return l[l.index(orientation) + 4 - steps]

    def advance(x, y, z, n):
        """Advance (x, y) by n steps in the direction of z"""
        func_map = {
            "N": lambda n: (x, y + n),
            "E": lambda n: (x + n, y),
            "S": lambda n: (x, y - n),
            "W": lambda n: (x - n, y),
        }
        return func_map[z](n)

    func_map = {
        "N": lambda n: (x, y + n, z),
        "E": lambda n: (x + n, y, z),
        "S": lambda n: (x, y - n, z),
        "W": lambda n: (x - n, y, z),
        "R": lambda n: (x, y, rotate(z, n, "R")),
        "L": lambda n: (x, y, rotate(z, n, "L")),
        "F": lambda n: (*advance(x, y, z, n), z),
    }
    return func_map[action](int(value))


x = 0
y = 0
orientation = "E"

instructions = map(lambda line: line.strip(), lines)
for instruction in instructions:
    x, y, orientation = parse_instruction(instruction, x, y, orientation)
print(abs(x) + abs(y))
