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

import argparse
import datetime
import json
import os
import sys
import webbrowser
from collections import Counter

import pandas as pd
import pkg_resources
import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import *
from natsort import natsorted
from rapidfuzz import fuzz

from .argofloats import argoexp

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


pyaqua_version()


# Go to the readMe
def readme():
    try:
        a = webbrowser.open("https://samapriya.github.io/pyaqua/", new=2)
        if a == False:
            print("Your setup does not have a monitor to display the webpage")
            print(" Go to {}".format("https://samapriya.github.io/pyaqua/"))
    except Exception as e:
        print(e)


def read_from_parser(args):
    readme()


def sitelist(sname, status):
    sid_list = []
    hobo_list = []
    status_list = []
    response = requests.get("https://ocean-systems.uc.r.appspot.com/api/sites")
    stat_type = ["maintenance", "deployed", "shipped", "lost"]
    if status is not None and status not in stat_type:
        sys.exit(
            "Status type not supported choose from: maintenance|deployed|shipped|lost"
        )
    for items in response.json():
        if items["sensorId"] is not None:
            if status is not None and items["status"] == status:
                sid_list.append([items["name"], items["id"]])
                status_list.append(items["status"])
            elif status is None:
                sid_list.append([items["name"], items["id"]])
                status_list.append(items["status"])
        elif items["hasHobo"] is True:
            hobo_list.append([items["name"], items["id"]])
    if sname is not None:
        for site in sid_list:
            rat = fuzz.ratio(sname.lower(), site[0].lower())
            if sname.lower() in site[0].lower() or rat > 75:
                print(f"{site[0]}: {site[1]}")
    elif sname is None:
        if sid_list:
            print("\n" + "================Spotter Locations================")
            print(
                "\n".join([" : ".join([str(cell) for cell in row])
                          for row in sid_list])
            )
    if hobo_list and sname is None:
        print("\n" + "================Hobo Sensor Locations================")
        print("\n".join([" : ".join([str(cell) for cell in row])
              for row in hobo_list]))
    print(
        "\n" + f"Found a total of {len(sid_list)} sites with spotters" + "\n")
    print(
        "\n" + f"Found a total of {len(hobo_list)} sites with hobo logger" + "\n")
    print("Spotter status distribution :")
    print(json.dumps(Counter(status_list)))


def sitelist_from_parser(args):
    sitelist(sname=args.name, status=args.status)


# Site alert
def sitealert(level, device):
    sid_list = []
    hobo_list = []
    overall_list = []
    status_list = []
    if level is None:
        level = 1  # only pick sites with alert

    response = requests.get("https://ocean-systems.uc.r.appspot.com/api/sites")
    if response.status_code == 200:
        for alert_sites in response.json():
            if device == "spotter" and alert_sites["sensorId"] is not None:
                if alert_sites["collectionData"]["temp_alert"] == 0:
                    alert_level = "no alert"
                elif alert_sites["collectionData"]["temp_alert"] == 1:
                    alert_level = "watch"
                elif alert_sites["collectionData"]["temp_alert"] == 2:
                    alert_level = "warning"
                elif alert_sites["collectionData"]["temp_alert"] == 3:
                    alert_level = "Level-1"
                elif alert_sites["collectionData"]["temp_alert"] == 4:
                    alert_level = "Level-2"
                if alert_sites["collectionData"]["temp_alert"] >= level:
                    sid_list.append(
                        [
                            alert_sites["name"],
                            alert_sites["id"],
                            alert_sites["collectionData"]["temp_alert"],
                        ]
                    )
                    status_list.append(alert_level)
            elif device == "hobo" and alert_sites["hasHobo"] is True:
                if alert_sites["collectionData"]["temp_alert"] == 0:
                    alert_level = "no alert"
                elif alert_sites["collectionData"]["temp_alert"] == 1:
                    alert_level = "watch"
                elif alert_sites["collectionData"]["temp_alert"] == 2:
                    alert_level = "warning"
                elif alert_sites["collectionData"]["temp_alert"] == 3:
                    alert_level = "Level-1"
                elif alert_sites["collectionData"]["temp_alert"] == 4:
                    alert_level = "Level-2"
                if alert_sites["collectionData"]["temp_alert"] >= level:
                    hobo_list.append(
                        [
                            alert_sites["name"],
                            alert_sites["id"],
                            alert_sites["collectionData"]["temp_alert"],
                        ]
                    )
                    status_list.append(alert_level)
            elif device is None:
                try:
                    if alert_sites["collectionData"]["temp_alert"] == 0:
                        alert_level = "no alert"
                    elif alert_sites["collectionData"]["temp_alert"] == 1:
                        alert_level = "watch"
                    elif alert_sites["collectionData"]["temp_alert"] == 2:
                        alert_level = "warning"
                    elif alert_sites["collectionData"]["temp_alert"] == 3:
                        alert_level = "Level-1"
                    elif alert_sites["collectionData"]["temp_alert"] == 4:
                        alert_level = "Level-2"
                    if alert_sites["collectionData"]["temp_alert"] >= level:
                        overall_list.append(
                            [
                                alert_sites["name"],
                                alert_sites["id"],
                                alert_sites["collectionData"]["temp_alert"],
                            ]
                        )
                        status_list.append(alert_level)
                except Exception as e:
                    print(e)
    else:
        sys.exit("\n" + f"Page returned status code :{response.status_code}")
    if device is not None and device == "spotter":
        print(
            "\n"
            + f"================Spotter Alert Locations & Level >={level}================"
        )
        print("\n".join([" : ".join([str(cell) for cell in row])
              for row in sid_list]))
        print(
            "\n"
            + f"Found a total of {len(sid_list)} sites with spotters & active alert level >= {level}"
            + "\n"
        )
    elif device is not None and device == "hobo":
        print(
            "\n" + f"================Hobo Sensor Locations & Level >=1================"
        )
        print("\n".join([" : ".join([str(cell) for cell in row])
              for row in hobo_list]))
        print(
            "\n"
            + f"Found a total of {len(hobo_list)} hobo sensor list sites with active alert level >= {level}"
            + "\n"
        )
    elif device is None:
        print(
            "\n"
            + f"================Overall sites Locations & Level >={level}================"
        )
        print(
            "\n".join([" : ".join([str(cell) for cell in row])
                      for row in overall_list])
        )
        print("\n")

    print("Level Key ===> 0: No alert, 1: watch, 2: warning, 3:Level-1, 4:Level-2")
    print("\n" + "Alert level distribution :")
    print(json.dumps(Counter(status_list)))


