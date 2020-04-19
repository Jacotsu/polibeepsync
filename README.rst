.. image:: https://api.travis-ci.org/Jacotsu/polibeepsync.svg?branch=master
    :alt: Build status

.. image:: https://pypip.in/license/poliBeePsync/badge.svg
    :target: https://pypi.python.org/pypi/poliBeePsync/
    :alt: License

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

.. image:: https://pypip.in/status/poliBeePsync/badge.svg
    :target: https://pypi.python.org/pypi/poliBeePsync/
    :alt: Development Status

.. image:: https://pypip.in/wheel/poliBeePsync/badge.svg
    :target: https://pypi.python.org/pypi/poliBeePsync/
    :alt: Wheel Status

PoliBeePsync |donate|
=====================
.. |donate| image:: https://liberapay.com/assets/widgets/donate.svg
    :target: https://liberapay.com/jacotsu/donate
    :width: 10%
    :alt: Donate using liberapay

This program, aimed at students of Politecnico di Milano, synces a local
folder with files uploaded by professors on the
`BeeP <https://beep.metid.polimi.it>`_ platform.

This code is in the beta stage. Documentation is under construction
`here <https://jacotsu.github.io/polibeepsync>`_.

Installation
============

Ubuntu 19.10
--------------
::

  sudo add-apt-repository ppa:jacotsu/polibeepsync
  sudo apt update
  sudo apt install python3-polibeepsync

Arch
-----
::

  yay -S polibeepsync

Windows
--------
Download the exe file from the `latest release <https://github.com/Jacotsu/polibeepsync/releases/latest>`_
and open the downloaded file.

MAC OS
------
Download the .app.zip file from the `latest release <https://github.com/Jacotsu/polibeepsync/releases/latest>`_ and
then drag it from the Downloads to Applications, `CTRL+Right click` polibeepsync's icon and click `open`.


Manual
------
**Use this only if the other methods don't work**
::

  pip3 install --user polibeepsync


Changelog
=========

0.7.2 (2020-04-19)
------------------

Fix
~~~
- New courses are now synced by default [DCDRJ]
- Fixed bug that would ignore timeout command line option when downloading files [DCDRJ]

0.7.1 (2020-04-15)
-------------------

New
~~~
- Removed Beep's embedded certificate as it's no longer necessary [DCDRJ]
- Added timeout flag [DCDRJ]

Fix
~~~
- Increased default timeout to 10 seconds to tolerate slow servers [DCDRJ]
- Greatly reduced window's executable size [DCDRJ]

0.7.0 (2020-04-13)
------------------
New
~~~
- Added support for MAC OS Catalina [DCDRJ]
- Added more startup options [DCDRJ]

  - `--sync-on-startup`: lets you override your settings file, and sync
    the course files on application startup
  - `--sync-interval`: lets you override your settings file sync frequency
- Added built in backup certificate to mitigate malformed beep ones [DCDRJ]

Fix
~~~
- Added missing dependencies to setup.py [DCDRJ]
- Minor UI improvements [DCDRJ]
- Minor code cleanup [DCDRJ]
- Increased info logging [DCDRJ]
- Fixed bug that hid some logging messages [DCDRJ]
- Added a default file version (0) to manage files that have None [DCDRJ]
- Added exception handling for invalid uuids [DCDRJ]
- Renewed copyright year in documentation [DCDRJ]
- Changed default professor name separator from `/` to `;` [DCDRJ]
- Updated documentation [DCDRJ]

0.6.0 (2020-03-10)
------------------
New
~~~
- Set 8 hours as new default sync time [DCDRJ]
- Added references in about info [DCDRJ]
- Added donate button link [DCDRJ]
- Renewed copyright year and explicitly added license to each file [DCDRJ]

Fix
~~~
- Improved name simplification code [DCDRJ]
- Now course files destination folders contain professor names [DCDRJ]
- Updated tests to match the new simplification algorithm [DCDRJ]
- Minor test code cleanup [DCDRJ]
- Removed some cruft [DCDRJ]
- Removed old icons [DCDRJ]
- Reorganized resources [DCDRJ]

0.5.2 (2019-10-25)
------------------
Fix
~~~
- Reimplemented webscraping as default download method due to BeeP's JSON API deactivation [DCDRJ]

0.5.1 (2019-07-11)
------------------
Fix
~~~
- Signalslot is now fetched from pypi [DCDRJ]
- Included icon in PPA [DCDRJ]
- Modified GUI layout [DCDRJ]
- Made checkboxes bigger [DCDRJ]
- Checkboxes are now more centered [DCDRJ]
- Moved login form and sync button out of the settings tab [DCDRJ]


0.5.0 (2019-07-09)
------------------
New
~~~
- PPA package release [DCDRJ]
- Windows installer release [DCDRJ]
- Automated multiplatform building with Makefile [DCDRJ]

Fix
~~~
- Improved documentation [DCDRJ]



0.4.4 (2019-03-08)
------------------
New
~~~
- The password is now saved in the system keyring instead of the dump file [DCDRJ]

Fix
~~~
- Status bar now shows when sync is finished [DCDRJ]
- Now thread priority is properly set [DCDRJ]
- Removed tests from package [DCDRJ]
- Now password and person code are updated when the input field looses focus [DCDRJ]


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

