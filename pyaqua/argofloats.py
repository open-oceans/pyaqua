import json
import math
import os
import platform
import subprocess
import sys
import time
import webbrowser
from os.path import expanduser

import geojson
import pandas as pd
import pkg_resources
import requests
from area import area
from tenacity import retry, stop_after_attempt, wait_exponential

if str(platform.system().lower()) == "windows":
    # Get python runtime version
    version = sys.version_info[0]
    try:
        import pipwin

        if pipwin.__version__ == "0.5.0":
            pass
        else:
            a = subprocess.call(
                "{} -m pip install pipwin==0.5.0".format(sys.executable),
                shell=True,
                stdout=subprocess.PIPE,
            )
            b = subprocess.call(
                "{} -m pip install wheel".format(sys.executable),
                shell=True,
                stdout=subprocess.PIPE,
            )
            subprocess.call("pipwin refresh", shell=True)
        """Check if the pipwin cache is old: useful if you are upgrading porder on windows
        [This section looks if the pipwin cache is older than two weeks]
        """
        home_dir = expanduser("~")
        fullpath = os.path.join(home_dir, ".pipwin")
        if not os.path.exists(fullpath):
            subprocess.call("pipwin refresh", shell=True)
        file_mod_time = os.stat(fullpath).st_mtime
        if int((time.time() - file_mod_time) / 60) > 90000:
            print("Refreshing your pipwin cache")
            subprocess.call("pipwin refresh", shell=True)
    except ImportError:
        a = subprocess.call(
            "{} -m pip install pipwin==0.5.0".format(sys.executable),
            shell=True,
            stdout=subprocess.PIPE,
        )
        subprocess.call("pipwin refresh", shell=True)
    except Exception as e:
        print(e)
    try:
        import gdal
    except ImportError:
        try:
            from osgeo import gdal
        except ModuleNotFoundError:
            subprocess.call("pipwin install gdal", shell=True)
    except ModuleNotFoundError or ImportError:
        subprocess.call("pipwin install gdal", shell=True)
    except Exception as e:
        print(e)
    try:
        import pyproj
    except ImportError:
        subprocess.call("pipwin install pyproj", shell=True)
    except Exception as e:
        print(e)
    try:
        import shapely
    except ImportError:
        subprocess.call("pipwin install shapely", shell=True)
    except Exception as e:
        print(e)
    try:
        import fiona
    except ImportError:
        subprocess.call("pipwin install fiona", shell=True)
    except Exception as e:
        print(e)
    try:
        import geopandas as gpd
    except ImportError:
        subprocess.call("pip install geopandas", shell=True)
    except Exception as e:
        print(e)
import geopandas as gpd

headers = {
    "Connection": "keep-alive",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Language": "en-US,en;q=0.9",
}

profile_list = []

################################################ Date block #################################################################


def numOfDays(date1, date2):
    return (date2 - date1).days


def date_range(start, end):
    from datetime import datetime

    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    days = numOfDays(start, end)
    intv = math.ceil(days / 30)
    diff = (end - start) / intv
    for i in range(intv):
        yield (start + diff * i).strftime("%Y-%m-%dT%H:%M:%SZ")
    yield end.strftime("%Y-%m-%dT%H:%M:%SZ")


######################################################geometry block ################################################################################
def getarea(geom):
    obj = {"type": "Polygon", "coordinates": []}
    obj["coordinates"] = geom
    poly_area = area(obj)
    return poly_area / 1000000


# point to square buffer function
def generate_buffer_meter(lat, lng, radius):
    data = pd.DataFrame({"Longitude": [lng], "Latitude": [lat]})
    data = gpd.GeoDataFrame(
        data,
        geometry=gpd.points_from_xy(data.Longitude, data.Latitude, crs="epsg:4326"),
    )
    data = data.to_crs("+proj=aeqd +units=m  +x_0=0 +y_0=0")
    data["geometry"] = data["geometry"].buffer(radius, cap_style=3)
    data = data.to_crs("epsg:4326")
    bound = json.loads(data.to_json())
    coord = bound["features"][0]["geometry"]["coordinates"]
    return coord


######################### Global profile searches #################################################################


def get_monthly_profile_pos(month, year):
    url = f"https://argovis.colorado.edu/selection/profiles/{month}/{year}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return f"Error: Unexpected response {resp}"
    monthlyProfilePos = resp.json()
    return monthlyProfilePos


def parse_meta_into_df(profiles):
    # initialize dict
    df = pd.DataFrame(profiles)
    if df.shape[0] == 0:
        return "error: no dataframes"
    return df


