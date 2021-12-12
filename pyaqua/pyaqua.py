from __future__ import print_function

__copyright__ = """
    Copyright 2021 Samapriya Roy
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__license__ = "Apache 2.0"

import requests
import json
import sys
import pkg_resources
import argparse
import time
import csv
import os
import datetime
from rapidfuzz import fuzz
from dateutil import parser
from bs4 import BeautifulSoup
from dateutil.relativedelta import *

headers = {
    "authority": "ocean-systems.uc.r.appspot.com",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    "accept": "application/json, text/html",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "crossdomain": "true",
    "sec-ch-ua-platform": '"Windows"',
    "origin": "https://aqualink.org",
    "sec-fetch-site": "cross-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://aqualink.org/",
    "accept-language": "en-US,en;q=0.9",
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


# pyaqua_version()


def sitelist(sname):
    sid_list = []
    response = requests.get("https://ocean-systems.uc.r.appspot.com/api/sites")
    for items in response.json():
        if items["sensorId"] is not None:
            sid_list.append({items["name"]: items["id"]})
    print(f"Found a total of {len(sid_list)} sites with spotters" + "\n")
    for site in sid_list:
        for name, sid in site.items():
            if sname is not None:
                rat = fuzz.ratio(sname.lower(), name.lower())
            if sname is not None and rat > 70:
                print(f"{name}: {sid}")
            elif sname is None:
                print(f"{name}: {sid}")


def sitelist_from_parser(args):
    sitelist(sname=args.name)


#### Get a quick check on a site
def site_live(sid):
    live_data = requests.get(
        f"https://ocean-systems.uc.r.appspot.com/api/sites/{sid}/live_data"
    )
    if live_data.status_code == 200:
        print(json.dumps(live_data.json(), indent=4))
    else:
        print(
            "Failed to get live data with error code {}".format(live_data.status_code)
        )


def sitelive_from_parser(args):
    site_live(sid=args.sid)


#### Get daily data for a site
def site_daily(delta, sid, dtype):
    d = datetime.datetime.utcnow()
    current_utc = d.strftime("%Y-%m-%dT%H:%M:%SZ")
    if delta is None:
        delta = 3
    past_utc = d + relativedelta(months=-delta)
    past_utc = past_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"Daily data from {past_utc} to {current_utc} for site {sid}")
    params = {
        "start": past_utc,
        "end": current_utc,
    }
    if dtype == "temp":
        dset = "temperature"
    elif dtype == "wind":
        dset = "wind"
    elif dtype == "wave":
        dset = "wave"
    elif dtype is None:
        dset = None
    else:
        sys.exit("Data type not supported")
    response = requests.get(
        f"https://ocean-systems.uc.r.appspot.com/api/sites/{sid}/daily_data",
        headers=headers,
        params=params,
    )
    if response.status_code == 200:
        for resp in response.json():
            if dset is not None:
                ext = {
                    key: value
                    for key, value in resp.items()
                    if dset.lower() in key
                    or dset.capitalize() in key
                    or dset.upper() in key
                }
                ext_dt = {key: value for key, value in resp.items() if key == "date"}
                combined = ext_dt.copy()
                combined.update(ext)
                print(json.dumps(combined, indent=2))
            else:
                print(json.dumps(resp, indent=2))


def sitedaily_from_parser(args):
    site_daily(sid=args.sid, delta=args.months, dtype=args.dtype)


def main(args=None):
    parser = argparse.ArgumentParser(description="Simple CLI for Aqualink API")
    subparsers = parser.add_subparsers()

    parser_sitelist = subparsers.add_parser(
        "site-list", help="Print lists of Site Name and ID with spotters"
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

    parser_sitedaily = subparsers.add_parser(
        "site-daily", help="Print daily data info for a site"
    )
    required_named = parser_sitedaily.add_argument_group("Required named arguments.")
    required_named.add_argument("--sid", help="Site ID", required=True)
    optional_named = parser_sitedaily.add_argument_group("Optional named arguments")
    optional_named.add_argument(
        "--months", help="Total number of months from today", default=None
    )
    optional_named.add_argument(
        "--dtype", help="Data type: wind/wave/temp", default=None
    )
    parser_sitedaily.set_defaults(func=sitedaily_from_parser)

    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()
