.. image:: https://api.travis-ci.org/Jacotsu/polibeepsync.svg?branch=master
  :alt: Build status

.. image:: https://pypip.in/license/poliBeePsync/badge.svg
    :target: https://pypi.python.org/pypi/poliBeePsync/
    :alt: License

.. image:: https://pypip.in/download/poliBeePsync/badge.svg?period=day
    :target: https://pypi.python.org/pypi/poliBeePsync/
    :alt: Downloads today

.. image:: https://pypip.in/download/poliBeePsync/badge.svg?period=week
    :target: https://pypi.python.org/pypi/poliBeePsync/
    :alt: Downloads this week

.. image:: https://pypip.in/download/poliBeePsync/badge.svg?period=month
    :target: https://pypi.python.org/pypi/poliBeePsync/
    :alt: Downloads this month

.. image:: https://pypip.in/version/poliBeePsync/badge.svg?text=version
    :target: https://pypi.python.org/pypi/poliBeePsync/
    :alt: Version

.. image:: https://pypip.in/py_versions/poliBeePsync/badge.svg
    :target: https://pypi.python.org/pypi/poliBeePsync/
    :alt: Supported Python versions

.. image:: https://pypip.in/implementation/poliBeePsync/badge.svg
    :target: https://pypi.python.org/pypi/poliBeePsync/
    :alt: Supported Python implementations

.. image:: https://pypip.in/status/poliBeePsync/badge.svg
    :target: https://pypi.python.org/pypi/poliBeePsync/
    :alt: Development Status

.. image:: https://pypip.in/wheel/poliBeePsync/badge.svg
    :target: https://pypi.python.org/pypi/poliBeePsync/
    :alt: Wheel Status

.. image:: https://pypip.in/egg/poliBeePsync/badge.svg
    :target: https://pypi.python.org/pypi/poliBeePsync/
    :alt: Egg Status




PoliBeePsync
============

This program, aimed at students of Politecnico di Milano, synces a local
folder with files uploaded by professors on the
`BeeP <https://beep.metid.polimi.it>`_ platform.

This code is in the beta stage. Documentation is under construction
`here <https://jacotsu.github.io/polibeepsync>`_.

Changelog
=========

0.4.3 (2019-01-22)
------------------
Fix
~~~
- Url encoded filenames are now saved with a proper name [DCDRJ]
- Login doesn't fail when password change prompt is shown [DCDRJ]

0.4.2 (2018-12-27)
------------------
New
~~~
- New icon (thanks to `Davide Depau <https://github.com/Depau>`_) [DCDRJ]

Fix
~~~
- Now the manually inserted root folder path is no longer ignored [DCDRJ]
- Now course names without a year or with accents are supported [DCDRJ]
- Now minimize and restore work properly [DCDRJ]
- Now the tar file includes the new_gui.ui file [DCDRJ]

0.4.1 (2018-12-26)
------------------
Fix
~~~
- Included .ui file in pip package [DCDRJ]

0.4.0 (2018-12-26)
------------------
New
~~~
- Implemented beep's liferay json api (thanks to `davethecipo <https://github.com/davethecipo>`_ and
  `edomora97 <https://github.com/edomora97>`_)[DCDRJ]

Fix
~~~
- Now if the settings file is corrupted the application doesn't crash [DCDRJ]
- Updated docs link in check new version code [DCDRJ]
- Updated tests [DCDRJ]
- Code cleanup [DCDRJ]

0.3.3 (2018-12-14)
------------------
New
~~~
- Set 'info' as default logging level [DCDRJ]
- Logging is now less cluttered [DCDRJ]
- Download size are now shown in human readable format during logging [DCDRJ]
- Terminal logging and console now are synced [DCDRJ]

Fix
~~~
- Code cleanup [DCDRJ]
- Improved QT integration [DCDRJ]
- Reduced number of connection threads, now beep shouldn't drop connections [DCDRJ]


0.3.2 (2018-08-04)
------------------
New
~~~
- Multithread download [DCDRJ]
- Material design theme implemented [DCDRJ]

Fix
~~~
- Increased download code robustness [GV]
- Redesigned interface in qt designer for increased modularity [DCDRJ]
- Regenerated documentation [DCDRJ]

0.3.1 (2018-07-25)
------------------
New
~~~
- PySide2 support added for python3.6 [DCDRJ]

Fix
~~~
- Fixed Gui code where app couldn't find button [DCDRJ]
- Now sync message label works [DCDRJ]
- Fixed login error [DCDRJ]
- Fixed labels typos [DCDRJ]
- Added status label [DCDRJ]
- Fixed sync code [DCDRJ]


0.3.0 (2015-01-12)
-------------------

New
~~~

Progress bar for each course.


0.2.4 (2015-01-06)
-------------------

Fix
~~~

- KeyError fixed (bug #12)

0.2.3 (2015-01-06)
-------------------

Fix
~~~

- pyparsing dependency added.

Changes
~~~~~~~~

- Add travis-ci configuration

0.2.2 (2015-01-03)
-------------------

Fix
~~~

- Deny zero-length save folder names #10. [Davide Olianas]


0.2.1 (2015-01-03)
------------------

Changes
~~~~~~~

- Only links containing real courses are processed.
  [Davide Olianas]


0.2.0 (2015-01-02)
------------------

New
~~~

- --hidden option works #6. [Davide Olianas]

Changes
~~~~~~~

- --debug option works #6. [Davide Olianas]


0.1.5 (2015-01-02)
------------------

New
~~~

- Basic working configuration for logging. [Davide Olianas]

Changes
~~~~~~~

- Add debugging statements. [Davide Olianas]

- Style fixes. [Davide Olianas]

- Remove unused import. [Davide Olianas]

- Add .ico icon for Windows. [Davide Olianas]

- Store __version__ in __init__.py and use setuptools. [Davide Olianas]

