.. image:: https://badge.waffle.io/davethecipo/polibeepsync.png?label=ready&title=Ready 
 :target: https://waffle.io/davethecipo/polibeepsync
 :alt: 'Stories in Ready'

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

.. image:: https://pypip.in/license/poliBeePsync/badge.svg
    :target: https://pypi.python.org/pypi/poliBeePsync/
    :alt: License



PoliBeePsync
============

This program, aimed at students of Politecnico di Milano, synces a local
folder with files uploaded by professors on the
`BeeP <https://beep.metid.polimi.it>`_ platform.

This code is in the beta stage. Documentation is under construction
`here <http://www.davideolianas.com/polibeepsync/index.html>`_.

Changelog
=========

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

