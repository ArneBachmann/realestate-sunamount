#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x65a62ff0

# Compiled with Coconut version 1.3.1-post_dev28 [Dead Parrot]

# Coconut Header: -------------------------------------------------------------

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_cached_module = _coconut_sys.modules.get("__coconut__")
if _coconut_cached_module is not None and _coconut_os_path.dirname(_coconut_cached_module.__file__) != _coconut_file_path:
    del _coconut_sys.modules["__coconut__"]
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_NamedTuple, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------

# -*- coding: utf-8 -*-
# Copyright Arne Bachmann

# This module provides functions to evaluate a room's or house's sun irradiation for comparison of real estate options.
# This code requires the Coconut transpiler (pip install coconut) and can be tested via coconut-run --strict sunamount.coco --test --mypy


# Standard modules
import calendar  # for number of days in a year computation
import datetime  # for timestamp generation
import math  # trigonometry
import time  # for system locale's daylight savings information

# Dependencies (install via "pip install pysolar pytz" - the latter only used for unit tests)
import pysolar.solar

try:
    from typing import Any
    from typing import List
    from typing import Type
except:
    pass


# Value type definitionss: instantiation and access per keyword or index
class Location(_coconut_NamedTuple("Location", [("latitude", 'float'), ("longitude", 'float'), ("elevation", 'float')])):  # degrees, degrees, meters
    __slots__ = ()  # degrees, degrees, meters
    __ne__ = _coconut.object.__ne__  # degrees, degrees, meters
    def __eq__(self, other):  # degrees, degrees, meters
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # degrees, degrees, meters
    def __new__(_cls, latitude, longitude, elevation=0.):  # degrees, degrees, meters
        return _coconut.tuple.__new__(_cls, (latitude, longitude, elevation))  # degrees, degrees, meters
# degrees, degrees, meters
class Room(_coconut_NamedTuple("Room", [("elevation", 'float'), ("relevance", 'float'), ("times", '_coconut.typing.Optional[_coconut.typing.Sequence[TimeInterval]]')])):  # meters, factor, time intervals (if None, use default)
    __slots__ = ()  # meters, factor, time intervals (if None, use default)
    __ne__ = _coconut.object.__ne__  # meters, factor, time intervals (if None, use default)
    def __eq__(self, other):  # meters, factor, time intervals (if None, use default)
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # meters, factor, time intervals (if None, use default)
    def __new__(_cls, elevation=0., relevance=1., times=None):  # meters, factor, time intervals (if None, use default)
        return _coconut.tuple.__new__(_cls, (elevation, relevance, times))  # meters, factor, time intervals (if None, use default)
# meters, factor, time intervals (if None, use default)
class Window(_coconut_NamedTuple("Window", [("direction", 'float'), ("room", 'Room'), ("stretch", 'float')])):  # degrees, Room, factor
    __slots__ = ()  # degrees, Room, factor
    __ne__ = _coconut.object.__ne__  # degrees, Room, factor
    def __eq__(self, other):  # degrees, Room, factor
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # degrees, Room, factor
    def __new__(_cls, direction, room=Room(), stretch=1.):  # degrees, Room, factor
        return _coconut.tuple.__new__(_cls, (direction, room, stretch))  # degrees, Room, factor
# degrees, Room, factor
class Obstacle(_coconut_NamedTuple("Obstacle", [("direction", 'float'), ("distance", 'float'), ("width", 'float'), ("height", 'float'), ("opacity", 'float')])):  # degrees, meters, meters, meters, 0..1 (0=fully translucent, 1=fully opaque)
    __slots__ = ()  # degrees, meters, meters, meters, 0..1 (0=fully translucent, 1=fully opaque)
    __ne__ = _coconut.object.__ne__  # degrees, meters, meters, meters, 0..1 (0=fully translucent, 1=fully opaque)
    def __eq__(self, other):  # degrees, meters, meters, meters, 0..1 (0=fully translucent, 1=fully opaque)
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # degrees, meters, meters, meters, 0..1 (0=fully translucent, 1=fully opaque)
    def __new__(_cls, direction, distance, width, height, opacity=1.):  # degrees, meters, meters, meters, 0..1 (0=fully translucent, 1=fully opaque)
        return _coconut.tuple.__new__(_cls, (direction, distance, width, height, opacity))  # degrees, meters, meters, meters, 0..1 (0=fully translucent, 1=fully opaque)