def sitealert_from_parser(args):
    sitealert(level=args.level, device=args.device)


# Get a quick check on a site
def site_info(sid, ext):
    response = requests.get(
        f"https://ocean-systems.uc.r.appspot.com/api/sites/{sid}")
    if response.status_code == 200:
        keys_to_remove = ["admins", "historicalMonthlyMean",
                          "stream", "videoStream"]
        site_inf = response.json()
        if ext is not None and ext == "historical":
            ext = "historicalMonthlyMean"
            keys_to_remove.remove(ext)
        elif ext is not None and ext == "admins":
            ext = "admins"
            keys_to_remove.remove(ext)
        elif ext is None:
            pass
        else:
            sys.exit("Extra info key not found")
        for key in keys_to_remove:
            site_inf.pop(key)
        print(json.dumps(site_inf, indent=4))
    else:
        print(
            f"Failed to get site information with error {response.status_code}: {response.text}"
        )


def siteinfo_from_parser(args):
    site_info(sid=args.sid, ext=args.extra)


# Get a quick check on a site
def site_live(sid):
    live_data = requests.get(
        f"https://ocean-systems.uc.r.appspot.com/api/sites/{sid}/live_data"
    )
    if live_data.status_code == 200:
        print(json.dumps(live_data.json(), indent=4))
    else:
        print(
            "Failed to get live data with error code {}".format(
                live_data.status_code)
        )


def sitelive_from_parser(args):
    site_live(sid=args.sid)


# Get daily data for a site
def site_daily(delta, sid, dtype, fpath, start, end):
    if start and end is not None:
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
        end = datetime.datetime.strptime(end, "%Y-%m-%d")
        past_utc = start.strftime("%Y-%m-%dT%H:%M:%SZ")
        current_utc = end.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        d = datetime.datetime.utcnow()
        current_utc = d.strftime("%Y-%m-%dT%H:%M:%SZ")
        if delta is None:
            delta = 3
        past_utc = d + relativedelta(months=-int(delta))
        past_utc = past_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    response = requests.get(
        f"https://ocean-systems.uc.r.appspot.com/api/sites/{sid}")
    if response.status_code == 200:
        resp = response.json()["polygon"]["coordinates"]
        lng = resp[0]
        lat = resp[1]
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
        overall = []
        for resp in response.json():
            if dset is not None:
                ext = {
                    key: value
                    for key, value in resp.items()
                    if dset.lower() in key
                    or dset.capitalize() in key
                    or dset.upper() in key
                }
                ext_dt = {key: value for key,
                          value in resp.items() if key == "date"}
                combined = ext_dt.copy()
                combined.update(ext)
                overall.append(combined)
            else:
                overall.append(resp)
        if fpath is not None:
            if dtype is None:
                dtype = "overall"
            fname = os.path.join(fpath, f"spotter_{dtype}_{sid}.csv")
            df = pd.DataFrame(overall)
            print(f"Exporting daily data to {fname}")
            if lat and lng is not None:
                df["latitude"] = lat
                df["longitude"] = lng
            df.dropna(axis=1, how="all", inplace=True)
            df = df.loc[:, (df != 0).any(axis=0)]
            df.to_csv(fname, index=False)
        else:
            print(json.dumps(overall, indent=2))
    else:
        print(
            f"Daily date fetch failed with error: {response.status_code} & {response.text}"
        )


