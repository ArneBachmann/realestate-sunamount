import os, sys, time
from setuptools import setup, find_packages

lt = time.localtime()
version = (lt.tm_year, (10 + lt.tm_mon) * 100 + lt.tm_mday, (10 + lt.tm_hour) * 100 + lt.tm_min)
versionString = '.'.join(map(str, version))

# Clean up old binaries for twine upload
if "clean" in sys.argv:
  import shutil
  shutil.rmtree("build")

if os.path.exists("dist"):
  rmFiles = list(sorted(os.listdir("dist")))
  for file in (f for f in rmFiles if any([f.endswith(ext) for ext in (".tar.gz", "zip")])):
    print("Removing old sdist archive %s" % file)
    try: os.unlink(os.path.join("dist", file))
    except: print("Cannot remove old distribution file " + file)

setup(
  name = 'rese',
  version = versionString,  # without extra
  description = "RESE - Real estate sunlight estimator",
  long_description = "",  # TODO readme excerpt
  install_requires = ["mypy", "pysolar", "pytz"],  # mypy is actually just for testing
  python_requires = '>=3.0',
  classifiers = [c.strip() for c in """
        Development Status :: 5 - Production/Stable
        Intended Audience :: Developers
        Intended Audience :: Financial and Insurance Industry
        Intended Audience :: Other Audience
        Intended Audience :: Science/Research
        License :: OSI Approved :: GNU General Public License v3 (GPLv3)
        Operating System :: OS Independent
        Programming Language :: Python
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: 3.6
        """.split('\n') if c.strip()],  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
  keywords = 'real estate solar irradiation sunlight sun amount wattage house room floor window obstacle',
  author = 'Arne Bachmann',
  author_email = 'ArneBachmann@users.noreply.github.com',
  maintainer = 'Arne Bachmann',
  maintainer_email = 'ArneBachmann@users.noreply.github.com',
  url = 'http://github.com/ArneBachmann/realestate-sunamount',
  license = 'Mozilla Public License Version 2.0 (MPL-2.0)',
  packages = find_packages(),  # should return ["rese"]
  package_dir = {"rese": "rese"},
  package_data = {"rese": ["../LICENSE", "../*.md", "*.coco"]},
  include_package_data = False,  # if True, will *NOT* package the data!
  zip_safe = False
)