# degrees, meters, meters, meters, 0..1 (0=fully translucent, 1=fully opaque)
class TimeInterval(_coconut_NamedTuple("TimeInterval", [("fromHour", 'float'), ("toHour", 'float'), ("weekFactor", 'float')])):  # 0..23.99, 0..23.99, 0..1
    __slots__ = ()  # 0..23.99, 0..23.99, 0..1
    __ne__ = _coconut.object.__ne__  # 0..23.99, 0..23.99, 0..1
    def __eq__(self, other):  # 0..23.99, 0..23.99, 0..1
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # 0..23.99, 0..23.99, 0..1
    def __new__(_cls, fromHour, toHour, weekFactor=7. / 7.):  # 0..23.99, 0..23.99, 0..1
        return _coconut.tuple.__new__(_cls, (fromHour, toHour, weekFactor))  # 0..23.99, 0..23.99, 0..1
# 0..23.99, 0..23.99, 0..1
class Radiation(_coconut_NamedTuple("Radiation", [("wattage", 'float'), ("altitude", 'float'), ("azimuth", 'float')])):  # watts, meters, degrees
    __slots__ = ()  # watts, meters, degrees
    __ne__ = _coconut.object.__ne__  # watts, meters, degrees
    def __eq__(self, other):  # watts, meters, degrees
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  # watts, meters, degrees
# watts, meters, degrees


# Constants
REF_YEAR = 2015  # type: int  # last year with leap seconds definition of the pysolar module, to avoid a warning
MINUTE_STEPS = 5  # type: int  # time interval for accumulated daily sun wattage (increase for faster computation, decrease for more accurate results)
ENTIRE_DAY = TimeInterval(fromHour=0., toHour=23.99, weekFactor=1.)


# Utility decorator
class memoize(dict):
    def __init__(_, func: '_coconut.typing.Callable[[], _coconut.typing.Optional[Any]]') -> 'None':
        _.func = func
    def __call__(_, *args):
        return _[args]
    def __missing__(_, key):
        result = _[key] = _.func(*key)
        return result


Timezone = datetime.timezone  # type: Type  # typedef
UTC = datetime.timezone.utc  # type: Timezone  # the default for all test cases
@memoize
@_coconut_tco
def mktz(hours: 'float'=0.) -> 'Timezone':
    return _coconut_tail_call(Timezone, datetime.timedelta(hours=hours))
CET = mktz(1)  # type: Timezone
CEST = mktz(2)  # type: Timezone


@memoize
@_coconut_tco
def daysinyear(year: 'int') -> 'int':
    return _coconut_tail_call(sum, [calendar.monthrange(year, month)[1] for month in range(1, 12 + 1)])

def sq(value: 'float') -> 'float':  # or value ** 2
    return value * value  # or value ** 2

def is_dst(dt: 'datetime.datetime') -> 'int':  # WARN: uses only the system's local timezone. HINT: In Python, bool is an int, but mypy complains
    return time.localtime(calendar.timegm(dt.timetuple())).tm_isdst  # WARN: uses only the system's local timezone. HINT: In Python, bool is an int, but mypy complains

def tz_datetime(tz: 'Timezone') -> 'function':
    return lambda *args, **kwargs: datetime.datetime(*args, **kwargs).replace(tzinfo=tz)