def sitedaily_from_parser(args):
    site_daily(
        sid=args.sid,
        delta=args.months,
        dtype=args.dtype,
        fpath=args.fpath,
        start=args.start,
        end=args.end,
    )


# Function to export time series data from site
def site_timeseries(delta, sid, dtype, fpath, start, end):
    if start and end is not None:
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
        end = datetime.datetime.strptime(end, "%Y-%m-%d")
        past_utc = start.strftime("%Y-%m-%dT%H:%M:%SZ")
        current_utc = end.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        d = datetime.datetime.utcnow()
        current_utc = d.strftime("%Y-%m-%dT%H:%M:%SZ")
        if delta is None:
            delta = 3
        past_utc = d + relativedelta(months=-int(delta))
        past_utc = past_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"Time series from {past_utc} to {current_utc}")

    response = requests.get(
        f"https://ocean-systems.uc.r.appspot.com/api/sites/{sid}")
    if response.status_code == 200:
        resp = response.json()["polygon"]["coordinates"]
        lng = resp[0]
        lat = resp[1]
    if dtype is not None:
        if dtype == "temp":
            metrics = "bottom_temperature,top_temperature"
        if dtype == "wave":
            metrics = "significant_wave_height,wave_peak_period,wave_mean_direction"
        if dtype == "sat_temp":
            metrics = "satellite_temperature"
        if dtype == "wind":
            metrics = "wind_speed,wind_direction"
        if dtype == "alert":
            metrics = "alert,weekly_alert"
        if dtype == "anomaly":
            metrics = "sst_anomaly"
        if dtype == "dhw":
            metrics = "dhw"
    elif dtype is None:
        metrics = "bottom_temperature,top_temperature,significant_wave_height,wave_peak_period,wave_mean_direction,satellite_temperature,wind_speed,wind_direction,alert,weekly_alert,sst_anomaly,dhw"
    else:
        print("Datatype is not supported")

    params = {
        "start": past_utc,
        "end": current_utc,
        "metrics": metrics,
        "hourly": "true",
    }

    response = requests.get(
        f"https://ocean-systems.uc.r.appspot.com/api/time-series/sites/{sid}",
        headers=headers,
        params=json.dumps(params),
    )
    metric_list = []
    if response.status_code == 200:
        resp = response.json()
        for metric in resp:
            metric_list.append(metric)
        if dtype is not None and dtype in metric_list:
            metric_list = [dtype]
        for metric in natsorted(metric_list):
            print(f"Processing spotter_{metric}_{sid}")
            fname = os.path.join(fpath, f"spotter_{metric}_{sid}.csv")
            try:
                df = pd.DataFrame(resp[metric]["spotter"]["data"])
            except Exception as error:
                df = pd.DataFrame(resp[metric]["noaa"]["data"])
            if lat and lng is not None:
                df["latitude"] = lat
                df["longitude"] = lng
            df.dropna(axis=1, how="all", inplace=True)
            df = df.loc[:, (df != 0).any(axis=0)]
            df.to_csv(fname, index=False)
    else:
        print(
            f"Time series failed with error: {response.status_code} & {response.text}"
        )


def timeseries_from_parser(args):
    site_timeseries(
        sid=args.sid,
        delta=args.months,
        dtype=args.dtype,
        fpath=args.fpath,
        start=args.start,
        end=args.end,
    )


# Function to export time series data from site
def site_argofloats(sid, fpath, start, end, radius):
    response = requests.get(
        f"https://ocean-systems.uc.r.appspot.com/api/sites/{sid}")
    if response.status_code == 200:
        resp = response.json()["polygon"]["coordinates"]
        lng = resp[0]
        lat = resp[1]
    else:
        sys.exit(
            f"Failed to fetch {sid} coordinates with error: {response.status_code}"
        )
    try:
        argoexp(
            fpath=fpath,
            lat=lat,
            lng=lng,
            start=start,
            end=end,
            radius=radius,
            geometry=None,
            plid=None,
        )
    except Exception as e:
        print(e)


def argo_from_parser(args):
    site_argofloats(
        sid=args.sid,
        start=args.start,
        end=args.end,
        fpath=args.fpath,
        radius=args.radius,
    )


