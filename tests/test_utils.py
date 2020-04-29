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
from polibeepsync.utils import raw_date_to_datetime
from polibeepsync.common import GMT1


class TestTimestampParsing:
    def test_timestampWithDotHourFormat(self):
        raw_date = ' 08/10/15 14.15 '
        gmt = GMT1()
        correct_date = datetime(2015, 10, 8, 14, 15, tzinfo=gmt)
        calculated_date = raw_date_to_datetime(raw_date, gmt)
        assert correct_date == calculated_date

    def test_timestampWithSemiColonHourFormat(self):
        raw_date = ' 08/10/15 14:15 '
        gmt = GMT1()
        correct_date = datetime(2015, 10, 8, 14, 15, tzinfo=gmt)
        calculated_date = raw_date_to_datetime(raw_date, gmt)
        assert correct_date == calculated_date
