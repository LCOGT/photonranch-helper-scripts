import requests
import json
import datetime
import random
import argparse
import time
import os

from makedata import make_header, make_data_files
from tqdm import tqdm

# TODO:
# - make fits files match range of normal data (ie [0,2^64] instead of [-0.5, 0.5])
# - large fits should be different size than small fits

TEXT_HEADER_PATH = "./generated_files/generated.txt"
FITS_00_PATH = "./generated_files/generated.fits.bz2"
FITS_10_PATH = "./generated_files/generated.fits.bz2"
JPG_10_PATH = "./generated_files/generated.jpg"
JPG_11_PATH = "./generated_files/generated.jpg"

PHOTONRANCH_API = "https://api.photonranch.org/test"


def get_upload_url(filename, s3_directory, info_channel=None):
    request_body = {"object_name": filename, "s3_directory": s3_directory}
    if info_channel is not None:
        request_body["info_channel"] = info_channel
    url = PHOTONRANCH_API + "/upload"
    response = requests.post(url, json.dumps(request_body))
    return response.json()

# Gets the latest image at the site, and adds 1 to the file number at the end.
def get_next_filenumber(site):
    url = f"http://api.photonranch.org/api/{site}/latest_images/1"
    response = requests.get(url).json()
    base_filename = response[0]['base_filename']
    filenumber = int(base_filename.split('-')[-1])
    return filenumber + 1


def get_list_of_filenames(site, data_type, utc_time, files, filenumber):

    # simple hardcode instrument name for now
    instrument = 'inst'
    datestring = utc_time.strftime('%Y%m%d')


    file_header = (
        f"{site}-{instrument}-{datestring}-{filenumber}-{data_type}00.txt", TEXT_HEADER_PATH)
    file_jpg = (
        f"{site}-{instrument}-{datestring}-{filenumber}-{data_type}10.jpg", JPG_10_PATH)
    file_jpg_small = (
        f"{site}-{instrument}-{datestring}-{filenumber}-{data_type}11.jpg", JPG_11_PATH)
    file_sfits = (
        f"{site}-{instrument}-{datestring}-{filenumber}-{data_type}10.fits.bz2", FITS_10_PATH)
    file_fits = (
        f"{site}-{instrument}-{datestring}-{filenumber}-{data_type}00.fits.bz2", FITS_00_PATH)

    file_list = []
    if 'h' in files:
        file_list.append(file_header)
    if 'j' in files:
        file_list.append(file_jpg)
    if 't' in files:
        file_list.append(file_jpg_small)
    if 'f' in files:
        file_list.append(file_sfits)
    if 'F' in files:
        file_list.append(file_fits)
    return file_list


def upload_files(filename_list, s3dir, info_channel, site):
    for f in filename_list:
        upload_url = get_upload_url(f[0], s3dir, info_channel)
        with open(f[1], 'rb') as base_file:
            data = {'file': (f[0], base_file)}
            upload_response = requests.post(
                upload_url["url"], upload_url["fields"], files=data)

            if upload_response.status_code == 204:
                print(f'uploading {upload_url["fields"]["key"]}... \t\tsuccess')
            else:
                print(f'uploading {upload_url["fields"]["key"]}... \t\tfailed')

def upload_test_files(site, data_type, files, s3dir, info_channel, extra_headers={}):

    # generate fits header
    time_now = datetime.datetime.utcnow()
    header = make_header(extra_headers)
    make_data_files(header)

    # Read the filenumber to use
    filenumber = get_next_filenumber(site)
    zero_padding = "0" * (8 - len(str(filenumber)))
    filenumber = f"{zero_padding}{filenumber}"

    # get list of files to upload
    files_to_upload = get_list_of_filenames(site, data_type, time_now, files, filenumber)

    upload_files(files_to_upload, s3dir, info_channel, site)


def upload_smartstack_files(site, data_type, files, s3dir, info_channel, smartstack_len):

    # Make one id used for all files in the same stack
    smartstack_id = f"ssk_id_{int(time.time())}"
    exposure_time = round(random.randint(1,20), 3)
    ra = random.random()*24,
    dec = (random.random() * 180) - 90,

    # Get the next filenumber based on the latest site image
    starting_filenumber = get_next_filenumber(site)

    # generate fits header
    time_now = datetime.datetime.utcnow()

    # iterate through each smartstack frame
    for i in range(smartstack_len):
        smartstack_headers = {
            "SSTKNUM": i,
            "SSTKLEN": smartstack_len,
            "SMARTSTK": smartstack_id,
            "EXPTIME": exposure_time,
            "CRVAL1": ra,
            "CRVAL2": dec,
        }
        header = make_header(smartstack_headers)
        make_data_files(header)

        # Create the filenumber for each subsequent smartstack frame
        filenumber = starting_filenumber + i
        zero_padding = "0" * (8 - len(str(filenumber)))
        filenumber = f"{zero_padding}{filenumber}"

        # get list of files to upload
        files_to_upload = get_list_of_filenames(site, data_type, time_now, files, filenumber)

        upload_files(files_to_upload, s3dir, info_channel, site)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--site', default='tst',
                        help="set the name of the site (ie. tst)")
    parser.add_argument('-dt', '--data_type', default='e',
                        help="set the data type (eg. e or EP)")
    parser.add_argument('-f', '--files', default='hjtf',
                        help="files to include (h=header, j=jpg, f=fits10, F=fits01, t=thumbnail)")
    parser.add_argument('-r', '--repeat', default=1, type=int,
                        help="upload this number of data sets")
    parser.add_argument('-s3', '--s3dir', default='data', type=str,
                        help="choose from {'data', 'info-images', 'allsky'}")
    parser.add_argument('-c', '--channel', default=1, type=int,
                        help="for info images: which channel to use (1,2, or 3)")
    parser.add_argument('-ss', '--smartstack', default=1, type=int,
                        help="number of smartstack frames; 1 means no smartstack (default==1)")

    args = parser.parse_args()

    site = args.site
    data_type = args.data_type.upper()
    files = args.files
    repeat = args.repeat
    s3dir = args.s3dir
    info_channel = args.channel
    smartstack_len = args.smartstack

    for i in range(repeat):

        if smartstack_len > 1:
            print(
                f"uploading {smartstack_len} smartstack frames with site {site}, data_type {data_type}, files {files}, s3dir {s3dir} -- {i}")
            upload_smartstack_files(
                site, data_type, files, s3dir, info_channel, smartstack_len)
        else:
            print(
                f"uploading with site {site}, data_type {data_type}, files {files}, s3dir {s3dir} -- {i}")
            upload_test_files(site, data_type, files, s3dir, info_channel)
