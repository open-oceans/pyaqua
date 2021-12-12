#!/usr/bin/python
# -*- coding: utf-8 -*-

__copyright__ = """

MIT License

Copyright (c) 2021 Samapriya Roy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


"""
__license__ = "MIT License"

import requests
import json
import sys
import pkg_resources
import argparse
import time
import csv
import getpass
import os
import pytz
import datetime
from itertools import groupby
from dateutil import parser
from os.path import expanduser
from bs4 import BeautifulSoup
from timezonefinder import TimezoneFinder
from dateutil.relativedelta import *

headers = {
    'authority': 'ocean-systems.uc.r.appspot.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'accept': 'application/json, text/html',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'crossdomain': 'true',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://aqualink.org',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://aqualink.org/',
    'accept-language': 'en-US,en;q=0.9',
}


class Solution:
    def compareVersion(self, version1, version2):
        versions1 = [int(v) for v in version1.split(".")]
        versions2 = [int(v) for v in version2.split(".")]
        for i in range(max(len(versions1), len(versions2))):
            v1 = versions1[i] if i < len(versions1) else 0
            v2 = versions2[i] if i < len(versions2) else 0
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
        return 0


ob1 = Solution()

# Get package version
def pyaqua_version():
    url = "https://pypi.org/project/pyaqua/"
    source = requests.get(url)
    html_content = source.text
    soup = BeautifulSoup(html_content, "html.parser")
    company = soup.find("h1")
    vcheck = ob1.compareVersion(
        company.string.strip().split(" ")[-1],
        pkg_resources.get_distribution("pyaqua").version,
    )
    if vcheck == 1:
        print(
            "\n"
            + "========================================================================="
        )
        print(
            "Current version of pyaqua is {} upgrade to lastest version: {}".format(
                pkg_resources.get_distribution("pyaqua").version,
                company.string.strip().split(" ")[-1],
            )
        )
        print(
            "========================================================================="
        )
    elif vcheck == -1:
        print(
            "\n"
            + "========================================================================="
        )
        print(
            "Possibly running staging code {} compared to pypi release {}".format(
                pkg_resources.get_distribution("pyaqua").version,
                company.string.strip().split(" ")[-1],
            )
        )
        print(
            "========================================================================="
        )


#pyaqua_version()

def sitelist(sname):
    sid_list=[]
    response = requests.get('https://ocean-systems.uc.r.appspot.com/api/sites')
    for items in response.json():
        if items['sensorId'] is not None:
            sid_list.append({items['name']:items['id']})
    print(f'Found a total of {len(sid_list)} sites with spotters'+'\n')
    for site in sid_list:
        for name,sid in site.items():
            if sname is not None and sname.lower() == name.lower():
                print(f'{name}: {sid}')
            elif sname is None:
                print(f'{name}: {sid}')

def sitelist_from_parser(args):
    sitelist(sname=args.name)

# ### Get a quick check on a site
def site_live(sid):
    live_data = requests.get(f'https://ocean-systems.uc.r.appspot.com/api/sites/{sid}/live_data')
    if live_data.status_code==200:
        print(json.dumps(live_data.json(),indent=4))
    else:
        print('Failed to get live data with error code {}'.format(live_data.status_code))
def sitelive_from_parser(args):
    site_live(sid=args.sid)

# def spot_check(spot_id):
#     if not spot_id.startswith("SPOT-"):
#         spot_id = f"SPOT-{spot_id}"
#     dic = {}
#     obj = TimezoneFinder()
#     headers = {
#         "token": tokenize(),
#     }
#     response = requests.get(
#         f"https://api.sofarocean.com/api/latest-data?spotterId={spot_id}",
#         headers=headers,
#     )
#     if response.status_code == 200:
#         spotter = response.json()
#         print(f"Fetching info for Spotter {spot_id}" + "\n")
#         for key, value in spotter["data"].items():
#             if key != "frequencyData" and key != "track" and key != "waves":
#                 dic[key] = value
#             # print(key,value)
#         latitude = spotter["data"]["waves"][-1]["latitude"]
#         longitude = spotter["data"]["waves"][-1]["longitude"]
#         time_zone = obj.timezone_at(lat=float(latitude), lng=float(longitude))
#         tz = pytz.timezone(time_zone)
#         now_utc = parser.parse(spotter["data"]["waves"][-1]["timestamp"])
#         now_kl = now_utc.replace(tzinfo=pytz.utc).astimezone(tz)
#         dic["last updated (UTC time)"] = str(now_utc)
#         dic["last updated (spotter local time)"] = str(now_kl)
#         dic["latitude"] = spotter["data"]["waves"][-1]["latitude"]
#         dic["longitude"] = spotter["data"]["waves"][-1]["longitude"]
#         print(json.dumps(dic, indent=2, sort_keys=False))
#     else:
#         print(
#             f"Spot check failed with error code {response.status_code}: {response.json()['message']}"
#         )


# def spotcheck_from_parser(args):
#     spot_check(spot_id=args.sid)


