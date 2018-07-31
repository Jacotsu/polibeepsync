Installation (Linux)
======================

.. note:: Every distribution uses slightly different names for the
    ``python`` command. I'll show commands for Ubuntu 14.04.

Install python 3.4 using the package manager of your distribution.
In Ubuntu, it should be already installed.
You also need ``pip`` and other programs (to compile the library ``PySide``)
::
    sudo apt-get upgrade && sudo apt-get update && sudo apt-get install python3-pip  build-essential cmake libqt4-dev

You have two choices now: install poliBeePsync directly or in a "virtual
environment", which is a fancy name for a folder holding a copy of python,
under which poliBeePsync will be installed. This implies that you can easily
remove the application by just removing the folder of the virtual environment.

I recommend using a virtual environment, although it's slightly more
difficult.

Direct installation
----------------------
In a terminal issue the command
::
    sudo pip3 install poliBeePsync

Once it has finished, you can start the application with the command
``polibeepsync-gui``.

I recommend adding a custom menu entry to the application menu of your
Desktop Environment. As an icon, you can use `this one <https://raw.githubusercontent.com/davethecipo/polibeepsync/master/icons/uglytheme/48x48/polibeepsync.png>`_.

Installation inside a virtual environment
------------------------------------------

1. Create a virtual environment.
    Open a terminal and type
    ::
      sudo pip3 install virtualenv
      virtualenv-3.4 polibeepsync-venv
      source polibeepsync-venv/bin/activate

    You can choose the name of folder, I chose ``polibeepsync-venv``.

2. Install the program.
    Open a terminal and write
    ::
        pip3 install poliBeePsync

    Press ``Enter`` to confirm and wait.



Once it has finished, you can start the application with the command
``polibeepsync-gui`` if the virtual environment is active (this is done with
the third command shown in point 1). You can automate this by creating a
shell script with the following content
::
    cd ~/polibeepsync-venv
    source bin/activate
    polibeepsync-gui &

I recommend adding a custom menu entry to the application menu of your
Desktop Environment. As an icon, you can use `this one <https://raw.githubusercontent.com/davethecipo/polibeepsync/master/icons/uglytheme/48x48/polibeepsync.png>`_.
In this case, you would create an entry for the shell script.


Upgrade
===========

If you installed poliBeePsync directly, open a terminal, write the following
code and press ``Enter``
::
    pip install --upgrade poliBeePsync

If you used a virtual environment, before issuing the command, remember to
activate the virtual environment
::
    cd ~/polibeepsync-venv
    source bin/activate

How to remove
====================

Uninstall poliBeePsync by writing this code in a terminal
::
    pip uninstall poliBeePsync requests appdirs beautifulsoup4 PySide

...and then pressing ``Enter`` to execute the command. When it asks for
confirmation, type ``y`` and press ``Enter`` again (it will ask multiple times,
one for every package).

Remove ``~/.config/poliBeePsync`` and ``~/.local/share/poliBeePsync``
::
    rm -R ~/.config/poliBeePsync
    rm -R ~/.local/share/poliBeePsync
