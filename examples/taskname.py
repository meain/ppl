import time
import random
from ppl import pb

total = 120
tasks = [
    'Make paintball', 'Find dragons', 'Code in python', 'Take out the trash',
    'Fill up water bottles for trip'
]
for task in tasks:
    i = 0
    for i in pb(range(total), task=task):
        sleep_time = [.05, .04, .03, .02, .01][random.randint(0, 4)]
        time.sleep(sleep_time)  # emulating long-playing task
