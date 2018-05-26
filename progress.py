import os
import sys
import time
import types


class bcolors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def _draw_progress_bar(task, total, count, start_time, bar_len):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'

    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)

    avg_time = (time.time() - start_time) / count
    time_left = (total - count) * avg_time
    count_per_sec = 1 / avg_time

    if count < total - 1:
        sys.stdout.write(ERASE_LINE)
        print('%s• %s%s' % (bcolors.RED, task, bcolors.ENDC))

    if count == total - 1:
        time_taken = time.time() - start_time
        sys.stdout.write(ERASE_LINE)
        print('%s✔ %s%s  took: %.2fs\r' % (bcolors.GREEN, task, bcolors.ENDC,
                                           time_taken))
    if count < total - 1:
        bar = ' ' * 2 + '─' * (filled_len - 1) + '•' + '⋯' * (
            bar_len - filled_len)
        sys.stdout.write(ERASE_LINE)
        sys.stdout.write(
            '%s  %.2f%s%s\r\n' % (bar, percents, '%', bcolors.ENDC))
        sys.stdout.flush()

    if count < total - 1:
        print('    %s avg: %.2fs  %sleft: %.2fs  %scount: %.2fiter/s%s' %
              (bcolors.PINK, avg_time, bcolors.BLUE, time_left, bcolors.YELLOW,
               count_per_sec, bcolors.ENDC))
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(CURSOR_UP_ONE)


def _draw_spinner(task, count, start_time, final=False):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    spinner_icons = ['◐', '◓', '◑', '◒']
    time_taken = time.time() - start_time
    avg_time = time_taken / count
    icon = spinner_icons[int(((time_taken * 10) % 4))]
    sys.stdout.write(ERASE_LINE)
    print('%s%s %s%s' % (bcolors.RED, icon, task, bcolors.ENDC))
    sys.stdout.write(ERASE_LINE)
    sys.stdout.write('%s  avg: %.2fs%s  time: %.2fs  %siter: %d%s\r' %
                     (bcolors.PINK, avg_time, bcolors.BLUE, time_taken,
                      bcolors.YELLOW, count, bcolors.ENDC))
    sys.stdout.write(ERASE_LINE)
    sys.stdout.write(CURSOR_UP_ONE)
    if final:
        total_time = time.time() - start_time
        sys.stdout.write(ERASE_LINE)
        print('%s%s %s%s  took: %.2fs' % (bcolors.GREEN, '✔', task,
                                          bcolors.ENDC, total_time))


def pb(iterable, task='Task', bar_len=0):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    rows, columns = [int(i) for i in os.popen('stty size', 'r').read().split()]
    if bar_len == 0:
        bar_len = columns - 13
    is_generator = isinstance(iterable, types.GeneratorType)
    count = 0
    start_time = time.time()
    if is_generator:
        spinner_icons = ['◐', '◓', '◑', '◒']
        for obj in iterable:
            yield obj
            count += 1
            _draw_spinner(task, count, start_time)
        _draw_spinner(task, count, start_time, final=True)
    else:
        total = len(iterable)
        for obj in iterable:
            yield obj
            count += 1
            _draw_progress_bar(task, total, count, start_time, bar_len)
