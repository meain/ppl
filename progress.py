import os
import sys
import time
import random


class bcolors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def pb(iterable, task='Task', bar_len=0):
    rows, columns = [int(i) for i in os.popen('stty size', 'r').read().split()]
    if bar_len == 0:
        bar_len = columns - 13
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'

    count = 0
    total = len(iterable)
    times = time.time()
    for obj in iterable:
        yield obj
        count += 1
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)

        avg_time = (time.time() - times) / count
        time_left = (total - count) * avg_time
        count_per_sec = 1 / avg_time

        if count < total - 1:
            sys.stdout.write(ERASE_LINE)
            print('%s• %s%s' % (bcolors.RED, task, bcolors.ENDC))

        if count == total - 1:
            time_taken = time.time() - times
            sys.stdout.write(ERASE_LINE)
            print(bcolors.GREEN + '✔ ' + task + bcolors.ENDC + '  took ' +
                  str(int(time_taken)) + 's')
        if count < total - 1:
            bar = ' ' * 2 + '─' * (filled_len - 1) + '•' + '⋯' * (
                bar_len - filled_len)
            sys.stdout.write(ERASE_LINE)
            sys.stdout.write(
                '%s  %.2f%s%s\r\n' % (bar, percents, '%', bcolors.ENDC))
            sys.stdout.flush()

        if count < total - 1:
            print('    %s avg: %.2fs  %sleft: %.2fs  %scount: %.2fiter/s%s' %
                  (bcolors.BLUE, avg_time, bcolors.YELLOW, time_left, bcolors.PINK, count_per_sec,
                   bcolors.ENDC))
            sys.stdout.write(CURSOR_UP_ONE)
            sys.stdout.write(CURSOR_UP_ONE)
            sys.stdout.write(CURSOR_UP_ONE)


if __name__ == '__main__':
    total = 120
    tasks = [
        'Make paintball', 'Find dragons', 'Code in python',
        'Take out the trash', 'Fill up water bottles for trip'
    ]
    for task in tasks:
        i = 0
        for i in pb(range(total), task=task):
            sleep_time = [.05, .04, .03, .02, .01][random.randint(0, 4)]
            time.sleep(sleep_time)  # emulating long-playing task
