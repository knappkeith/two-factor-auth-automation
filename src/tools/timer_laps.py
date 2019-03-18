from src.tools import stopwatch
from collections import namedtuple


class LapWatch(stopwatch.Timer):
    lap_tuple = namedtuple('lap',
                           ['total_time', 'lap_time', 'lap_name', 'tag'])

    def __init__(self):
        self.laps = lap_list()
        super(LapWatch, self).__init__()

    def lap(self, lap_name=None, tag=None):
        total = self.elapsed
        if not lap_name:
            lap_name = "Lap %d" % (len(self.laps) + 1)
        if len(self.laps) == 0:
            lap_time = total
        else:
            lap_time = total - self.laps[-1][0]
        self.laps.append(self.lap_tuple(total, lap_time, lap_name, tag))
        return lap_time

    def reset_laps(self):
        self.laps = lap_list()


class lap_list(list):
    def __init__(self, print_format="{name}:{time:>17}", *args, **kwargs):
        self.print_format = print_format
        super(lap_list, self).__init__(*args, **kwargs)

    def average(self):
        if len(self) > 0:
            return self.sum() / len(self)
        else:
            return self.sum()

    def max(self):
        return max(self, key=lambda x: x.lap_time)

    def min(self):
        return min(self, key=lambda x: x.lap_time)

    def sum(self):
        return sum([x.lap_time for x in self])

    def filter(self, tag_filter=[]):
        return lap_list(
            self.print_format,
            [x for x in self if x.tag in tag_filter])

    def exclude(self, tag_exclude=[]):
        return lap_list(
            self.print_format,
            [x for x in self if x.tag not in tag_exclude])

    def _print_lap(self, lap):
        if isinstance(lap, dict):
            return self.print_format.format(
                name=lap['lap_name'],
                time=secs_to_str(lap['lap_time']),
                tag=lap['tag'],
                total=lap['total_time'])
        else:
            return self.print_format.format(
                name=lap.lap_name,
                time=secs_to_str(lap.lap_time),
                tag=lap.tag,
                total=lap.total_time)

    def __str__(self):
        return "\n".join([self._print_lap(x) for x in self])


def secs_to_str(seconds):
    hrs = int(seconds // 3600)
    time_left = seconds - (hrs * 3600)
    mins = int(time_left // 60)
    time_left -= (mins * 60)
    secs = int(time_left)
    time_left -= secs
    milli_secs = int(round(time_left, 3) * 1000)
    if hrs > 0:
        rtn_str = "{hrs}h {mins:>02}m {secs:>2}.{milli:>03}s".format(
            hrs=str(hrs),
            mins=str(mins),
            secs=str(int(secs)),
            milli=str(milli_secs))
    elif mins > 0:
        rtn_str = "{mins}m {secs:>02}.{milli:>03}s".format(
            mins=str(mins),
            secs=str(int(secs)),
            milli=str(milli_secs))
    else:
        rtn_str = "{secs}.{milli:>03}s".format(
            secs=str(int(secs)),
            milli=str(milli_secs))
    return rtn_str