# def spot_data(spot_id, dtype, folder):  #'SPOT-0222'
#     waves_list = []
#     wind_list = []
#     sst_list = []
#     if not spot_id.startswith("SPOT-"):
#         spot_id = f"SPOT-{spot_id}"
#     obj = TimezoneFinder()
#     params = {
#         "spotterId": [spot_id],
#         "includeSurfaceTempData": True,
#         "includeWindData": True,
#     }
#     headers = {
#         "token": tokenize(),
#     }
#     response = requests.get(
#         "https://api.sofarocean.com/api/wave-data", headers=headers, params=params
#     )
#     if response.status_code == 200:
#         spotter = response.json()
#         print("\n" + f"Fetching info for Spotter {spot_id}" + "\n")
#         if (
#             not "surfaceTemp" in spotter["data"]
#             or len(spotter["data"]["surfaceTemp"]) == 0
#             and dtype == "sst"
#         ):
#             sys.exit("No surfaceTemp data found")
#         else:
#             for readings in spotter["data"]["surfaceTemp"]:
#                 readings["date"] = readings["timestamp"].split("T")[0]
#                 readings["spotter_id"] = spot_id
#                 sst_list.append(readings)
#         if (
#             not "waves" in spotter["data"]
#             or len(spotter["data"]["waves"]) == 0
#             and dtype == "wave"
#         ):
#             sys.exit("No waves data found")
#         else:
#             for readings in spotter["data"]["waves"]:
#                 readings["date"] = readings["timestamp"].split("T")[0]
#                 readings["spotter_id"] = spot_id
#                 waves_list.append(readings)
#         if (
#             not "wind" in spotter["data"]
#             or len(spotter["data"]["wind"]) == 0
#             and dtype == "wind"
#         ):
#             sys.exit("No wind data found")
#         else:
#             for readings in spotter["data"]["wind"]:
#                 readings["date"] = readings["timestamp"].split("T")[0]
#                 readings["spotter_id"] = spot_id
#                 wind_list.append(readings)
#     else:
#         sys.exit(
#             f"Failed with status_code: {response.status_code}: {response.json()['message']}"
#         )

#     if dtype == "wave":
#         csv_columns = [
#             "significantWaveHeight",
#             "peakPeriod",
#             "meanPeriod",
#             "peakDirection",
#             "peakDirectionalSpread",
#             "meanDirection",
#             "meanDirectionalSpread",
#             "timestamp",
#             "latitude",
#             "longitude",
#             "date",
#             "spotter_id",
#         ]
#         main_list = waves_list
#     elif dtype == "wind":
#         csv_columns = [
#             "speed",
#             "direction",
#             "seasurfaceId",
#             "latitude",
#             "longitude",
#             "timestamp",
#             "date",
#             "spotter_id",
#         ]
#         main_list = wind_list
#     elif dtype == "sst":
#         csv_columns = [
#             "degrees",
#             "latitude",
#             "longitude",
#             "timestamp",
#             "date",
#             "spotter_id",
#         ]
#         main_list = sst_list
#     # define a fuction for key
#     def key_func(k):
#         return k["date"]

#     # sort INFO data by 'company' key.
#     INFO = sorted(main_list, key=key_func)

#     for key, value in groupby(INFO, key_func):
#         print(f"Processing {spot_id}_{key}_{dtype}.csv")
#         dict_data = list(value)
#         try:
#             with open(
#                 os.path.join(folder, f"{spot_id}_{key}_{dtype}.csv"), "w"
#             ) as csvfile:
#                 writer = csv.DictWriter(
#                     csvfile, fieldnames=csv_columns, delimiter=",", lineterminator="\n"
#                 )
#                 writer.writeheader()
#                 for data in dict_data:
#                     writer.writerow(data)
#         except IOError:
#             print("I/O error")


# def spot_data_from_parser(args):
#     spot_data(spot_id=args.sid, dtype=args.dtype, folder=args.folder)


def main(args=None):
    parser = argparse.ArgumentParser(description="Simple CLI for Aqualink API")
    subparsers = parser.add_subparsers()

    parser_sitelist = subparsers.add_parser(
        "sitelist", help="Print lists of Site Name and ID with spotters"
    )
    optional_named = parser_sitelist.add_argument_group("Optional named arguments")
    optional_named.add_argument("--name", help="Pass site name", default=None)
    parser_sitelist.set_defaults(func=sitelist_from_parser)

    parser_sitelive = subparsers.add_parser(
        "site-live", help="Get most recent/live infor from a site"
    )
    required_named = parser_sitelive.add_argument_group("Required named arguments.")
    required_named.add_argument("--sid", help="Site ID", required=True)
    parser_sitelive.set_defaults(func=sitelive_from_parser)

    # parser_spot_data = subparsers.add_parser(
    #     "spot-data", help="Export Spotter Data based on Spotter ID & grouped by date"
    # )
    # required_named = parser_spot_data.add_argument_group("Required named arguments.")
    # required_named.add_argument("--sid", help="Spotter ID", required=True)
    # required_named.add_argument(
    #     "--dtype", help="Data type: wind/wave/sst", required=True
    # )
    # required_named.add_argument(
    #     "--folder", help="Folder to export CSV data", required=True
    # )
    # parser_spot_data.set_defaults(func=spot_data_from_parser)

    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()
