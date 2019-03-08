#!/usr/bin/env bash
py.test --cov polibeepsync tests
pyflakes polibeepsync/qtgui.py
pyflakes polibeepsync/common.py
pyflakes polibeepsync/tests/*.py
flake8 polibeepsync/qtgui.py
flake8 polibeepsync/common.py
flake8 tests/*.py
coverage html
xdg-open htmlcov/index.html
