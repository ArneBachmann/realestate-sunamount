# Sun amount estimation library #

## Summary ##
This library allows to compare different real estate buying or building alternatives for the criterion of available sunlight inside the building by computing the amount of natural light coming inside through its windows, depending on real estate location, house and windows orientation, room importance and relevant at-home times, window size and/or room's wall sides ratio, neighboring light-blocking obstacles.


## Requirements ##
- Language interpreter: [Python 3](https://www.python.org). Python 2 would be supported as well by Coconut, but the `pysolar` library below is not compatible
- [Coconut programming language and transpiler](http://coconut.readthedocs.io)
- Software dependencies: [`pysolar`](http://pysolar.org) and [`pytz` package (recommended)](http://pytz.sourceforge.net/)

### Installation
- The code is written in the Coconut language, but any installed Python interpreter with a recent `pip` will be able to install Coconut to further compile and run the application
- Installation is performed via `pip install coconut pysolar pytz`
- The library is tested via `coconut-run --strict sunamount.coco --test`. Seeing no output means that all tests have passed. Manual transpilation can be done via `coconut --strict sunamount.coco --mypy`
- The example is executed via `coconut-run --strict example.coco`


## Provisions ##
- All angles are given in degrees (which are internally converted to radians, as in most computer systems)
- `0` degrees means *south* for locations on the northern hemisphere (boreal), and *north* on the southern hemisphere (austral), which is a convention borrowed from the `pysolar` library); `+90` degrees is always pointing to the east, `-90` degrees to the west
- The length unit for obstacles sizes is undefined. You may enter feet or meters without a change in the result; the sunlight computation, however, relies on an elevation above sea level in meters, therefore it's recommended to always stick to meters
- For years after 2015, leap seconds information is missing, but this is most likely neglegible for the fidelity of this module's computations. The `pysolar` library has been augmented with 2016 and 2017 leap seconds, but is not yet available via `pip` (still on the `develop` Git branch)
- All data types are defined as value types (named tuples) to simplify work with house definitions. Please see `sunamount.coco` for their definition


## Function descriptions ##
- `getShadowing(sunAltitude, direction, obstacle, elevation)`

  computes a shadowing factor for obstacles blocking the light from the sun to a window viewing direction.
    - `sunAltitude`:float - sun height above the horizon in degrees, as computed by `pysolar`
    - `direction`:float - the orientation that a window is facing to in degrees, e.g. 45° means to south-east (on the northern hemisphere, north-east on the southern hemisphere)
    - `obstacle`:Obstacle - an obstacle value type to take into account regarding shadowing, which is a named 5-tuple:
        - `direction`: angle in degrees of an obstacle from the house (e.g. -90 means fully west of the house/room/window)
        - `distance`: the obstacle's estimated average (front side) distance from the window, neglecting any obstacle shape or curvature
        - `width`: the obstacle's estimated and/or apparent width perpendicular to the viewing direction
        - `height`: the obstacle's estimated and/or apparent height in relation to the window's bottom side (>= 0)
        - `opacity`: the obstacle's opacity in the range of 0..1 where `1.0` means that all light is blocked, while `0.0` means fully transparent
    - `elevation`:float - height above ground of the computed window's bottom side

  The function computes angle differences of the obstacle's (assumedly perpendicular and square) vertical and horizontal edges and checks if sunlight is blocked by it.
  To avoid total neglection of any light when blocked (full darkness is unrealistic inside Earth's atmosphere), a normalization by angle differences is computed to let some remaining (environmental) light be accounted for, unless an obstacle is *exactly* in the straight path of light. The resulting value has a range of `0.0` (fully blocked/shadowed) to `1.0` (no blocking/shadowing) to account for indirect lighting, disregarding fog/haze/dust/particles and using a fixed simplification formula.
- `getAngleCorrectionRoomFactor(viewingAngle, incomingAngle, stretch_factor)`

  computes a factor for the amount of available light inside a room, depending on the angle it arrives from, and assuming that light arriving at an angle illuminates less of the room due to its angle (of course this is an assumption that doesn't take room topology and furniture placement or home owners' preferred residence locations into account and attempts to maximize room *volume* lighting, which is different from maximizing wall or furniture *area* lighting)
    - `viewingAngle`:float - the orientation that a window is facing to, e.g. 45 means *to* south-east (on the northern hemisphere)
    - `incomingAngle`:float - the orientation of incoming light, e.g. -45 means *from* south-west
    - `stretch_factor`:float - this factor allows to tell the function how stretched the room is as seen from the window's wall and/or how large the window opening is in comparison with the room's wall areas. If the room is twice as long as it is wide, a factor of 2 makes sense. The factor is multiplied internally with the angle difference between viewing angle and incoming light angle to narrow down allowable angles; this is a simplification and is in no way physically meaningful or accurate.
      The room stretch factor can also be multiplied by actual window area (in square length units) to account for different window sizes (e.g. 0.96m^2).
      The room stretch factor must be set differently for different windows in the same room, if they are placed at differnent walls, to account for their relative geometry (from one side its a wide room, but on the other wall it's a stretched room).

  The function returns a unitless factor between `0..1` that can be multiplied with the amount of sun irradiation hitting the window on the outside (as computed by `getShadowing`) to account for angle of arrival (room window orientation) and room dimensions (width / depth ratio) and/or window area size.
- `getAngleCorrectedSunWattage(date, location, window)`

  computes the *average* hourly sun wattage for the given date, geographic location, and window orientation, and returns a radiation value type.
    - `date`:datetime.datetime - a timestamp (potentially localized, otherwise using system's locale)
    - `location`:Location - a location value type to compute sun wattage for, which is a named 3-tuple:
        - `latitude`:float - degrees from equator (positive is northern, negative is southern)
        - `longitude`:float - degrees from Greenwich (positive is eastern, negative is western)
        - `elevation`:float - meters above sea level
    - `window`:Window - a window value type to compute incoming light for, which is a named 3-tuple:
        - `direction`:float - the orientation that a window is facing to in degrees
        - `room`:Room - a room value type that the window belongs to, which is a 3-tuple:
            - `elevation`:float - meters of the room's floor level relative to the location's elevation (positive means higher, negative lower)
            - `relevance`:float - a unitless factor to optionally tell apart rooms of different relative importance to the home owner
            - `times`:[TimeInterval] - a non-empty list of time intervals the room is inhabited, or None (using defaults provided to the `getHouseScore` function)
    - `stretch`:float - a unitless room dimensions aspect ratio factor, optionally multiplied by a window square area

  The function computes an angle-corrected radiation wattage for the given date, geographic location, taking into account room relevance and presence, and window orientation.
- `getTimeNormalizedSunWattage(date, location, window, timeInterval, obstacles, minute_interval)`

  computes incoming sun radiation over a certain time interval of a day and normalizes to an hourly average wattage.
    - `date`:datetime.datetime - a pure (optionally localized) date timestamp, ignoring the time of day
    - `location`:Location - a location value type
    - `window`:Window - a window value type
    - `timeInterval`:TimeInterval - time interval value type to aggregate sun wattage over the part of a day's time, which is a named 3-tuple:
        - `fromHour`:float - hour to start computation at (inclusive). Decimal fractional time may be used, e.g. `5.5` means half past five in the morning
        - `toHour`:float - hour to end computation (exclusive). Use `21.99` to compute sunlight until ten in the evening
        - `weekFactor`:float - a factor applied to the result of the given time interval computation, allowing to reduce the importance of a time interval, e.g. to differentiate between working days, weekend, or entire week (`5./7.`, `2./7`, or `7./7.`)
    - `obstacles`:[Obstacle] - potentially empty list of obstacles to check for blocking the path of light, e.g. trees, fences, other houses or even cars
    - `minute_interval`: int - number of minutes between sunlight computations. `6` means one computations for every 6 minutes, or 10 computations per hours. This can be used to increase or decrease fidelity vs. computation time

  The function sums up over the given time interval of a day all computed wattages in certain time steps (with a default of 5 minutes, or 12 computations per hour) and normalize the result to an hourly wattage to facilitate better comparison between house and window options.
- `getDailySunWattageSumForEntireYear(location, window, timeInterval, obstacles, year, timezone, time_dst)`

  computes the total sun radiation for an entire year.
    - `location`:Location - a location value type
    - `window`:Window - a window value type
    - `timeInterval`:TimeInterval - a time interval value type
    - `obstacles`:[Obstacle] - a list of obstacle value types
    - `year`:int - the year to compute data for, defaulting to a reference year, as supported by `pysolar`
    - `timezone`:Timezone - a timezone object with the hours offset for the standard time in that timezone, and/or logic to know about daylight savings offset and start/end timesm, as returned by the `pytz` library (recommended)
    - `time_dst`:Timezone - a timezone object with the hours offset for the daylight savings dates (as determined by the current system locale, not recommended)

  The function sums up the hourly wattages for all days in the given year. This allows comparison of houses for an entire earth cycle around the sun including winter and summer to include short and long days throughout the year for a realistic score.
- `getHouseScore(location, windows, obstacles, timeIntervals, timezone, time_dst)`

  computes an aggregate sun amount score for a fully specified house and time intervals of an entire year.
    - `location`:Location - a location value type
    - `windows`:[Window] - a list of window value types
    - `obstacles`:[Obstacle] - a list of obstacle value types
    - `timeInterval`:[TimeInterval] - a possible empty list of time interval value types, to be used if windows's room references don't specify time intervals themselves
    - `timezone`:Timezone - a timezone object with the hours offset for the standard time in that timezone, and/or logic to know about daylight savings offset and start/end timesm, as returned by the `pytz` library (recommended)
    - `time_dst`:Timezone - a timezone object with the hours offset for the daylight savings dates (as determined by the current system locale, not recommended)

  By summing up all window sides it becomes possible to compare house options with or without some of the windows.
  By adding hourly wattages for each window instead of computing an overall average (which might be lower for more windows), comparison between number of windows becomes possible.
  Summation for the entire year allows true season-independent comparison of several real estate options.

## Todo ##
- Provide a pre-transpiled Python-installable package, also for conda
- Create a GUI