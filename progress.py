import os
import sys
import time
import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


times = time.time()


def progress(count, total, task=''):
    global times
    rows, columns = [int(i) for i in os.popen('stty size', 'r').read().split()]
    bar_len = columns - 10
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)

    if count == 0:
        times = time.time()
        print(bcolors.FAIL + '• ' + task + bcolors.ENDC)

    if count == total - 1:
        time_taken = time.time() - times
        sys.stdout.write(ERASE_LINE)
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)
        print(bcolors.OKGREEN + '✔ ' + task + bcolors.ENDC + ' took ' +
              str(int(time_taken)) + 's')
    else:
        bar = ' ' * 2 + '─' * (filled_len - 1) + '•' + '⋯' * (
            bar_len - filled_len)
        sys.stdout.write('%s %s%s%s\r' % (bar, percents, '%', bcolors.ENDC))
        sys.stdout.flush()


total = 120
tasks = [
    'Make paintball', 'Find dragons', 'Code in python', 'Take out the trash',
    'Fill up water bottles for trip'
]
for task in tasks:
    i = 0
    while i < total:
        progress(i, total, task=task)
        sleep_time = [.05, .04, .03, .02, .01][random.randint(0, 4)]
        time.sleep(sleep_time)  # emulating long-playing job
        i += 1
