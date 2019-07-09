Developing
===============

Source code
------------

Source code is available on `<https://github.com/jacotsu/polibeepsync>`_.
I recommend using a virtualenv in order to develop; the command used to create
one may be different from the one I show below. The following instructions are
for Linux.

.. code-block:: bash

    git clone https://github.com/jacotsu/polibeepsync.git
    cd polibeepsync
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
    pip3 install -r test-requirements.txt

.. toctree::
  :maxdepth: 1

  modules

Bug Tracker
------------

In order to file a bug report, you should
`open a issue <https://github.com/jacotsu/polibeepsync/issues>`_
on github.

.. toctree::
  :maxdepth: 1

  debug
