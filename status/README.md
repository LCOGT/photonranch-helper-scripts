
# Send Site Status

This is a script that simulates an observatory sending device, weather, and enclosure status payloads. It is useful for 
verifying the behavior of photonranch-status and ptr_ui. 

## Usage

To set up the environment, create and activate a virtual environment with python3.9.
Install the dependencies in requirements.txt.

Run the script in its default state with `$ python send_status.py`.

There are a number of optional arguments you can add to adjust the settings of the script:

| name | long form | short form | default | description |
| ---- | --------- | ---------- | ------- | ----------- |
| site | --site    | -s         | tst     | set the name of the site |
| status type | --type | -t | wed       | Status that will be included: w for weather, e for enclosure, d for devices |
| stage | --stage | -st | prod    | Select the status environment stage to use. This should match the one used in the frontend for results to be visible. |
| repeat | --repeat | -r         |  | Include this flag to continually send status every 5 seconds |
| interval | --interval | -i | 5    | Number of seconds between each status update |

Here is an example command you can run with some non-default parameters:

``` bash
python send_status.py -s tst -r -i 2 -t we
```

This will send weather and enclosure status to the tst site repeatedly every 2 seconds. 

For each status sent, the terminal will print the letter corresponding to the status type. So the above will have an output that looks like
``` bash 
wewewewewewe...
```
which will continue until the process is stopped (ctrl-c).

If you go to www.photonranch.org/site/tst/observe, you should be able to see the status updating in the bottom status panel.
