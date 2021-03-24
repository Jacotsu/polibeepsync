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

from datetime import datetime, timedelta
import logging
import time
import re
import requests
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


def debug_dump(data, logger=logging.getLogger(), extension='',
               min_level=logging.DEBUG):
    if logger.level <= min_level:
        extension = f'.{extension}' if extension else ''
        with open(f'Polibeepsync-dump-{time.time()}{extension}', 'wb') as dump:
            dump.write(data)


def debug_dump_request_response(response, logger=logging.getLogger(),
                                min_level=logging.DEBUG):
    debug_dump(response.text.encode(), logger, 'html', min_level)


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

def check_course_url(user_obj, course_url):
    url_regex = '^(?:https://|http://|)beep.metid.polimi.it/web/([\w\d\-\_]+)'
    match = re.match(url_regex, course_url)

    if match:
        try:
            # If theres a match and we get a page then it's probably a valid
            # course. We return the friendly url
            if user_obj.get_page(course_url):
                return match.group(1)
        except requests.TooManyRedirects:
            pass

    return False


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


@static_vars(last_times={})
def fps_limiter(target_fps, key):
    try:
        time_delta = timedelta(milliseconds=1/target_fps)
        current_time = datetime.now()
        if current_time - fps_limiter.last_times[key] > time_delta:
            return True
        else:
            return False
    except KeyError:
        fps_limiter.last_times[key] = current_time
        return True
