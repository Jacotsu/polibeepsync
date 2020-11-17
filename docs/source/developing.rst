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

Modifying the user interface
----------------------------

The user interface, the resources and the slot connections **must** be modified with QT5 designer.
This makes the code cleaner and thus more maintainable.

Once you've made your changes you must regenerate the corresponding python files with the following
commands.

.. code:: bash

    pyside2-uic --from-imports user_interfaces/add_course_popup.ui -o polibeepsync/ui/ui_add_course_popup.py
    pyside2-uic --from-imports user_interfaces/main_form.ui -o polibeepsync/ui/ui_main_form.py
    pyside2-rcc uglytheme.qrc -o polibeepsync/ui/uglytheme_rc.py

In the future this will be done through a makefile rule


Bug Tracker
------------

In order to file a bug report, you should
`open a issue <https://github.com/jacotsu/polibeepsync/issues>`_
on github.

.. toctree::
  :maxdepth: 1

  debug
