import time
import random
from ppl import pb

total = 120
tasks = ["Making paintball", "Finding dragons", "Taking out the trash"]

print('With iter_name')
for task in tasks:
    i = 0
    for i in pb(range(total), task=task):
        sleep_time = [.05, .04, .03, .02, .01][random.randint(0, 4)]
        time.sleep(sleep_time)  # emulating long-playing task

print('\nWithout iter_name')
for task in tasks:
    i = 0
    for i in pb(range(total), task=task, iter_name=None):
        sleep_time = [.05, .04, .03, .02, .01][random.randint(0, 4)]
        time.sleep(sleep_time)  # emulating long-playing task