def getShadowing(sunAltitude: 'float', direction: 'float', obstacle: 'Obstacle', elevation: 'float'=0.) -> 'float':
    ''' Returns sunlight ratio of another building shadowing a window
      returns: 0..1 factor to multiply with incoming sunlight wattage, to reduce its value by the obstacle blocking some light (lower value means less light/more shadowing)

  >>> print(round(getShadowing(2, 90, Obstacle(91, 10, 2, 5)), 4))  # hypo: 11.18m, vangle: 24.10°, hypo: 10.05m, hangle: 11.26°
  0.0074
  >>> print(getShadowing(25, 90, Obstacle(91, 10, 2, 5)))  # hypo: 11.18m, vangle: 26.15°, hypo: 10.31m, hangle: 11.48°, hdiff: 1° < 11.48°, sunAlt: 27° > 26.15°
  1.0
  >>> print(round(getShadowing(24, 90, Obstacle(91, 10, 2, 5)), 4))
  0.0885
  >>> print(round(getShadowing(24, 90, Obstacle(91, 10, 2, 5, opacity = .5)), 4))
  0.5442
  >>> print(getShadowing(2, 90, Obstacle(102, 10, 2, 5)))  # just outside angle
  1.0
  >>> print(round(getShadowing(2, 90, Obstacle(101, 10, 2, 5)), 4))  # just inside angle
  0.0811
  >>> print(round(getShadowing(2, 90, Obstacle(79, 10, 2, 5)), 4))  # same in the other direction
  0.0811
  >>> print(round(getShadowing(2, 90, Obstacle(79, 10, 2, 5), 2.), 4))  # window is two meters higher: more light!
  0.1219
  '''
    translucency = 1. - obstacle.opacity  # type: float
    distanceSquared = (sq)(obstacle.distance)
    elevation = min(obstacle.height, elevation)  # assure that no negative angle occurs (window higher than obstacle)
    hypothenuse = math.sqrt(distanceSquared + sq(obstacle.height - elevation))
    verticalAngle = (math.degrees)((math.atan)(((obstacle.height - elevation) / hypothenuse)))  # angle up upper building edge above ground (arcsin -1..+1 -> -pi/2..+pi/2)
    assert verticalAngle >= 0. and verticalAngle < 90.  # can't be 90 or more, unless infinitely wide
    hypothenuse = math.sqrt(distanceSquared + sq(obstacle.width) / 4.)  # width / 2 for angle to each side
    horizontalAngle = (math.degrees)((math.atan)((obstacle.width / hypothenuse)))  # max. obstacle angle
    assert horizontalAngle >= 0. and horizontalAngle < 90.
    horizontal_diff_deg = abs(direction - obstacle.direction)  # angles out of right direction, independent of right or left
    if horizontal_diff_deg >= horizontalAngle or sunAltitude >= verticalAngle:  # is definitely not shadowed (no obstacle in path of sunlight)
        return 1.  # is definitely not shadowed (no obstacle in path of sunlight)
    return translucency + obstacle.opacity * (horizontal_diff_deg / horizontalAngle) * (sunAltitude / verticalAngle)  # product of quotients -> factor 0..1 favouring low values. translucency/opacity divide the interval 0..1. for factor 1 and the computed factor


def getAngleCorrectionRoomFactor(viewingAngle: 'float', incomingAngle: 'float', stretch_factor: 'float'=1.) -> 'float':
    ''' Return light factor determined by angle difference.
      returns: 0..1 factor that corrects the sunlight wattage

  >>> def output(*args): print(round(getAngleCorrectionRoomFactor(*args), 3))
  >>> output(0., 0.)
  1.0
  >>> output(0., 90.)
  0.0
  >>> output(0., -90.)
  0.0
  >>> output(90., 0.)
  0.0
  >>> output(45., 90.)
  0.707
  >>> output(45., -45.)
  0.0
  >>> output(-45., 45.)
  0.0
  >>> output(45., 0.)
  0.707
  >>> output(45., 0., 1.2)
  0.588
  >>> output(45., 90.)
  0.707
  >>> output(90., 115.)
  0.906
  >>> output(-90., 90.)
  0.0
  >>> output(160., 0.)
  0.0
  '''
    diff_deg = abs(viewingAngle - incomingAngle) * stretch_factor  # type: float  # angles out of right direction
    if diff_deg > 90:  # ignore this angle, as it is outside the (stretched) relevant observation direction
        return 0.  # ignore this angle, as it is outside the (stretched) relevant observation direction
    factor = (abs)((math.cos)((math.radians)(diff_deg)))  # just a formula to get a reduced value depending on the angle
    assert factor >= 0.
    return factor


