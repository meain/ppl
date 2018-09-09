import os
import sys
import time
import types


class bcolors:
    PINK = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


CURSOR_UP_ONE = "\x1b[1A"
ERASE_LINE = "\x1b[2K"
spinner_icons = ["◐", "◓", "◑", "◒"]

END_CHAR = "⋛"
BAR_CHAR = "─"
CHECK_CHAR = "✔"
# end options: ⋛ ≒
# bar options: ■ ─
# pointer options: ╼ ◎ ● ○
# extention options: ' ' ⋯


def _draw_progress_bar(task, total, count, start_time, bar_len):
    time_taken = time.time() - start_time
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    icon = spinner_icons[int(((time_taken * 10) % 4))]

    avg_time = (time_taken / count) if count != 0 else 0
    time_left = ((total - count) * avg_time) if avg_time != 0 else 0
    count_per_sec = (1 / avg_time) if avg_time != 0 else 0

    if (count != 0):
        sys.stdout.write(ERASE_LINE)
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)

    if count == total:
        sys.stdout.write(
            "\r%s%s %s%s  took: %.2fs\n"
            % (bcolors.GREEN, CHECK_CHAR, task, bcolors.ENDC, time_taken)
        )
    else:
        sys.stdout.write("\r%s%s %s%s\n" % (bcolors.RED, icon, task, bcolors.ENDC))

        bar = (
            "  "
            + BAR_CHAR * (filled_len - 1)
            + BAR_CHAR
            + " " * (bar_len - filled_len)
            + " "
            + END_CHAR
        )
        sys.stdout.write("\r%s  %.2f%s%s\n" % (bar, percents, "%", bcolors.ENDC))

        sys.stdout.write(
            "\r  %savg: %.2fs  %sleft: %.2fs  %siter: %d  %sspeed: %.2fiter/s%s"
            % (
                bcolors.PINK,
                avg_time,
                bcolors.BLUE,
                time_left,
                bcolors.YELLOW,
                count,
                bcolors.GREEN,
                count_per_sec,
                bcolors.ENDC,
            )
        )


def _draw_spinner(task, count, start_time, final=False):
    time_taken = time.time() - start_time
    avg_time = (time_taken / count) if count != 0 else 0
    count_per_sec = (1 / avg_time) if avg_time != 0 else 0
    icon = spinner_icons[int(((time_taken * 10) % 4))]

    if (count != 0):
        sys.stdout.write(ERASE_LINE)
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)
    if final:
        sys.stdout.write(
            "\r%s%s %s%s  took: %.2fs\n"
            % (bcolors.GREEN, CHECK_CHAR, task, bcolors.ENDC, time_taken)
        )
    else:
        sys.stdout.write("\r%s%s %s%s\n" % (bcolors.RED, icon, task, bcolors.ENDC))
        sys.stdout.write(
            "\r  %savg: %.2fs%s  time: %.2fs  %siter: %d  %sspeed: %.2fiter/s%s"
            % (
                bcolors.PINK,
                avg_time,
                bcolors.BLUE,
                time_taken,
                bcolors.YELLOW,
                count,
                bcolors.GREEN,
                count_per_sec,
                bcolors.ENDC,
            )
        )


def _draw_mini_progress_bar(task, total, count, start_time):
    time_taken = time.time() - start_time
    percents = round(100.0 * count / float(total), 1)
    icon = spinner_icons[int(((time_taken * 10) % 4))]

    sys.stdout.write(ERASE_LINE)
    if count == total:
        sys.stdout.write(
            "\r%s%s %s%s  took: %.2fs\n"
            % (bcolors.GREEN, CHECK_CHAR, task, bcolors.ENDC, time_taken)
        )
    else:
        sys.stdout.write(
            "\r%s%s %s%s %.2f%s"
            % (bcolors.RED, icon, task, bcolors.ENDC, percents, "%")
        )


def _draw_mini_spinner(task, count, start_time, final=False):
    time_taken = time.time() - start_time
    icon = spinner_icons[int(((time_taken * 10) % 4))]

    sys.stdout.write(ERASE_LINE)
    if final:
        sys.stdout.write(
            "\r%s%s %s%s  took: %.2fs\n"
            % (bcolors.GREEN, CHECK_CHAR, task, bcolors.ENDC, time_taken)
        )
    else:
        sys.stdout.write(
            "\r%s%s %s%s iter: %d" % (bcolors.RED, icon, task, bcolors.ENDC, count)
        )


def _cleanup():
    sys.stdout.write(ERASE_LINE)
    sys.stdout.write("\n")
    sys.stdout.write(ERASE_LINE)
    sys.stdout.write("\n")
    sys.stdout.write(ERASE_LINE)
    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(CURSOR_UP_ONE)


def pb(iterable, task="Task", bar_len=0, mini=False):
    is_generator = isinstance(iterable, types.GeneratorType)
    count = 0
    start_time = time.time()
    if is_generator:
        if not mini:
            for obj in iterable:
                _draw_spinner(task, count, start_time)
                yield obj
                count += 1
            _draw_spinner(task, count, start_time, final=True)
        else:
            for obj in iterable:
                _draw_mini_spinner(task, count, start_time)
                yield obj
                count += 1
            _draw_mini_spinner(task, count, start_time, final=True)
        _cleanup()
    else:
        total = len(iterable)
        if not mini:
            try:
                columns = int(os.popen("stty size", "r").read().split()[1])
            except Exception:
                columns = 100
            if bar_len == 0:
                bar_len = columns - 13
                if bar_len > 60:
                    bar_len = 60
            for obj in iterable:
                _draw_progress_bar(task, total, count, start_time, bar_len)
                yield obj
                count += 1
            _draw_progress_bar(task, total, count, start_time, bar_len)
        else:
            for obj in iterable:
                _draw_mini_progress_bar(task, total, count, start_time)
                count += 1
                yield obj
            _draw_mini_progress_bar(task, total, count, start_time)
        _cleanup()
