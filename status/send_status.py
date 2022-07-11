import time
import random
import json
import requests
import sys
import argparse

def r(smallest, largest, decimals=3):
    r_range = largest - smallest
    return round((random.random() * r_range) + smallest, decimals)

def random_by_minute(options):
    length = len(options)

def observing_conditions_status_factory():
    weather_status = {
        "meas_sky_mpsas": 23.6,
        "open_ok": "no",
        "dewpoint_C": 11,
        "wind_m/s": r(0,5,0),
        "temperature_C": r(0, 20, 2),
        "cloud_cover_%": "0.0",
        "humidity_%": r(10,90,0),
        "rain_rate": 0,
        "calc_HSI_lux": 0.004,
        "calc_sky_mpsas": 1.37,
        "last_sky_update_s": 19,
        "pressure_mbar": 978,
        "sky_temp_C": -2.9,
        "wx_ok": "Yes",

        "wx_hold": False,
        "hold_duration": 0,
    }
    random_keys_to_remove = []
    for key in weather_status:
        if random.random() < 0.5:
            random_keys_to_remove.append(key)
    for key in random_keys_to_remove:
        del weather_status[key]
    return weather_status

def enclosure_status_factory():
    enclosure = {
        "enclosure_mode": random.choice(["sentient", "lifelike", "hibernation", "friendly", "simple"]),
        "dome_azimuth": r(0,180,0),
        "dome_slewing": False,
        "shutter_status": random.choice(["laughing", "sleeping", "breathing", "eating lunch", "dancing"]),
        "enclosure_message": "Enclosure message: the enclosure says hello",
        "enclosure_synchronized": True
    }
    return enclosure


def mount_status_factory():
    mount_status = {
        "altitude": "-0.002",
        "right_ascension": 'mount_ra',
        "sidereal_time": "4.29609",
        "azimuth": "180.001",
        "message": "-",
        "pointing_instrument": "tel1",
        "zenith_distance": "90.0",
        "declination": 'mount_dec',
        "coordinate_system": "J.now",
        "tracking_declination_rate": "0.0",
        "tracking_right_ascension_rate": "0.0",
        "airmass": " >> 5 ",
        "equinox": "J2020.68",
        "timestamp": time.time()
    }
    return mount_status


def telescope_status_factory():
    telescope_status = {
        "right_ascension": round(random.random() * 24, 3),
        "declination": round(random.random() * 180 - 90, 3),
        "altitude": "-0.002",
        "sidereal_time": "4.29609",
        "azimuth": "180.001",
        "message": "-",
        "pointing_instrument": "tel1",
        "zenith_distance": "90.0",
        "coordinate_system": "J.now",
        "tracking_declination_rate": "0.0",
        "tracking_right_ascension_rate": "0.0",
        "airmass": " >> 5 ",
        "equinox": "J2020.68",
        "timestamp": time.time()
    }
    return telescope_status


def make_status():
    status = {
        "statusType": "deviceStatus",
        "status": {
            "screen": {
                "screen1": {
                    "bright_setting": "0",
                    "dark_setting": "screen is off"
                }
            },
            "focuser": {
                "focuser1": {
                    "focus_temperature": "7.0",
                    "focus_moving": "false",
                    "focus_position": "9415.3"
                }
            },
            "camera": {
                "camera1": {
                    "busy_lock": "false",
                    "status": "not implemented yet",
                    "NEWKEY": "NEWVAL",
                }
            },
            "telescope": {
                "telescope1": telescope_status_factory(),
                "telescope2": telescope_status_factory(),
            },
            "mount": {
                "mount1": mount_status_factory(),
                "mount2": mount_status_factory(),
            },
            "rotator": {
                "rotator1": {
                    "rotator_moving": "false",
                    "position_angle": "190.001"
                }
            },
            "send_heartbeat": "false",
            "filter_wheel": {
                "filter_wheel1": {
                    "filter_number": "0",
                    "filter_name": "none",
                    "filter_offset": "0.0",
                    "wheel_is_moving": "false"
                }
            },
            "selector": {
                "selector1": {
                    "camera": "camera_1_1",
                    "guider": None,
                    "instrument": "Main_camera",
                    "port": 1
                }
            },
            "sequencer": {
                "sequencer1": {
                    "active_script": "none",
                    "sequencer_busy": "false"
                }
            },
            "timestamp": time.time(),
        }
    }
    return status

def make_wxEncStatus():
    status = {
        "statusType": "wxEncStatus",
        "status": {
            "observing_conditions": {
                "observing_conditions1": observing_conditions_status_factory()
            },
            "enclosure": {
                "enclosure1": enclosure_status_factory()
            },
        }
    }
    return status