@_coconut_tco
def getAngleCorrectedSunWattage(date: 'datetime.datetime', location: 'Location', window: 'Window') -> 'Radiation':
    ''' Get radiation amount for specific date, location, and viewing direction.
      returns: a Radiation value type

  >>> location = Location(53.4613331, 9.8276266, 20.)
  >>> def output(irr): print((round(irr.wattage, 3), round(irr.altitude, 3), round(irr.azimuth, 3)))
  >>> output(getAngleCorrectedSunWattage(tz_datetime(CET)(REF_YEAR, 1, 1,  0), location, Window(0.)))  # facing south
  (0.0, 0.0, 0.0)
  >>> output(getAngleCorrectedSunWattage(tz_datetime(CEST)(REF_YEAR, 6, 1,  0), location, Window(0.)))  # midnight
  (0.0, 0.0, 0.0)
  >>> output(getAngleCorrectedSunWattage(tz_datetime(CET)(REF_YEAR, 1, 1, 12), location, Window(0.)))  # noon january
  (674.304, 13.421, 5.699)
  >>> output(getAngleCorrectedSunWattage(tz_datetime(CEST)(REF_YEAR, 6, 1, 12), location, Window(0.)))  # noon june
  (718.889, 55.223, 33.055)
  >>> output(getAngleCorrectedSunWattage(tz_datetime(CEST)(REF_YEAR, 6, 1, 9), location, Window(-90.)))  # noon june other angle
  (0.0, 0.0, 0.0)
  '''
    altitude = pysolar.solar.get_altitude(location.latitude, location.longitude, date, location.elevation + window.room.elevation)  # type: float  # in degrees and meters
    azimuth = pysolar.solar.get_azimuth(location.latitude, location.longitude, date, location.elevation + window.room.elevation)  # type: float
    if azimuth < -180.:  # normalization
        azimuth += 360.  # normalization
    elif azimuth > 180.:  # to -180..180
        azimuth -= 360.  # to -180..180
    if altitude < 0. or altitude > 180.:  # behind the horizon, don't return radiation
        return _coconut_tail_call(Radiation, 0., 0., 0.)  # behind the horizon, don't return radiation
    factor = getAngleCorrectionRoomFactor(window.direction, azimuth, window.stretch)
    return Radiation(factor * pysolar.solar.radiation.get_radiation_direct(date, altitude), altitude, azimuth) if factor > 0. else Radiation(0., 0., 0.)  # compute radiation in Watts / square meter


