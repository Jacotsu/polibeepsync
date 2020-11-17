How to debug
=============

In order to debug, you should open a terminal and pass the ``--log-level DEBUG_LEVEL``
option. `DEBUG_LEVEL` can be one of the following:

* `debug`
* `info`
* `warning`
* `error`
* `critical`

You should usually use `info`.

Platform-specific commands follow.

On Windows
--------------

Open ``cmd.exe`` and write

.. code-block:: bash

  polibeepsync --log-level DEBUG_LEVEL


On Linux
---------

If you used the direct installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In a terminal

.. code-block:: bash

    polibeepsync --log-level DEBUG_LEVEL


If you used the virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In a terminal

.. code-block:: bash

    source ~/polibeepsync-venv/bin/activate
    polibeepsync --log-level DEBUG_LEVEL


How to enable QT5 verbose logging
=================================

In some cases it may be useful to get a log file of the underlying QT5 framework, especially when there are
problems with the graphicals interface that are not shown in the normal debug log.
To enable thee verbose logging mode you have to set the following environment variable
:code:`QT_LOGGING_RULES="*.debug=true"`.

To start polibeepsync in full verbose logging mode use the following command

.. code:: bash

    QT_LOGGING_RULES="*.debug=true" polibeepsync --log-level debug

Command line options
====================

poliBeePsync supports the following command line options, none of these are persistent

+---------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| Option                                                  | Description                                                                                               |
+=========================================================+===========================================================================================================+
| :code:`-h, --help`                                      | shows the help message                                                                                    |
+---------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| :code:`--hidden`                                        | Don't show the main window, just the icon in the system tray                                              |
+---------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| :code:`--log-level {debug,info,warning,error,critical}` | Choose logging report verbosity                                                                           |
+---------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| :code:`-s, --use_theme`                                 | Choose Qt theme over gtk                                                                                  |
+---------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| :code:`--default-timeout DEFAULT_TIMEOUT`               | Choose how long (in seconds) the connection should remain open before assuming that the server is offline |
+---------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| :code:`--sync-interval SYNC_INTERVAL`                   | Choose how often (in minutes) the courses files should be synced                                          |
+---------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
| :code:`--sync-on-startup`                               | Synces the courses files on startup                                                                       |
+---------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
