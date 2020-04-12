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
