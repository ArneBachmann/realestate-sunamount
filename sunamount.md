# Sun amount estimation library #

## Summary ##
This library allows to compare different real estate buying or building alternatives for the criterion of available sunlight inside the house by computing the amount of light coming through its windows, depending on real estate location, house and windows orientation, window size and/or room's wall sides ratio, neighboring light-blocking obstacles, and relevant time intervals while the inhabitants will be at home to be benefitting from natural sunlight.


## Requirements ##
- [Python 3](https://www.python.org)
- [`pysolar` package](http://pysolar.org)

The code is written in the [Coconut programming language](http://coconut.readthedocs.io), but any Python interpreter with a recent `pip` will be able to run the code.
- Installation is performed via `pip install coconut pysolar`
- Code is run/tested via `coconut-run --strict sunamount.coco --test --mypy`. No visible output means that all tests have passed.


## Provisions ##
- All angles are given in degrees (which are internally converted to radians, as in most programming languages)
- `0` degrees means south for locations on the northern hemisphere, and north on the southern hemisphere (a `pysolar` convention); `90` degrees is always pointing to the east, `-90` degrees to the west
- The unit for obstacles sizes is undefined. You may enter feet or meters without a change in the result
- For years after 2015 leap second information is missing, but this is neglegible for the fidelity of this module's computations


## Functions ##
- `getShadowing(sunAltitude, direction, obstacle)`

  computes a shadowing factor for obstacles blocking the light from the sun to a window viewing direction.
    - `sunAltitude`:float - sun height above the horizon in degrees, computed by `pysolar`
    - `direction`:float - the orientation that a window is facing to, e.g. 45° means to south-east (for on the northern hemisphere, otherwise north-east)
    - `obstacle`:Obstacle - obstacle value type to take into account, which is a named 5-tuple
        - `direction`: degrees of an obstacle from the house (e.g. -90 means fully west of it)
        - `distance`: the obstacle's estimated average distance from the window
        - `width`: the obstacle's estimated and/or apparent width perpendicular to the viewing direction
        - `height`: the obstacles estimated and/or apparent height in relation to the window's center point (>= 0)
        - `opacity`: the opacity, 0..1 where `1.0` means that no light shines through, while `0.0` blocks no light at all

  The function computes angle differences of the obstacles vertical and horizontal edges and checks if sunlight is blocked by it.
  To avoid total neglection of any light when blocked, a normalization by angle differences is computed to let some remaining (environmental) light be accounted for, unless an obstacle is *exactly* in the straight path of light. The resulting value has a range of `0.0` (fully blocked/shadowed) to `1.0` (no blocking/shadowing) to account for indirect lighting.
- `getAngleCorrectionRoomFactor(viewingAngle, incomingAngle, stretch_factor)`

  computes a factor for the amount of available light inside a room, depending on the angle it arrives from, and assuming that light arriving at an angle illuminates less of the room due to more shadowing (of course this is an assumption that doesn't take room topology and furniture or home owners preferred seating locations into account and attempts to maximize room volume lighting, which is contrary to maximized wall/furniture area lighting)
    - `viewingAngle`:float - the orientation that a window is facing to, e.g. 45 means to south-east (northern hemisphere)
    - `incomingAngle`:float - the orientation of incoming light, e.g. -45 means from south-west
    - `stretch_factor`:float - this factor allows to tell the function how stretched the room is and/or how large the window opening is. If the room is twice as long as it is wide, a factor of 2 makes sense. The factor is multiplied internally with the angle difference between viewing angle and incoming light angle to narrow down allowable angles.
      The room stretch factor can also be multiplied by actual window area (in square length units) to account for different window sizes (e.g. 0.96m^2)

  The function returns a unitless factor that can be multiplied with the amount of sun irradiation hitting the window on the outside to account for angle of arrival (room window orientation) and room dimensions (width / depth ratio)
- `getAngleCorrectedSunWattage(date, location, viewing, stretch_factor)`

  computes the average hourly sun wattage for the given date and window orientation.
    - `date`:datetime.datetime - a timestamp
    - `location`:Location - location value type to compute sun wattage for, which is a named 3-tuple
        - `latitude`:float - degrees
        - `longitude`:float - degrees
        - `elevation`:float - in meters above ocean level
    - `window`:Window - window value type to compute incoming light for, which is a named 3-tuple
        - `direction`:float - in degrees, the orientation that a window is facing to
        - `relevance`:float - a unitless factor to tell apart windows of different importance to the home owner
        - `stretch`:float - a unitless room side aspect ratio factor of `>= 1.0`

  The function computes an angle corrected radiation wattage using the `pysolar` library for the given date, geographic location and window orientation.
- `getTimeNormalizedSunWattage(date, location, window, timeInterval, obstacles, minute_interval)`

  computes incoming sun radiation over a certain time interval and normalizes to an hourly average wattage.
    - `date`:datetime.datetime - a date timestamp, ignoring the time of day
    - `location`:Location
    - `window`:Window
    - `timeInterval`:TimeInterval - time interval value type to aggregate sun wattage over a day's time, which is a named 3-tuple
        - `fromHour`:float - hour to start computation at (inclusive). Decimal fractional time may be used, e.g. `5.5` means have past five in the morning
        - `toHour`: end of computation (exclusive). Use `21.99` to compute until ten in the evening.
        - `weekFactor`: factor applied to the result of the given time interval computation, allowing to reduce the importance of a time interval during working days or only apply a time interval on the weekends using `0.286`or `2./7`
    - `obstacles`:[Obstacle] - list of obstacles potentially blocking the path of light, e.g. trees or other houses

  The function will sum up over a days's course all computed wattages in certain time steps (with a default of 5 minutes, or 12 computations per hour) and normalize to an hourly wattage to facilitate better comparability between house and window options.
- `getDailySunWattageSumForEntireYear(location, window, timeInterval, obstacles, year)`

  computes the total sun radiation for an entire (reference) year (which is 2015 because the library doesn't have information on leap seconds after that).
    - `location`:Location
    - `window`:Window
    - `timeInterval`:TimeInterval
    - `obstacles`:[Obstacle]
    - `year`:int - the year to compute data for, defaulting to a refernce year supported by `pysolar`

  The function sums up the hourly wattages for all days. This allows comparison of houses for an entire earth cycle including winter and summer.
- `getHouseScore(location, windows, timeIntervals, obstacles)`

  computes an aggregate sun score for all window sides of a house for the provided time intervals (e.g. morning, afternoon). By summing all window sides it becomes possible to compare house options with or without some of the windows, by adding hourly wattages for each window instead of computing an overall average (which might be lower for more windows). Summation for the entire year allows true season-independent comparison of several real estate options.
 

## Future ideas ##
- Allow windows to have a height above ground and take into account obstacles' heights in relation to them to have different shadowings between rooms/windows.
- Create a GUI that allows to place houses, rooms, windows, and surrounding obstacles graphically, including a data base of common shapes