def main(args=None):
    parser = argparse.ArgumentParser(description="Simple CLI for Aqualink API")
    subparsers = parser.add_subparsers()

    parser_read = subparsers.add_parser(
        "readme", help="Go to the web based pyaqua readme page"
    )
    parser_read.set_defaults(func=read_from_parser)

    parser_sitelist = subparsers.add_parser(
        "site-list", help="Print lists of Site Name and ID with spotters"
    )
    optional_named = parser_sitelist.add_argument_group(
        "Optional named arguments")
    optional_named.add_argument("--name", help="Pass site name", default=None)
    optional_named.add_argument(
        "--status",
        help="Site status from maintenance|deployed|shipped|lost",
        default=None,
    )
    parser_sitelist.set_defaults(func=sitelist_from_parser)

    parser_sitealert = subparsers.add_parser(
        "site-alert", help="Print site alerts for sites with spotters"
    )
    optional_named = parser_sitealert.add_argument_group(
        "Optional named arguments")
    optional_named.add_argument(
        "--level",
        help="Level 0-4 no-alert|watch|warning|Level-1|Level-2",
        default=None,
        type=int,
        choices=range(0, 5),
    )
    optional_named.add_argument(
        "--device",
        help="spotter|hobo",
        default=None,
    )
    parser_sitealert.set_defaults(func=sitealert_from_parser)

    parser_siteinfo = subparsers.add_parser(
        "site-info", help="Print detailed information for a site"
    )
    required_named = parser_siteinfo.add_argument_group(
        "Required named arguments.")
    required_named.add_argument("--sid", help="Site ID", required=True)
    optional_named = parser_siteinfo.add_argument_group(
        "Optional named arguments")
    optional_named.add_argument(
        "--extra", help="extra info keywords: historical/admins", default=None
    )
    parser_siteinfo.set_defaults(func=siteinfo_from_parser)

    parser_sitelive = subparsers.add_parser(
        "site-live", help="Get most recent/live info from a site"
    )
    required_named = parser_sitelive.add_argument_group(
        "Required named arguments.")
    required_named.add_argument("--sid", help="Site ID", required=True)
    parser_sitelive.set_defaults(func=sitelive_from_parser)

    parser_sitedaily = subparsers.add_parser(
        "site-daily", help="Print daily data info for a site"
    )
    required_named = parser_sitedaily.add_argument_group(
        "Required named arguments.")
    required_named.add_argument("--sid", help="Site ID", required=True)
    optional_named = parser_sitedaily.add_argument_group(
        "Optional named arguments")
    optional_named.add_argument(
        "--months",
        help="Total number of months in the past from today (default=1)",
        default=None,
    )
    optional_named.add_argument(
        "--start", help="Start date for daily data in format YYYY-MM-DD", default=None
    )
    optional_named.add_argument(
        "--end", help="End date for daily data in format YYYY-MM-DD", default=None
    )
    optional_named.add_argument(
        "--dtype", help="Data type: wind/wave/temp", default=None
    )
    optional_named.add_argument(
        "--fpath", help="Full path to folder to export daily data as CSV", default=None
    )
    parser_sitedaily.set_defaults(func=sitedaily_from_parser)

    parser_timeseries = subparsers.add_parser(
        "site-timeseries", help="Exports timeseries data for a site"
    )
    required_named = parser_timeseries.add_argument_group(
        "Required named arguments.")
    required_named.add_argument("--sid", help="Site ID", required=True)
    required_named.add_argument(
        "--fpath", help="Folder path for export", required=True)
    optional_named = parser_timeseries.add_argument_group(
        "Optional named arguments")
    optional_named.add_argument(
        "--months",
        help="Total number of months in the past from today (default=3)",
        default=None,
    )
    optional_named.add_argument(
        "--start", help="Start date for daily data in format YYYY-MM-DD", default=None
    )
    optional_named.add_argument(
        "--end", help="End date for daily data in format YYYY-MM-DD", default=None
    )
    optional_named.add_argument(
        "--dtype",
        help="Data type: wind/wave/temp/sat_temp/alert/anomaly/dhw",
        default=None,
    )

    parser_timeseries.set_defaults(func=timeseries_from_parser)

    parser_argo = subparsers.add_parser(
        "site-argo", help="Exports coincident argofloat data for a site"
    )
    required_named = parser_argo.add_argument_group(
        "Required named arguments.")
    required_named.add_argument("--sid", help="Site ID", required=True)
    required_named.add_argument(
        "--start", help="Start date in format YYYY-MM-DD", required=True
    )
    required_named.add_argument(
        "--end", help="End date in format YYYY-MM-DD", required=True
    )
    required_named.add_argument(
        "--fpath", help="Folder path for export", required=True)
    optional_named = parser_argo.add_argument_group("Optional named arguments")
    optional_named.add_argument(
        "--radius", help="Search radius in kilometers", default=None
    )
    parser_argo.set_defaults(func=argo_from_parser)

    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()
