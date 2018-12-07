#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BrewPi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BrewPi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BrewPi.  If not, see <http://www.gnu.org/licenses/>.
#
# Contributors:
#   Benoit Delbosc
""" Unit test for brewmon lib
"""
import unittest

from brewmon import BrewMon

# CSV line
# date;beer_temp;beer_setting_temp;annotation;fridge_temp;fridge_setting_temp;annotation;state;room_temp
OK_LINE = 'Dec 14 2018 10:24:19;18.11;18.50;"Some annotation";17.63;19.10;"Some comment";0;17.63'
OK_LINE_OLD = 'Sep 26 2012 00:01:00;18.96;19.00;None;19.94;19.60;None'

BAD_LINE_1 = 'XXX 14 2018 10:24:19;18.11;18.50;"Some annotation";17.63;19.10;"Some comment";0;17.63'
BAD_LINE_2 = 'Dec 14 2018 10:24:19;18.11;18.50;"Some annotation";17.63'
BAD_LINE_3 = 'Dec 14 2018 10:24:19;"Wrong temp";18.50;"Some annotation";17.63;19.10;"Some comment";0;17.63'
BAD_LINE_4 = ''
BAD_LINE_5 = None


class TestBrewMon(unittest.TestCase):

    def test_invalid_udp_server(self):
        # sending valid data with UDP fail silently
        brewmon = BrewMon(host="localhost", port=1234, udp=True)
        self.assertIsNotNone(brewmon)
        brewmon.publish_line("someBeer", OK_LINE)
        brewmon.publish_line("someBeer", OK_LINE_OLD)
        self.assertEqual(2, brewmon.get_count())

    def test_invalid_line(self):
        # invalid line or beer name should not crash brewpi
        brewmon = BrewMon(udp=True)
        self.assertIsNotNone(brewmon)
        brewmon.publish_line("someBeer", BAD_LINE_1)
        brewmon.publish_line("someBeer", BAD_LINE_2)
        brewmon.publish_line("someBeer", BAD_LINE_3)
        brewmon.publish_line("someBeer", BAD_LINE_4)
        brewmon.publish_line("someBeer", BAD_LINE_5)
        brewmon.publish_line("", OK_LINE)
        brewmon.publish_line(None, OK_LINE)
        # nothing was sent
        self.assertEqual(0, brewmon.get_count())


if __name__ == '__main__':
    unittest.main()