def getTimeNormalizedSunWattage(date: 'datetime.datetime', location: 'Location', window: 'Window', timeInterval: 'TimeInterval'=ENTIRE_DAY, obstacles: '_coconut.typing.Sequence[Obstacle]'=[], minute_interval: 'int'=MINUTE_STEPS) -> 'float':
    ''' Computes radiation by the minute, then normalize by time interval for an hourly value.
      returns: hourly average radiation (for observed time interval)

  >>> location = Location(53.4613331, 9.8276266, 20.)
  >>> print(round(getTimeNormalizedSunWattage(tz_datetime(CEST)(2015, 6, 1), location, Window(0.)), 3))  # average over entire day this is very little
  188.804
  >>> print(round(getTimeNormalizedSunWattage(tz_datetime(CEST)(2015, 6, 1), location, Window(0., stretch = 2.)), 3))  # smaller window compared to wall length
  81.772
  >>> print(round(getTimeNormalizedSunWattage(tz_datetime(CET)(2015, 3, 1), location, Window(0.)), 3))
  228.892
  >>> print(round(getTimeNormalizedSunWattage(tz_datetime(CET)(2015, 3, 1), location, Window(5.), TimeInterval(9., 18.)), 3))  # average over entire day this is very little
  573.894
  '''
    amount = 0.
    minutes_from = int((timeInterval.fromHour % 1.) * 60)  # type: int
    minutes_to = int((timeInterval.toHour % 1.) * 60)  # type: int
    if minutes_to == 0:  # to avoid computation on last hour (e.g. 4..5 means not compute first minute of 5)
        minutes_to = -1  # to avoid computation on last hour (e.g. 4..5 means not compute first minute of 5)
    for hour in range(int(timeInterval.fromHour), int(timeInterval.toHour) + 1):
        for minute in range(minutes_from if hour == int(timeInterval.fromHour) else 0, minutes_to + 1 if hour == int(timeInterval.toHour) else 60, minute_interval):
            time = tz_datetime(date.tzinfo)(date.year, date.month, date.day, hour, minute)  # create timestamp to compute radiation for
            radiation = getAngleCorrectedSunWattage(time, location, window)
            shadowFactor = 1.  # start with "no shadowing"
            for obstacle in obstacles:  # using the angle corrected wattage, we only need to consider sun altitude in the following step
                shadowFactor = min(shadowFactor, getShadowing(radiation.altitude, window.direction, obstacle, window.room.elevation))  # min for the obstacle blocking the most
            assert radiation.altitude >= 0. and radiation.altitude <= 180.
            assert radiation.azimuth >= -180. and radiation.azimuth <= 180.
            amount += radiation.wattage * shadowFactor
    norm = (60. / MINUTE_STEPS) * (timeInterval.toHour - timeInterval.fromHour)  # type: float
    assert norm >= 0.
    return amount / norm if norm != 0. else 0.


def getDailySunWattageSumForEntireYear(location: 'Location', window: 'Window', timeInterval: 'TimeInterval', obstacles: '_coconut.typing.Sequence[Obstacle]'=[], year: 'int'=REF_YEAR, timezone: 'Timezone'=UTC, time_dst: '_coconut.typing.Optional[Timezone]'=None) -> 'float':
    ''' Return sum of daily average radiation amount.
      returns: computed aggregate wattage

  >>> location = Location(53.4613331, 9.8276266, 20.)
  >>> print(round(getTimeNormalizedSunWattage(tz_datetime(CET)(REF_YEAR, 3, 1), location, Window(0.), TimeInterval(fromHour = 9., toHour = 18.)), 3))
  581.087
  >>> print(round(getDailySunWattageSumForEntireYear(location, Window(0.), TimeInterval(9., 18.), timezone = CET, time_dst = CEST), 3))
  183646.713
  >>> print(round(getDailySunWattageSumForEntireYear(location, Window(0.), TimeInterval(8., 19.), timezone = CET, time_dst = CEST), 3))  # is less due to longer interval at dark times
  153370.104
  >>> print(round(getDailySunWattageSumForEntireYear(location, Window(0.), TimeInterval(11., 15.), timezone = CET, time_dst = CEST), 3))  # is more due to focus on good times
  266687.268

  Try another timezone (but for same location - doesn't really make much sense, but exemplifies the "localize" logic)
  >>> print(round(getDailySunWattageSumForEntireYear(location, Window(0.), TimeInterval(1., 5.), timezone = pytz.timezone("Australia/Queensland")), 3))  # no dst in this timezone
  14860.366

  Now try something with an obstacle:
  >>> print(round(getDailySunWattageSumForEntireYear(location, Window(0., room = Room(elevation = 0.)), TimeInterval(11., 15.), [Obstacle(5, 30, 6, 7, .9)], timezone = pytz.timezone("Europe/Berlin")), 3))  # no dst in this timezone
  257854.546

  And again, with a floor height of 5 meters, which should result in more sunlight
  >>> print(round(getDailySunWattageSumForEntireYear(location, Window(0., room = Room(elevation = 5.)), TimeInterval(11., 15.), [Obstacle(5, 30, 6, 7, .9)], timezone = pytz.timezone("Europe/Berlin")), 3))  # no dst in this timezone
  266687.268
  '''
    amount = 0.
    for days in range(0, (daysinyear)(year)):
        raw_date = datetime.datetime(year, 1, 1) + datetime.timedelta(days=days)
        if time_dst is None:  # using named timezone from pytz or non-dst fixed timezone
            date = timezone.localize(raw_date)
        else:
            date = tz_datetime(time_dst if is_dst(raw_date) else timezone)(year, raw_date.month, raw_date.day)  # compute day of year WARN: is_dst uses system's locale
        amount += timeInterval.weekFactor * getTimeNormalizedSunWattage(date, location, window, timeInterval, obstacles)
    return amount


