# Real estate sunlight estimator #

Calculates a score for the amount of natural sunlight coming into (the rooms of) a house through its windows, to get an idea of if it's nice to live inside it.
The library takes shadowing of neighboring buildings and other obstacles into account, as well as computation of realistic sunlight irradiation.

This software is licensed under the [MPL-2.0](https://github.com/ArneBachmann/realestate-sunamount/blob/master/LICENSE).

If you use this library for whatever purpose, please let me know so I may link back and/or refer to your projects.

- [The package documentation](./sunamount.md)
- [A realistic sunlight simulation over time on a map online](https://www.sonnenverlauf.de/#/53.468,9.8129,11/2017.08.22/18:47/1/0)
- [The `pysolar` library](http://pysolar.org), licensed under GPLv3
- [The `pytz` library](http://pytz.sourceforge.net), licensed under the MIT license

Hint on using timezone-aware `datetime` objects:
- Best is using the `pytz` package.
- Alternatively, use fixed-hours timezones or the replacement class defined for Python 2 (cf. source of [`sunamount`](./sunamount.coco)).
