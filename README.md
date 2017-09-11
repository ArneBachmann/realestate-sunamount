# Real estate sunlight estimator #
Calculate the a score for the amount of natural sunlight coming into a house through its windows, to know if it's nice to live inside it.
The library takes shadowing of neighboring buildings and other obstacles into account, as well as computation of realistic sunlight irradiation.

If you use this library for whatever purpose, observe the MPL license and also let me know so I may link back or refer to your projects.

- [Link](./sunamount.md) to the package documentation
- [Link](https://www.sonnenverlauf.de/#/53.468,9.8129,11/2017.08.22/18:47/1/0) to a realistic sunlight simulation over time on a map online
- [Link](http://pysolar.org) to the `pysolar` library, which is distributed under the GPLv3 license

Hint on using timezone-aware `datetime` objects:
- Using the `.replace(tzinfo)` method works but doesn't handle daylight savings correctly.
- Better use `pytz` package and use the `.localize()` method