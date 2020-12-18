from functools import partial
from collections import deque, defaultdict

input_txt = "0,3,6"
input_txt = "20,0,1,11,6,3"
starting_nums = list(map(int, input_txt.split(",")))
last_num = starting_nums[-1]
i = len(starting_nums)

# [num] -> [last two turn numbers in which 'num' was spoken]
last_spoken = defaultdict(
    partial(deque, maxlen=2),
    {num: deque([i], maxlen=2) for i, num in enumerate(starting_nums)},
)

for turn in range(i, 30000000):
    d = last_spoken.get(last_num)
    if len(d) < 2:
        # say '0'
        last_num = 0
    else:
        last_num = d[-1] - d[-2]
    # update 'last_spoken' with current number
    last_spoken[last_num].append(turn)
print(turn, last_num)
