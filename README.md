# fitfilerenamer.py

### LEZYNE GPS Devices...
...creating fit files with unfriendly names like:
`bcfe453.fit`   
This tool looks into the fit file and automatically rename such files in:   
`2017-12-10_15-30-36_lezyne_576hm_4.fit`   
this syntax:   
`YYYY-MM-DD_hh-mm-ss_device_altitudegain_count.fit`

### HOWTO INSTALL
  * 1st install python 2.7 or python 3 or pypy
  * Install fitparse modul
    [Available here](http://dtcooper.github.com/python-fitparse/)
description some where below
  * download fitfilerenamer.py and save it some where
  * create a shortcut on the Desktop. Target:
  `C:\yourepythonprogrammfolder\python.exe C:\thefolderwhereyousavethefile\fitfilerenamer.py`
## HOWTO USE
##### There are three different ways to use this tool:
1. doubleclick the shortcut, the script looking for fit files in the defaultdirectory, defined inside the python file
```python
# Directory where the FIT Files are located
# HOME stands for youre homedirectory e.g /home/pi 
HOME = os.path.expanduser('~')
FIT_DEFAULT_PATH = os.path.join(HOME,'BTSync','SA5','Documents','LezyneGpsAlly','6745th')
```

2. drag and drop one or more fit files to the shortcut. this files are renamed
3. drag and drop ONE folder to the shortcut. all fitfiles in the first level of that folder are renamed
Note: This tool using the fitparse modul, powerfull but slow. So please be patient.
##### The options:
* getting help: `C:\thefolderwhereyousavethefile\fitfilerenamer.py -h`
* getting version `C:\thefolderwhereyousavethefile\fitfilerenamer.py --version`

## HOWTO install fitparse
the description on the project webpage did not worked for me so i do it this way:
* go to the [project github page](https://github.com/dtcooper/python-fitparse)
* click on "clone or download" and select "download zip"
* unzip this file into a new folder
* open a command prompt and change in that folder and execude the `setup.py`:
```sh
$ cd youredownloadfolder\python-fitparse
$ C:\yourepythonprogrammfolder\python.exe setup.py install
```
for pypy:
```sh
$ cd youredownloadfolder\python-fitparse
$ C:\yourepypyprogrammfolder\pypy.exe setup.py install
```
The \"normal\" easyier way would be:
```sh
$ C:\yourepythonprogrammfolder\pip install python-fitparse
```
you should try that first
## TIP
instead of using the standard python, use [pypy](https://pypy.org)   
With pypy the script runs about 5 times faster.   
On Windows, there is only the python2 compliant 32bit version. but that version is ok. 

