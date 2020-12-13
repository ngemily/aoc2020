from toolz.curried import pipe, map, filter

with open("input.txt") as f:
    ready_at = int(f.readline().strip())
    busses = pipe(
        f.readline().split(","),
        filter(lambda s: s != "x"),
        map(lambda s: int(s)),
    )

next_departures = []
for bus in busses:
    next_departure = bus * (int(ready_at / bus) + 1)
    next_departures.append((bus, next_departure))

bus, departure = min(next_departures, key=lambda t: t[1])
wait_time = departure - ready_at
print(bus, wait_time, bus * wait_time)