def make_weather_status():
    status = {
        "statusType": "weather",
        "status": {
            "observing_conditions": {
                "observing_conditions1": observing_conditions_status_factory()
            },
        }
    }
    return status

def make_enclosure_status():
    status = {
        "statusType": "enclosure",
        "status": {
            "enclosure": {
                "enclosure1":enclosure_status_factory()
            },
        }
    }
    return status

def make_device_status():
    status = {
        "statusType": "device",
        "status": {
            "screen": {
                "screen1": {
                    "bright_setting": "0",
                    "dark_setting": "screen is off"
                }
            },
            "focuser": {
                "focuser1": {
                    "focus_temperature": "7.0",
                    "focus_moving": "false",
                    "focus_position": "9415.3"
                }
            },
            "camera": {
                "camera1": {
                    "busy_lock": "false",
                    "status": "not implemented yet",
                    "NEWKEY": "NEWVAL",
                }
            },
            "telescope": {
                "telescope1": telescope_status_factory(),
                "telescope2": telescope_status_factory(),
            },
            "mount": {
                "mount1": mount_status_factory(),
                "mount2": mount_status_factory(),
            },
            "rotator": {
                "rotator1": {
                    "rotator_moving": "false",
                    "position_angle": "190.001"
                }
            },
            "send_heartbeat": "false",
            "filter_wheel": {
                "filter_wheel1": {
                    "filter_number": "0",
                    "filter_name": "none",
                    "filter_offset": "0.0",
                    "wheel_is_moving": "false"
                }
            },
            "selector": {
                "selector1": {
                    "camera": "camera_1_1",
                    "guider": None,
                    "instrument": "Main_camera",
                    "port": 1
                }
            },
            "sequencer": {
                "sequencer1": {
                    "active_script": "none",
                    "sequencer_busy": "false"
                }
            },
            "timestamp": time.time(),
        }
    }
    return status

# For testing sites like FAT where all status is sent as a single package.
# Want to make sure timestamps are handled correctly.
def make_combined_status(status_types: str = 'dew') -> dict:
    #status = {} 
    #if 'd' in status_types: 
        #status.update(make_status())
    #if 'e' in status_types: 
        #status.update()
    return {
        **make_wxEncStatus(),
        **make_status() 
    }


def send_device_status_old(url):
    status_payload = json.dumps(make_status())
    response = requests.post(url, status_payload)
    sys.stdout.write('d')
    sys.stdout.flush()

def send_wx_status_old(url):
    status_payload = json.dumps(make_wxEncStatus())
    response = requests.post(url, status_payload)
    sys.stdout.write('w')
    sys.stdout.flush()

    # ====================

def send_weather_status(url):
    status_payload = json.dumps(make_weather_status())
    requests.post(url, status_payload)
    sys.stdout.write('w')
    sys.stdout.flush()

def send_enclosure_status(url):
    status_payload = json.dumps(make_enclosure_status())
    requests.post(url, status_payload)
    sys.stdout.write('e')
    sys.stdout.flush()

def send_device_status(url):
    status_payload = json.dumps(make_device_status())
    requests.post(url, status_payload)
    sys.stdout.write('d')
    sys.stdout.flush()

def send_batch_status(url, status_types):
    if 'd' in status_types: send_device_status(url)
    if 'w' in status_types: send_weather_status(url)
    if 'e' in status_types: send_enclosure_status(url)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--site', default='tst', help="set the name of the site (ie. tst)")
    parser.add_argument('-t', '--type', default="wed", help="w for weather, e for enclosure, d for devices")
    parser.add_argument('-st', '--stage', default="prod", help="Set endpoint stage: prod, dev, or test")
    parser.add_argument('-r', '--repeat', action=argparse.BooleanOptionalAction)
    parser.add_argument('-i', '--interval', default=5, type=int, help="Number of seconds between each status update")

    args = parser.parse_args()

    # Use to translate stage (prod, dev, test) into the url name
    stage_parser = {
        "prod": "status",
        "dev": "dev",
        "test": "test"
    }

    # set sending parameters
    site = args.site
    stage = stage_parser.get(args.stage, "prod") # Note: 'dev' stage doesn't exist (7/11/22), use prod or test.
    url = f"https://status.photonranch.org/{stage}/{site}/status"

    status_type = args.type
    repeat = args.repeat
    interval = args.interval

    print('sending status')
    send_batch_status(url, status_type)
    while repeat:
        for i in range(12):
            send_batch_status(url, status_type)
            time.sleep(interval)
        print()  # newline after 12 updates (1 minute)

    
