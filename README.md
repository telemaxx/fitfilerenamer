# fitfilerenamer

### LEZYNE GPS Devices
creating fit files with unfriendly names like:
```
bcfe453.fit
```
This tool automaticily rename such files in:
```
YYYY-MM-DD_hh-mm-ss_device_altitudegain_count.fit
2017-12-10_15-30-36_lezyne_576hm_4.fit
```
HOWTO INSTALL
-----------------------------------

  * 1st install python 2.7 or python 3 or pypy

  * Install fitparse modul
    [Available here](http://dtcooper.github.com/python-fitparse/)
description somewhere below
  * download fitfilerenamer.py and save it some where
  * create a shortcut on the Desktop. Target:
  ```
  C:\yourepythonprogrammfolder\python.exe C:\thefolderwhereyousavethefile\fitfilerenamer.py
```
## HOWTO USE
* doubleclick the shortcut, the script looking for fit files in the defaultdirectory, defined in the python file
* drag and drop fit files to the shortcut. this files are renamed
* drag and drop ONE folder to the shortcut. all fitfiles in the first level of that folder are renamed

## HOWTO install fitparse
the description on the project webpage did not worked for me so i do it this way:
* go to the [project github page](https://github.com/dtcooper/python-fitparse)
* click on "clone or download" and select "download zip"
* unzip this file into a new folder
* open a command prompt and change in that folder:
```sh
$ cd youredownloadfolder\python-fitparse
$ C:\yourepythonprogrammfolder\python.exe setup.py install
```

