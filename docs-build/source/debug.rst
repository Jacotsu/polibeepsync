How to debug
=============

In order to debug, you should open a terminal and pass the ``--debug DEBUG_LEVEL``
option. DEBUG_LEVEL can be one of the following

1. debug
2. info
3. warning
4. error
5. critical

You should usually use *info*.

Platform-specific commands follow.

On Windows
--------------

Open ``cmd.exe`` and write
::
  polibeepsync --debug DEBUG_LEVEL


On Linux
---------

If you used the direct installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In a terminal
::
    polibeepsync --debug DEBUG_LEVEL


If you used the virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In a terminal
::
    source ~/polibeepsync-venv/bin/activate
    polibeepsync --debug DEBUG_LEVEL

