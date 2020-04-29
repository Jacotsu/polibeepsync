__copyright__ = """Copyright 2020 Davide Olianas (ubuntupk@gmail.com), Di
Campli Raffaele (dcdrj.pub@gmail.com)."""

__license__ = """This f is part of poliBeePsync.
poliBeePsync is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

poliBeePsync is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with poliBeePsync. If not, see <http://www.gnu.org/licenses/>.
"""

from datetime import datetime
import logging
import time
import re
from PySide2.QtCore import Qt


def raw_date_to_datetime(rawdate, gmt):
    day = int(rawdate.split(' ')[1].split('/')[0])
    month = int(rawdate.split(' ')[1].split('/')[1])
    year = int('20' + rawdate.split(' ')[1].split('/')[2])
    hour = int(re.split('\.|:', rawdate.split(' ')[2])[0])
    minute = int(re.split('\.|:', rawdate.split(' ')[2])[1])
    complete_date = datetime(year, month, day, hour, minute,
                             tzinfo=gmt)
    return complete_date


def debug_dump(data, logger=logging.getLogger(), min_level=logging.DEBUG):
    if logger.level <= min_level:
        with open(f'Polybeepsync-dump-{time.time()}', 'wb') as dump:
            dump.write(data)


def debug_request_response(response, logger=logging.getLogger(),
                           min_level=logging.DEBUG):
    if logger.level <= min_level:

        with open(f'Polybeepsync-dump-{time.time()}', 'wb') as dump:
            dump.write(response.text)


def init_checkbox(qt_checkbox, dictionary, key, state_slot=None):
    logger = logging.getLogger()
    try:
        state = Qt.Checked if dictionary[key] == str(True) else Qt.Unchecked
        qt_checkbox.setCheckState(state)
    except KeyError:
        qt_checkbox.setCheckState(Qt.Unchecked)
        logger.warning(f'{key} is missing from the dictionary'
                       'Qt.Unchecked has been set as fallback')

    if state_slot:
        qt_checkbox.stateChanged.connect(state_slot)
    else:
        logger.warning('No state change slot has been '
                       f'specified {qt_checkbox}')
