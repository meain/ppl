import time
import random
from ppl import pb

total = 120
tasks = [
    'Making paintball', 'Finding dragons', 'Coding in python',
    'Taking out the trash', 'Filling up water bottles for trip'
]
for task in tasks:
    i = 0
    for i in pb(range(total), task=task, mini=True):
        sleep_time = [.05, .04, .03, .02, .01][random.randint(0, 4)]
        time.sleep(sleep_time)  # emulating long-playing task