def getHouseScore(location: 'Location', windows: '_coconut.typing.Sequence[Window]', obstacles: '_coconut.typing.Sequence[Obstacle]', timeIntervals: '_coconut.typing.Sequence[TimeInterval]'=[], timezone: 'Timezone'=UTC, time_dst: '_coconut.typing.Optional[Timezone]'=None) -> 'float':
    ''' Second experiment. Simply show sum of annual amount of daily-hour-normalized sun wattage to compare different house options.
      returns: a score >= 0

  Define the reference location, windows, times and obstacles:
  >>> location = Location(53.4613331, 9.8276266, 20.)
  >>> rooms = {"living": Room(0., 1.), "kitchen": Room(0, .5), "office": Room(0., .5)}
  >>> windows = [Window(-135., rooms["living"], 2.), Window(45., rooms["kitchen"], 2.), Window(-45., rooms["office"], .3)]
  >>> times = [TimeInterval(7., 9., 7./7.), TimeInterval(16., 22.5, 7/7.), TimeInterval(9., 16., 2./7)]
  >>> obstacles = [Obstacle(50, 20, 10, 10, .9), Obstacle(-5, 30, 5, 4, .9), Obstacle(-45, 10, 10, 10, .9), Obstacle(-135, 15, 10, 10, .8)]

  Use a daylight saving-aware timezone:
  >>> print(round(getHouseScore(location, windows, obstacles, times, timezone = pytz.timezone("Europe/Berlin")), 4))
  52799.2992

  Use explicit CET/CEST timezones. TODO This test passes only on a CET/CEST machine, because it derives DST'S start/end dates from the current system locale
  >>> print(round(getHouseScore(location, windows, obstacles, times, timezone = CET, time_dst = CEST), 4))
  52799.2992

  Start a new example:
  >>> print(round(getHouseScore(location, windows[1:2], obstacles[1:2], times, timezone = CET, time_dst = CEST), 4))
  29222.2158

  Update window's room's floor height:
  >>> windows[1] = windows[1]._replace(room = windows[1].room._replace(elevation = 4.))  # raise window's room floor to achieve more light inside
  >>> print(round(getHouseScore(location, windows[1:2], obstacles[1:2], times[:1], timezone = CET, time_dst = CEST), 4))
  14056.5206

  Now check room time interval vs. default time intervals:
  >>> time = [TimeInterval(10, 15)]  # around noon instead
  >>> windows[1] = windows[1]._replace(room = windows[1].room._replace(times = time))  # update time interval
  >>> print(round(getHouseScore(location, windows[1:2], obstacles[1:2], times[:1], timezone = CET, time_dst = CEST), 4))
  58162.953
  '''
    amount = 0.
    for window in windows:
        assert window.room is None or len(window.room) > 0
        for timeInterval in (lambda _coconut_none_coalesce_item: timeIntervals if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(window.room.times):  # use default if nothing defined on room
            amount += window.room.relevance * getDailySunWattageSumForEntireYear(location, window, timeInterval, obstacles, timezone=timezone, time_dst=time_dst)
    return amount


if __name__ == '__main__':
    sys = _coconut_sys
    if '--test' in sys.argv:
        import doctest
        import pytz
        doctest.testmod()
