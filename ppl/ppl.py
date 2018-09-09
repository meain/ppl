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

    if count != 0:
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

    if count != 0:
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


def _call_renderer(is_generator, mini, task, count, start_time, total, bar_len, final):
    if not is_generator or total is not None:
        if mini:
            _draw_mini_progress_bar(task, total, count, start_time)
        else:
            _draw_progress_bar(task, total, count, start_time, bar_len)
    else:
        if mini:
            _draw_mini_spinner(task, count, start_time, final)
        else:
            _draw_spinner(task, count, start_time, final)


def pb(iterable, task="Task", bar_len=None, mini=False, total=None):
    count = 0
    start_time = time.time()
    is_generator = isinstance(iterable, types.GeneratorType)

    if not is_generator or total is not None:
        if total is None:
            total = len(iterable)
        if bar_len is None:
            try:
                columns = int(os.popen("stty size", "r").read().split()[1])
            except Exception:
                columns = 100
            bar_len = min(60, columns - 13)

    for obj in iterable:
        yield obj
        _call_renderer(is_generator, mini, task, count, start_time, total, bar_len, False)
        count += 1
    _call_renderer(is_generator, mini, task, count, start_time, total, bar_len, True)
