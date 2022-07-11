
# Send Test Images

This directory contains code that will upload images to a Photon Ranch site.
The main script is up.py, which generates fake data and sends them to s3 with the same routine that observatory sites use.

## Usage

To set up the environment, create and activate a virtual environment with python3.9.
Install the dependencies in requirements.txt.

Run the script in its default state with `$ python up.py`.

There are a number of optional arguments you can add to adjust the settings of the script:

usage: up.py [-h] [-s SITE] [-dt DATA_TYPE] [-f FILES] [-r REPEAT] [-s3 S3DIR] [-c CHANNEL]

| name | long form | short form | default | description |
| ---- | --------- | ---------- | ------- | ----------- |
| site | --site    | -s         | tst     | set the name of the site |
| data type | --data_type | -dt | e       | set the data type (eg. e, EX, EP, ...) |
| files | --files | -f         | hjtfF | files to include (h=header, j=jpg, f=fits10, F=fits01, t=thumbnail) |
| repeat | --repeat | -r         | 1 | upload this number of data sets |
| s3 directory | --s3dir | -s3         | data | choose from {'data', 'info-images'}, {'allsky'} |
| channel | --channel | -c         | 1 | for info images: which channel to use (1, 2, or 3) |

Here is an example command you can run with some non-default parameters:

``` bash
$ python up.py -s tst -f fFh -r 3 
```

This command will upload data to the tst site. Each exposure includes the small fits, large fits, and header txt file. It will send data for three separate exposures. 

Each file uploaded successfully to s3 will print a <Response [204]> in the console. 

If you go to www.photonranch.org/site/tst/observe, you should be able to see the images you just uploaded. 

## Developer Notes

The filenumbers for each image are supposed to increment sequentially. 
The numbering is tracked in a simple text file `filenumber.txt` that is updated after each exposure set is created and sent. 
This means if two developers are using this script at the same time from different machines, these is a possibility for 
identically named files to both be sent, resulting in unexpected behavior. So it's best to check that no one else is 
using this script at the same time, if possible, and manually update the filenumber.txt number to match the latest test
image for the site that day (this ensures a unique filename). 

The images that are created are generated randomly and will look like smooth monochrome blobs. The data is generated using
a simple perlin noise algorithm. 



