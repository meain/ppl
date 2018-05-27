import os
import sys
import time
import types
import math


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

    spinner_icons = ['◐', '◓', '◑', '◒']
    time_taken = time.time() - start_time
    icon = spinner_icons[int(((time_taken * 10) % 4))]

    avg_time = time_taken / count
    time_left = (total - count) * avg_time
    count_per_sec = 1 / avg_time

    if count == total - 1:
        time_taken = time.time() - start_time
        sys.stdout.write(ERASE_LINE)
        print('%s✔ %s%s  took: %.2fs\r' % (bcolors.GREEN, task, bcolors.ENDC,
                                           time_taken))
    if count < total - 1:
        sys.stdout.write(ERASE_LINE)
        print('%s%s %s%s' % (bcolors.RED, icon, task, bcolors.ENDC))

        # end options: ⋛ ≒
        # bar options: ■ ─
        # extention options: ' ' ⋯

        bar = '  ≒ ' + '─' * (filled_len - 1) + '─' + ' ' * (
            bar_len - filled_len) + ' ≒'
        sys.stdout.write(ERASE_LINE)
        sys.stdout.write(
            '%s  %.2f%s%s\r\n' % (bar, percents, '%', bcolors.ENDC))
        sys.stdout.flush()

        print(
            '  %savg: %.2fs  %sleft: %.2fs  %siter: %d  %sspeed: %.2fiter/s%s'
            % (bcolors.PINK, avg_time, bcolors.BLUE, time_left, bcolors.YELLOW,
               count, bcolors.GREEN, count_per_sec, bcolors.ENDC))
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(CURSOR_UP_ONE)


def _draw_spinner(task, count, start_time, final=False):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    spinner_icons = ['◐', '◓', '◑', '◒']
    time_taken = time.time() - start_time
    avg_time = time_taken / count
    count_per_sec = 1 / avg_time
    icon = spinner_icons[int(((time_taken * 10) % 4))]
    sys.stdout.write(ERASE_LINE)
    print('%s%s %s%s' % (bcolors.RED, icon, task, bcolors.ENDC))
    sys.stdout.write(ERASE_LINE)
    sys.stdout.write(
        '  %savg: %.2fs%s  time: %.2fs  %siter: %d  %sspeed: %.2fiter/s%s\r' %
        (bcolors.PINK, avg_time, bcolors.BLUE, time_taken, bcolors.YELLOW,
         count, bcolors.GREEN, count_per_sec, bcolors.ENDC))
    sys.stdout.write(ERASE_LINE)
    sys.stdout.write(CURSOR_UP_ONE)
    if final:
        total_time = time.time() - start_time
        sys.stdout.write(ERASE_LINE)
        print('%s%s %s%s  took: %.2fs' % (bcolors.GREEN, '✔', task,
                                          bcolors.ENDC, total_time))


def _draw_mini_progress_bar(task, total, count, start_time):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'

    percents = round(100.0 * count / float(total), 1)

    spinner_icons = ['◐', '◓', '◑', '◒']
    time_taken = time.time() - start_time
    icon = spinner_icons[int(((time_taken * 10) % 4))]

    if count == total - 1:
        time_taken = time.time() - start_time
        sys.stdout.write(ERASE_LINE)
        print('%s✔ %s%s  took: %.2fs\r' % (bcolors.GREEN, task, bcolors.ENDC,
                                           time_taken))
    if count < total - 1:
        sys.stdout.write(ERASE_LINE)
        print('%s%s %s%s %.2f%s' % (bcolors.RED, icon, task, bcolors.ENDC,
                                    percents, '%'))
        sys.stdout.write(CURSOR_UP_ONE)


def _draw_mini_spinner(task, count, start_time, final=False):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    spinner_icons = ['◐', '◓', '◑', '◒']
    time_taken = time.time() - start_time
    icon = spinner_icons[int(((time_taken * 10) % 4))]
    sys.stdout.write(ERASE_LINE)
    print(
        '%s%s %s%s iter: %d' % (bcolors.RED, icon, task, bcolors.ENDC, count))
    sys.stdout.write(CURSOR_UP_ONE)
    if final:
        total_time = time.time() - start_time
        sys.stdout.write(ERASE_LINE)
        print('%s%s %s%s  took: %.2fs' % (bcolors.GREEN, '✔', task,
                                          bcolors.ENDC, total_time))


def pb(iterable, task='Task', bar_len=0, mini=False):
    is_generator = isinstance(iterable, types.GeneratorType)
    count = 0
    start_time = time.time()
    if is_generator:
        if not mini:  # this split I guess helps with perf when by removing check on each iter
            for obj in iterable:
                yield obj
                count += 1
                _draw_spinner(task, count, start_time)
            _draw_spinner(task, count, start_time, final=True)
        else:
            for obj in iterable:
                yield obj
                count += 1
                _draw_mini_spinner(task, count, start_time)
            _draw_mini_spinner(task, count, start_time, final=True)
    else:
        total = len(iterable)
        if not mini:
            columns = int(os.popen('stty size', 'r').read().split()[1])
            if bar_len == 0:
                bar_len = columns - 13
                if bar_len > 60:
                    bar_len = 60
            for obj in iterable:
                yield obj
                count += 1
                _draw_progress_bar(task, total, count, start_time, bar_len)
        else:
            for obj in iterable:
                yield obj
                count += 1
                _draw_mini_progress_bar(task, total, count, start_time)
