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
""" Tool to import BrewPi CSV export into InfluxDB database.
"""
import argparse
import os

from brewmon import BrewMon, DEFAULT_TCP_PORT


def parse_args():
    parser = argparse.ArgumentParser(description="Import BrewPi beer in CSV format to InfluxDB")
    parser.add_argument('--host', type=str, required=False,
                        default='influxdb',
                        help='InfluxDB http API hostname')
    parser.add_argument('--port', type=int, required=False, default=DEFAULT_TCP_PORT,
                        help='InfluxDB http API port')
    parser.add_argument('--database', type=str, required=False,
                        default='brewpi',
                        help='InfluxDB database name')
    parser.add_argument("--beer-name", required=False, help="beer name to use instead of the CSV filename")
    parser.add_argument('--udp', action='store_true', help="Use UDP protocol instead of TCP")
    parser.add_argument('--ispindel', action='store_true', help="The CSV file is an iSpindel export")
    parser.add_argument('--verbose', action='store_true')

    parser.add_argument("CSV_FILE")
    return parser.parse_args()


def import_beer_file(brewmon, file_path, beer_name):
    print("# Importing beer '" + beer_name + "' from file: '" + file_path + "'")
    date_start = None
    date_end = None
    with open(file_path) as csvfile:
        for line in csvfile:
            row = line.split(';')
            if date_start is None:
                date_start = row[0]
            date_end = row[0]
            brewmon.add_beer_row(beer_name, row)
    brewmon.flush()
    print("# " + str(brewmon.get_count()) + " rows imported from: " + date_start + " to " + date_end)


def import_ispindel_file(brewmon, file_path):
    print("# Importing iSpindel from file: '" + file_path + "'")
    with open(file_path) as csvfile:
        for line in csvfile:
            row = line.split(',')
            if row[0] == "name":
                # skip header
                continue
            brewmon.add_ispindel_row(row)
    brewmon.flush()
    print("# " + str(brewmon.get_count()) + " rows imported")


def main():
    args = parse_args()
    if args.beer_name is None:
        args.beer_name = os.path.splitext(os.path.basename(args.CSV_FILE))[0]

    if args.ispindel:
        brewmon = BrewMon(host=args.host, port=args.port, udp=args.udp, verbose=args.verbose, time_precision="n")
        import_ispindel_file(brewmon, args.CSV_FILE)
    else:
        brewmon = BrewMon(host=args.host, port=args.port, udp=args.udp, verbose=args.verbose)
        import_beer_file(brewmon, args.CSV_FILE, args.beer_name)


if __name__ == "__main__":
    main()
