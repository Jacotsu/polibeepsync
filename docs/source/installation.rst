Installation
=============

Clicke `here <https://www.dropbox.com/sh/piyhj83x7ymhnw8/AAAzzA53UwuY4popz3v0kK-na?dl=0>`_
and click on

* ``buildwin64`` if you're using a 64bit version of Windows
* ``buildwin32`` if you're using a 32bit version of Windows


Now, on the upper right corner, click ``download/download as a .zip``.
After the download has finished, extract the .zip archive.
You can start the program by double-clicking on the ``qtgui`` program.
Keep reading if you want to create an easy shortcut and/or start the 
program automatically at boot.

For the moment, don't download the linux version (I'm examining why it doesn't
work); instead, download the package through pip (tested for python-3.4)
::

    pip install poliBeePsync

How to create a shortcut (Windows)
-----------------------------------

Select the
file named ``qtgui``, right click, ``create shortcut``. Now, right click on
the shortcut, select ``properties``, go to the ``General`` tab, change its name
to something you can remember easily (polibeepsync is a good choice). Go
to the ``shortcut`` tab, select ``Change icon``, select ``browse`` and then
the .ico file available in the downloaded folder.

You can now use the shortcut to start the program (copy/paste it where 
you want).

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

How to remove
=================

For both Windows and Linux, simply remove the folder you downloaded. The next
step is removing the folders in which settings and data are saved.

On Windows
------------

Open your user folder, make hidden files and folders visible, open 
``AppData\Local``
and remove the folder named ``poliBeePsync``.

On Linux
-----------

Remove ``~/.config/poliBeePsync`` and ``~/.local/share/poliBeePsync``
::
    rm -R ~/.config/poliBeePsync
    rm -R ~/.local/share/poliBeePsync
