from datetime import datetime
import logging
import time


def raw_date_to_datetime(rawdate, gmt):
    day = int(rawdate.split(' ')[1].split('/')[0])
    month = int(rawdate.split(' ')[1].split('/')[1])
    year = int('20' + rawdate.split(' ')[1].split('/')[2])
    hour = int(rawdate.split(' ')[2].split('.')[0])
    minute = int(rawdate.split(' ')[2].split('.')[1])
    complete_date = datetime(year, month, day, hour, minute,
                             tzinfo=gmt)
    return complete_date


def debug_dump(data, min_level=logging.DEBUG):
    if logging.getLogger().level >= min_level:
        with open(f'Polybeepsync-dump-{time.time()}', 'wb') as dump:
            dump.write(data)
