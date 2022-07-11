import requests 
import json 
import datetime 
import random
import argparse
import time

from makedata import make_header, make_data_files

# TODO: 
# - make fits files match range of normal data (ie [0,2^64] instead of [-0.5, 0.5])
# - large fits should be different size than small fits
# - generate thumbnails

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

def increment_filenumber():
    number = 0
    with open("filenumber.txt", "r") as f:
        number = int(f.read())
    with open("filenumber.txt", "w") as f:
        f.write(str(number + 1))

def get_list_of_filenames(site, data_type, utc_time, files):

    # simple hardcode instrument name for now
    instrument = 'inst'
    datestring = utc_time.strftime('%Y%m%d')

    # Read the filenumber to use
    filenumber = 0
    with open("./filenumber.txt",'r') as f:
        filenumber = int(f.read())
    zero_padding = "0" * (8 - len(str(filenumber)))
    filenumber = f"{zero_padding}{filenumber}"

    file_header = (f"{site}-{instrument}-{datestring}-{filenumber}-{data_type}00.txt", TEXT_HEADER_PATH)
    file_jpg = (f"{site}-{instrument}-{datestring}-{filenumber}-{data_type}10.jpg", JPG_10_PATH)
    file_jpg_small = (f"{site}-{instrument}-{datestring}-{filenumber}-{data_type}11.jpg", JPG_11_PATH)
    file_sfits = (f"{site}-{instrument}-{datestring}-{filenumber}-{data_type}10.fits.bz2", FITS_10_PATH)
    file_fits = (f"{site}-{instrument}-{datestring}-{filenumber}-{data_type}00.fits.bz2", FITS_00_PATH)

    file_list = []
    if 'h' in files: file_list.append(file_header)
    if 'j' in files: file_list.append(file_jpg)
    if 't' in files: file_list.append(file_jpg_small)
    if 'f' in files: file_list.append(file_sfits)
    if 'F' in files: file_list.append(file_fits)
    return file_list


def upload_files(filename_list, s3dir, info_channel):
    for f in filename_list:
        upload_url = get_upload_url(f[0], s3dir, info_channel)
        with open(f[1], 'rb') as base_file:
            data = {'file': (f[0], base_file)}
            upload_response = requests.post(upload_url["url"], upload_url["fields"], files=data)
            print(f'uploading {upload_url["fields"]["key"]}')
            print(upload_response)
    increment_filenumber()


def upload_test_files(site, data_type, files, s3dir, info_channel):

    # generate fits header
    time_now = datetime.datetime.utcnow()
    header = make_header()
    make_data_files(header)

    # get list of files to upload
    files_to_upload = get_list_of_filenames(site, data_type, time_now, files)

    upload_files(files_to_upload, s3dir, info_channel)

        
    
if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--site', default='tst', help="set the name of the site (ie. tst)")
    parser.add_argument('-dt', '--data_type', default='e', help="set the data type (eg. e or EP)")
    parser.add_argument('-f', '--files', default='hjtfF', help="files to include (h=header, j=jpg, f=fits10, F=fits01, t=thumbnail)")
    parser.add_argument('-r', '--repeat', default=1, type=int, help="upload this number of data sets")
    parser.add_argument('-s3', '--s3dir', default='data', type=str, help="choose from {'data', 'info-images', 'allsky'}")
    parser.add_argument('-c', '--channel', default=1, type=int, help="for info images: which channel to use (1,2, or 3)")

    args = parser.parse_args()

    site = args.site
    data_type = args.data_type.upper()
    files = args.files
    repeat = args.repeat
    s3dir = args.s3dir
    info_channel = args.channel

    for i in range(repeat):
      print(f"uploading with site {site}, data_type {data_type}, files {files}, s3dir {s3dir} -- {i}")
      upload_test_files(site, data_type, files, s3dir, info_channel)
