import time
from ppl import pb


def square(nums):
    for i in nums:
        yield (i * i)


tasks = [
    'Mapping points', 'Painting rainbow white', 'Planting seeds',
    'Playing mario', 'Watching anime'
]
counts = [100, 400, 100, 200, 50]
times = [.01, .01, .03, .02, .05]

for x in zip(tasks,counts, times):
    for i in pb(square(range(x[1])), task=x[0], mini=True):
        time.sleep(x[2])
