Installation (Windows)
=======================

Install `python 3.7 <https://www.python.org/>`_, making sure to enable the
option "Add python.exe to Path".

.. image:: addtopath.png

Open the program ``cmd.exe``, then write
::
    pip install poliBeePsync

.. image:: pipinstall.png

...and press ``Enter`` (if you get an error telling that ``pip`` is not a recognized command, logout and re-login, then write the command). Words will appear, wait. Once it says it has finished,
look where it has been installed.

.. image:: whereisinstalled.png

In the image, you can see that it has been installed to ``C:\Python37\Scripts``.
Browse to that folder, right click on ``polibeepsync-gui.exe`` and
choose ``create shortcut``.

.. image:: createshortcut.png

Now you can copy the shortcut wherever you want and use it to start the
program.

You may want to add a `nicer icon <https://raw.githubusercontent.com/jacotsu/polibeepsync/master/icons/uglytheme/48x48/polibeepsync.ico>`_
to the shortcut, by right-clicking on the shortcut, choosing ``Properties``
and then clicking on ``Choose icon``.



Start the application automatically at boot (Windows)
-----------------------------------------------------

Right click on the shortcut and select ``copy``.
Open the ``run`` program (you can find it by typing ``run`` after pressing
the "Windows" key), write
::
	%AppData%
	
and then click ``Ok``. In the opened folder, go to ``Microsoft\Windows\Start Menu\Programs\Startup``
and choose ``paste shortcut``. The next time you boot, the program will 
start automatically.


Upgrade
==========

Open the program ``cmd.exe``, Write the following and press ``Enter``
::
    pip install --upgrade poliBeePsync


How to remove
===============

Open ``cmd.exe``
::
    pip uninstall poliBeePsync requests appdirs beautifulsoup4 PySide

...and then press ``Enter`` to execute the command. When it asks for
confirmation, type ``y`` and press ``Enter`` again (it will ask multiple times,
one for every package).
The next step is removing the folders in which settings and data are saved.

Open your user folder, make hidden files and folders visible, open
``AppData\Local``
and remove the folder named ``poliBeePsync``.