def global_profiles(fpath, start, end, pid, bgc):
    key_list = {"pid": "platform_number", "bgc": "containsBGC", "allprofiles": "all"}
    if pid is not None:
        key = "pid"
        value = int(pid)
    elif bgc is not None:
        key = "bgc"
        value = bool(bgc)
    elif pid is None and bgc is None:
        key = "allprofiles"
        value = "allprofiles"
    if key is not None and key in key_list:
        keyword = key_list[key]
    elif key is not None and key not in key_list:
        sys.exit(f"Key {key} not found")

    start = "-".join(start.split("-")[0:2])
    end = "-".join(end.split("-")[0:2])
    periods = list(pd.period_range(start, end, freq="M").strftime("%Y-%m"))
    for period in periods:
        print(f"Searching globally within {period} for {keyword}:{value}")
        month = int(str(period).split("-")[1])
        year = int(str(period).split("-")[0])
        metaProfiles = get_monthly_profile_pos(month, year)
        metaDf = parse_meta_into_df(metaProfiles)
        dict = {"lat": "latitude", "lon": "longitude"}
        metaDf.rename(columns=dict, inplace=True)
        if keyword is not None and keyword != "all":
            metaDf_sorted = metaDf.loc[metaDf[keyword] == value]
        else:
            metaDf_sorted = metaDf
        filepath = os.path.join(fpath, f"global_{year}_{month}_{keyword}-{value}.csv")
        if metaDf_sorted.size > 0:
            print(f"Exporting global search within {period} to {filepath}")
            metaDf_sorted.to_csv(filepath, index=False)


######################### Profile Map find all profile ids for give aoi and time ################################


@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(4))
def profile_id(params):
    response = requests.get(
        "https://argovis.colorado.edu/selection/profiles/map",
        headers=headers,
        params=params,
    )
    if response.status_code == 200 and len(response.json()) > 0:
        for items in response.json():
            profile_list.append(items["_id"])
        return profile_list
    elif response.status_code != 200:
        raise Exception


######################### Profile measurements and exporter ################################
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(2))
def profiler_bgc(plid, fpath):
    filepath = os.path.join(fpath, f"argoprofile_bgc_{plid}.csv")
    if not os.path.exists(filepath):
        pf = requests.get(f"https://argovis.colorado.edu/catalog/profiles/{plid}")
        if pf.status_code == 200:
            profile = pf.json()
            bgc_keys = profile["bgcMeas"][0].keys()
            df_bgc = pd.DataFrame(columns=bgc_keys)
            profileDf = pd.DataFrame(profile["bgcMeas"])
            profileDf["cycle_number"] = profile["cycle_number"]
            profileDf["profile_id"] = profile["_id"]
            profileDf["latitude"] = profile["lat"]
            profileDf["longitude"] = profile["lon"]
            profileDf["date"] = profile["date"]
            df_bgc = pd.concat([df_bgc, profileDf], sort=False)
            try:
                print(f"Exporting bgc profile to {filepath}")
                df_bgc.to_csv(filepath, index=False)
            except Exception as e:
                print(e)
        elif response.status_code != 200:
            raise Exception
    else:
        print(f"File already exists SKIPPING: {os.path.basename(filepath)}")


@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(2))
def profiler(plid, fpath):
    filepath = os.path.join(fpath, f"argoprofile_core_{plid}.csv")
    if not os.path.exists(filepath):
        pf = requests.get(f"https://argovis.colorado.edu/catalog/profiles/{plid}")
        if pf.status_code == 200:
            profile = pf.json()
            meas_keys = profile["measurements"][0].keys()
            df = pd.DataFrame(columns=meas_keys)
            profileDf = pd.DataFrame(profile["measurements"])
            profileDf["cycle_number"] = profile["cycle_number"]
            profileDf["profile_id"] = profile["_id"]
            profileDf["latitude"] = profile["lat"]
            profileDf["longitude"] = profile["lon"]
            profileDf["date"] = profile["date"]
            df = pd.concat([df, profileDf], sort=False)
            try:
                print(f"Exporting core profile to {filepath}")
                df.to_csv(filepath, index=False)
            except Exception as e:
                print(e)
        elif response.status_code != 200:
            raise Exception
    else:
        print(f"File already exists SKIPPING: {os.path.basename(filepath)}")


################################### Export all profiles per platform #################################################################
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(2))
def profile_catalog(pid):
    url = f"https://argovis.colorado.edu/catalog/platforms/{pid}"
    resp = requests.get(url)
    if not resp.status_code == 200:
        raise Exception
    elif resp.status_code == 200:
        platformProfiles = resp.json()
    return platformProfiles


def get_profiles(profiles):
    meas_keys = profiles[0]["measurements"][0].keys()
    df = pd.DataFrame(columns=meas_keys)
    for profile in profiles:
        profileDf = pd.DataFrame(profile["measurements"])
        profileDf["cycle_number"] = profile["cycle_number"]
        profileDf["profile_id"] = profile["_id"]
        profileDf["latitude"] = profile["lat"]
        profileDf["longitude"] = profile["lon"]
        profileDf["date"] = profile["date"]
        df = pd.concat([df, profileDf], sort=False)
    return df


