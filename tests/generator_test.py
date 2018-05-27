import time
from ppl import pb


def square(nums):
    for i in nums:
        yield (i * i)


tasks = [
    'Mapping points', 'Painting rainbow white', 'Playing mario',
    'Watching anime'
]
counts = [100, 400, 100, 50]
times = [.01, .01, .03, .05]

for x in zip(tasks, counts, times):
    for i in pb(square(range(x[1])), task=x[0]):
        time.sleep(x[2])
