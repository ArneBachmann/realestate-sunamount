#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xba677239

# Compiled with Coconut version 1.3.1-post_dev28 [Dead Parrot]

# Coconut Header: -------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_cached_module = _coconut_sys.modules.get(str("__coconut__"))
if _coconut_cached_module is not None and _coconut_os_path.dirname(_coconut_cached_module.__file__) != _coconut_file_path:
    del _coconut_sys.modules[str("__coconut__")]
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_NamedTuple, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------

# -*- coding: utf-8 -*-
# Copyright Arne Bachmann

# Example application that may be adapted to the user's liking (anonymous real-world houses)


# Dependencies (install via "pip install pytz")
try:
    import pytz  # https://stackoverflow.com/questions/7373389/get-the-dst-boundaries-of-a-given-timezone-in-python
    timezone = pytz.timezone("Europe/Berlin")
except:
    LOCAL_TIME_OFFSET = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo.utcoffset(None).total_seconds() / 3600.  # or import time; time.localtime().tm_gmtoff / 3600.  # e.g. tm_zone = "CEST" -> 2.  or float(time.strftime("%z")[:3]) + int(time.strftime("%z")[3:5]) / 60.
    timezone = Timezone(LOCAL_TIME_OFFSET)

# Custom module
from sunamount import *


# Constants
airportNeugrabenFischbek = Location(53.4613331, 9.8276266, 20.)
atHomeTimes = [TimeInterval(7., 9., 7. / 7.), TimeInterval(16., 22.5, 7 / 7.), TimeInterval(9., 16., 2. / 7)]  # list of time intervals and week factors
defaultObstacle = Obstacle(10000., 179.99, .001, .001)  # just something very unlikely to be in the path of sunlight

rooms = {"living": Room(0., 1.), "kitchen": Room(0., .5), "side": Room(0., .6)}

houseChoices = {"Option 1": [Window(-135., rooms["living"], 2.), Window(45., rooms["kitchen"], 2.), Window(-45., rooms["side"], .3)], "Option 2": [Window(-80., rooms["living"], 2.), Window(100., rooms["kitchen"], 2.)]}

houseObstacles = {"Option 1": [Obstacle(20, 50, 10, 10, .9), Obstacle(30, -5, 5, 4, .9), Obstacle(10, -45, 10, 10, .9), Obstacle(15, -135, 10, 10, .8)], "Option 2": [Obstacle(10, 100, 50, 15, .4), Obstacle(20, -95, 8, 8, .9)]}


# Functions
def compareMidsummerMidwinter(coordinates  # type: _coconut.typing.Sequence[Location]
    ):
# type: (...) -> None
    ''' One experiment to confirm assumptions about sun light during day/year. '''
    (print)("Radiation amount on midsummer/midwinter day for specified time windows:")
    for viewing in range(-90, 91, 45):  # from west over south to east
        atMidsummer = sum([hours.weekFactor * getTimeNormalizedSunWattage(tz_datetime(timezone)(REF_YEAR, 6, 22), coordinates, Window(viewing), hours) for hours in atHomeTimes])
        atMidwinter = sum([hours.weekFactor * getTimeNormalizedSunWattage(tz_datetime(timezone)(REF_YEAR, 12, 23), coordinates, Window(viewing), hours) for hours in atHomeTimes])
        (print)("  # Windows facing at an angle of %d deg: %8f / %8f" % (viewing, atMidsummer, atMidwinter))
    (print)("Radiation amount on midsummer/midwinter day at noon:")
    for viewing in range(-90, 91, 45):
        atMidsummer = getTimeNormalizedSunWattage(tz_datetime(timezone)(REF_YEAR, 6, 22), coordinates, Window(viewing), TimeInterval(12, 13))  # sun is around 20..0  degrees during that time
        atMidwinter = getTimeNormalizedSunWattage(tz_datetime(timezone)(REF_YEAR, 12, 23), coordinates, Window(viewing), TimeInterval(12, 13))  # sun is around 5..-10 degrees during that time
        (print)("  # Windows facing at an angle of %d deg: %8f / %8f" % (viewing, atMidsummer, atMidwinter))


if __name__ == '__main__':
    (compareMidsummerMidwinter)(airportNeugrabenFischbek)  # Do a sanity check

    for house, windows in (sorted)(houseChoices.items()):
        (print)(house)
        ((print)(("  # Computed annual sum of hourly radiation during observed times: {}".format)(getHouseScore(airportNeugrabenFischbek, windows, houseObstacles.get(house, defaultObstacle), atHomeTimes, timezone=timezone))))
