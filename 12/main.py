from collections import namedtuple
import pudb  # noqa

Point = namedtuple("Point", ["x", "y"])

with open("input.txt") as f:
    lines = f.readlines()


def parse_instruction1(instruction, x, y, z):
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


def parse_instruction(instruction, ship, waypoint):
    action, value = instruction[0], instruction[1:]

    def rotate_waypoint(waypoint, degrees, direction):
        if direction == "L":
            degrees = 360 - degrees
        func_map = {
            90: lambda: (Point(waypoint.y, -waypoint.x)),
            180: lambda: (Point(-waypoint.x, -waypoint.y)),
            270: lambda: (Point(-waypoint.y, waypoint.x)),
        }
        return func_map[degrees]()

    def advance_ship(ship, waypoint, n):
        x_delta, y_delta = n * waypoint.x, n * waypoint.y
        return Point(ship.x + x_delta, ship.y + y_delta), waypoint

    func_map = {
        "N": lambda n: (ship, Point(waypoint.x, waypoint.y + n)),
        "E": lambda n: (ship, Point(waypoint.x + n, waypoint.y)),
        "S": lambda n: (ship, Point(waypoint.x, waypoint.y - n)),
        "W": lambda n: (ship, Point(waypoint.x - n, waypoint.y)),
        "R": lambda n: (ship, rotate_waypoint(waypoint, n, "R")),
        "L": lambda n: (ship, rotate_waypoint(waypoint, n, "L")),
        "F": lambda n: advance_ship(ship, waypoint, n),
    }
    return func_map[action](int(value))


x = 0
y = 0
orientation = "E"

instructions = map(lambda line: line.strip(), lines)
for instruction in instructions:
    x, y, orientation = parse_instruction1(instruction, x, y, orientation)
print(abs(x) + abs(y))

ship = Point(0, 0)
waypoint = Point(10, 1)

instructions = map(lambda line: line.strip(), lines)
for instruction in instructions:
    ship, waypoint = parse_instruction(instruction, ship, waypoint)
print(abs(ship.x) + abs(ship.y))
