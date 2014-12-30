.. PoliBeePsync documentation master file, created by
   sphinx-quickstart on Wed Dec 17 19:18:55 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to poliBeePsync's documentation!
========================================

PoliBeePsync is a simple GUI program, aimed at students of Politecnico di
Milano, which purpose is to sync the files loaded by professors onto the
`BeeP platform <https://beep.metid.polimi.it>`_.

This software is in the beta stage and the documentation is under
construction.


License
========

PoliBeePsync is distributed under the GNU General Public License v3 or later
(GPLv3+). The full license text is available `here <http://www.gnu.org/copyleft/gpl.html>`_.

Images
=======

.. image:: pbs-general.png
	:alt: The general settings tab.

.. image:: pbs-courses.png
	:alt: The list of courses available.

How to Install/Remove
============================

Installation (and removal) instructions are provided in the :doc:`installation` page for
Windows and Linux. The program hasn't been tested on Mac OS X yet.

Quickstart
============

After the :doc:`installation`, you need to configure the application.
You can find more in the :doc:`quickstart` page.

Support
=======

Feel free to send an e-mail to ubuntupk AT gmail DOT com.

For developers
===============

Bug Tracker
------------

In order to file a bug report, you should
`open a issue <https://github.com/davethecipo/polibeepsync/issues>`_
on github.

Source code
------------


Source code is available on `<https://github.com/davethecipo/polibeepsync>`_.
I recommend using a virtualenv in order to develop; the command used to create
one may be different from the one I show below. The following instructions are
for Linux.
::

    git clone https://github.com/davethecipo/polibeepsync.git
    cd polibeepsync
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    pip install -r test-requirements.txt



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