def platform2profiles(pid, fpath):
    if fpath is None:
        fpath = expanduser("~")
    profiles = profile_catalog(pid)
    pidf = get_profiles(profiles)
    platform_counts = pidf["profile_id"].nunique()
    print(f"Total unique profiles: {platform_counts}")
    print(f"Total measurements: {pidf.shape[0]}")
    filepath = os.path.join(fpath, f"all_profiles_core-{pid}.csv")
    print(f"Exporting core profile to {filepath}")
    pidf.to_csv(filepath, index=False)


def overview():
    response = requests.get(
        "https://argovis.colorado.edu/selection/overview", headers=headers
    )
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Overview failed with error code {response.status_code}")


# BGC parameter list
bgc_paramerters = {
    "psal": "Salinity (psu)",
    "bbp700": "Particle backscattering at 700nm (1/m)",
    "doxy": "Dissolved oxygen (micromole/kg)",
    "ph": "pH in situ total",
    "chla": "Chlorophyll-A (mg/m3)",
    "pres": "Pressure (dbar)",
    "nitrate": "Nitrate (micromole/kg)",
    "temp": "Temperature (celcius)",
    "down_irradiance443": "Downwelling irradiance at 443nm (W/m^2/nm)",
    "down_irradiance412": "Downwelling irradiance at 412nm (W/m^2/nm)",
    "down_irradiance490": "Downwelling irradiance at 490nm (W/m^2/nm)",
    "cdom": "Concentration of colored dissolved organic matter in sea water (ppb)",
    "downwelling_par": "Downwelling photosynthetically available radiation (uMol Quanta/m^2/sec)",
}


def platform_metadata(pid):
    response = requests.get(
        f"https://argovis.colorado.edu/catalog/platform_metadata/{pid}", headers=headers
    )
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
        """Check to see if profile is BGC and get BGC keys"""
        platform_url = f"https://argovis.colorado.edu/catalog/platforms/{pid}"
        resp = requests.get(platform_url)
        if resp.status_code == 200 and resp.json()[0].get("containsBGC") == True:
            print("\n" + "Profile contains BGC data with parameters" + "\n")
            for key in resp.json()[0].get("bgcMeasKeys"):
                if bgc_paramerters.get(key):
                    print(f"{key} : {bgc_paramerters[key]}")
                else:
                    print(key)
    else:
        print(f"Failed with error code {response.status_code}")


def platform_profile_metadata(plid):
    response = requests.get(
        f"https://argovis.colorado.edu/catalog/profiles/{plid}/map", headers=headers
    )
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed with error code {response.status_code}")


def argoexp(lat, lng, radius, start, end, geometry, fpath, plid):
    if geometry is not None:
        with open(geometry) as f:
            gj = geojson.load(f)
        shp = gj["features"][0]["geometry"]["coordinates"]
        ar = round(getarea(shp), 2)
        ar = "{:,}".format(ar)
        print(f"Processing {os.path.basename(geometry)} with area {ar} square km")
    elif plid is not None:
        print(f"Processing for Platform Profile ID {plid}" + "\n")
        profiler(plid, fpath)
        """Check to see if profile is BGC and get BGC keys"""
        platform_url = (
            f"https://argovis.colorado.edu/catalog/platforms/{plid.split('_')[0]}"
        )
        resp = requests.get(platform_url)
        if resp.status_code == 200 and resp.json()[0].get("containsBGC") == True:
            print(
                "BGC profile found for argofloats creating BGC platform profile export"
            )
            profiler_bgc(plid, fpath)
    elif lat is not None and lng is not None:
        if radius is None:
            radius = 1000000
        elif radius is not None:
            radius = float(radius) * 1000
        shp = generate_buffer_meter(float(lat), float(lng), float(radius))
        print(f"Processing for {float(radius)/1000} km around {lat},{lng}")
    else:
        sys.exit("Please provie lat long pair or full path to geometry.geojson file")
    if start is not None and end is not None:
        dates = date_range(start, end)
        dates = list(dates)
        for x in range(len(dates) - 1):
            st = dates[x]
            ed = dates[x + 1]
            params = {
                "startDate": st,
                "endDate": ed,
                "shape": f"{shp}",
                "presRange": "[0,2000]",
            }
            profile_id(params)
        if profile_list:
            for plid in profile_list:
                try:
                    profiler(plid, fpath)
                except tenacity.RetryError as e:
                    print(f"Retry failed for Core Platform Profile: with ID {plid}")

                """Check to see if profile is BGC and get BGC keys"""
                platform_url = f"https://argovis.colorado.edu/catalog/platforms/{plid.split('_')[0]}"
                resp = requests.get(platform_url)
                if (
                    resp.status_code == 200
                    and resp.json()[0].get("containsBGC") == True
                ):
                    print(
                        "BGC profile found for argofloats creating BGC platform profile export"
                    )
                    try:
                        profiler_bgc(plid, fpath)
                    except tenacity.RetryError as e:
                        print(f"Retry failed for BGC Platform Profile: with ID {plid}")
        else:
            print("\n" + "No matching profiles found for query")
    if plid is None and start is None and end is None:
        print("Provide start and end dates for Geometry or point searches")
