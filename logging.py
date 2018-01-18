#qpy:console
#qpy:2

""" fitfileRenamer.py
With this Script you can rename fit Files created with Lezyne e.g:
a876cde4.fit becomes 2017-12-31_15-59-59.fit
return codes:
0 = ok
1 = argument given, but nothing found
2 = No Argument given and Defaultlocation does not exist
6 = Arguments given but not a fitfiles found

release infos:
0.2: error handling to parse all demo fitfles
0.3: argument parser
0.4: searching 'time_created' instead of 'timstamp'
0.5: enhanced altidude is now correctly searched
0.6: working with absolut filenames in the list. to allow Drag n Drop multiple files
0.61: if parsing defective file and Verbosity is 2 some info is shown.
0.62: using totalascent instead of enhanced altitude to get correct altitude gain
0.63: mods to make the code comptible to python 2.7 AND 3
0.64: removing hard coded windows default path and using hopefully os independent path
0.70: switching from optparse to argparse. adding some options: -s (simulationmode -i (ignore wrong crc) -v (verbosity 0-2)
0.71: better Android Qpython detection
0.72: more detailed summary
"""

__version__ = '0.72'
__author__ = 'telemaxx'

import os
import sys
import argparse
import datetime
import time
import glob
import logging
from fitparse import FitFile, FitParseError

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.info('Information')
logging.warning('Warnung')
logging.debug('debug')
logging.error('error message')
logging.critical('critical message')

#try to detect QPython on android
ROA = True
try: #check if android and import gui tools
	import androidhelper.sl4a as sl4a # try new locaation
except: #otherwise its not android or old location
	#print('not qpython 3.6 or QPython 2')
	ROA = None
if not ROA:
	ROA = True
	try:
		import sl4a # try old location
	except:
		#print('not qpython 3.2')
		ROA = None

DEFAULT_MANUFACTURER = 'Samsung-A5-2017' # used, when no manufacturer given or manufacturer is set garmin by oruxmaps
DEFAULT_EVENT_TYPE = 'Cycling'
WAIT_AFTER_JOB_DONE = 10

# Directory where the FIT Files are located
if ROA: # android
    FIT_DEFAULT_PATH = os.path.abspath(os.path.join(os.sep,'sdcard','Documents','LezyneGpsAlly','6745th'))
else:
    # HOME stands for youre homedirectory e.g /home/pi 
    HOME = os.path.expanduser('~')
    FIT_DEFAULT_PATH = os.path.join(HOME,'BTSync','SA5','Documents','LezyneGpsAlly','6745th')

    

def main():
    global verbosity, simulation
    starttime = time.time()
#nargs="*",'--fit_files_or_folder','-f','--fit_files_or_folder', dest = 'fit_files_or_folder'
    parser = argparse.ArgumentParser(description='The fitfilerenamer tool',epilog = '%(prog)s {version}'.format(version=__version__))
    parser.add_argument('-v', '--verbosity', type = int, choices = range(0,2), default=1, help='0= silent, 1= a bit output, 2= many output')
    parser.add_argument('fit_files_or_folder',nargs="*",  help='w/o default Dir is used')
    parser.add_argument('-s', '--simulation', action = 'store_true', help='simulation without renaming any file')
    parser.add_argument('-i', '--ignorecrc', action = 'store_false', help='no crc check')
    arguments = vars(parser.parse_args())
    args = arguments['fit_files_or_folder']
    verbosity = arguments['verbosity']
    ignorecrc = arguments['ignorecrc']
    simulation = arguments['simulation']
    #    (optionen, args) = parser.parse_args()
    #Iprint('Argumentlength %s' % (len(args)))
    if ROA:
        Dprint('Android (qpython) detectet')
        droid = sl4a.Android()
    else:
        Dprint('Android not detectet')

    if len(args) == 1:
        Dprint("Looking for File or Directory: %s" % args[0])
        if args[0][-4:].lower()=='.fit' and os.path.isfile(args[0]): # if the one argument is a file, create a list with one entry
            filelist = [args[0]]
        elif os.path.isdir(args[0]): #if the one argument is a dir, create a list with the fit files
            Dprint("argument given, it is a directory: %s" % (args[0]))
            filelist = create_filelist(args[0])
        else:
            Iprint('argument given, but nothing found')
            final_message('wait %d sec or press strg c' % (WAIT_AFTER_JOB_DONE))
            sys.exit(1)

    elif  len(args) == 0: # no argument given
        Dprint('No argument, looking at default Path: %s' % (FIT_DEFAULT_PATH))
        if os.path.isdir(FIT_DEFAULT_PATH):
            Dprint('No argument, but default path exist: %s' % (FIT_DEFAULT_PATH))
            filelist = create_filelist(FIT_DEFAULT_PATH)
        else: # no argument and no defaultlocation found
            Iprint("No Argument given and Defaultlocation does not exist: %s" % (FIT_DEFAULT_PATH))
            final_message('wait %d sec or press strg c' % (WAIT_AFTER_JOB_DONE))
            sys.exit(2)
    else: # more than 1 arguments, todo: filtering *.fit
        Dprint('much arguments.  %d' % (len(args)))
        filelist = []
        for next_file in args:
            if next_file[-4:].lower()=='.fit' and os.path.isfile(next_file):
                Dprint('file %s' % (next_file))
                filelist.append(next_file)
        if len(filelist) == 0:
            Iprint('Arguments given but not a fitfiles found')
            final_message('wait %d sec or press strg c' % (WAIT_AFTER_JOB_DONE))
            sys.exit(6)
    Dprint('fitfiles: %s' % (filelist))

    n = len(filelist)
    if ROA:
        # create progressbar for download
        droid.dialogCreateHorizontalProgress(
        'Analyzing and Renaming',
        'please be patient',
        n)
        droid.dialogShow()
        Dprint('creating progressbar')

    Iprint('please be patient, i am parsing. This can take a minute')
    file_count = skipped_count = renamed_count = simulated_count = skipped_defective_count = 0
    for file in filelist:
        Dprint('processing %s' % (file))
        Dprint('start datafitprocessor')
        if not os.path.isfile(file):
            Iprint('skipping folder: %s' % (file))
            continue
        try:
            fitfile = FitFile(file, check_crc = ignorecrc)
            Dprint('parsing start')
            fitfile.parse()
            Dprint('parsing done')
        except FitParseError as e:
            Iprint('skipping defective fitfile %s' % (file))
            skipped_defective_count +=1
            for m in e.args:
                Dprint('Exception: %s' % (m))
            continue
        #Dprint('rename arguments: %s , %s , %d' % (fitfile, file, file_count))
        renamestatus = rename_fitfile(fitfile, file, file_count)
        if   renamestatus == 'renamed':
            renamed_count += 1
        elif renamestatus == 'simulated_renaming':
            simulated_count +=1
        elif renamestatus == 'skipped':
            skipped_count +=1
        if ROA:
            droid.dialogSetCurrentProgress(file_count + 1)
        file_count += 1
    difftime = time.time() - starttime
    Iprint('finished processing %d file(s) in %d seconds' % (file_count, difftime))
    summary = 'renamed: %d, simulated: %d, skipped existing: %d, skipped defective: %d' % (renamed_count, simulated_count, skipped_count, skipped_defective_count)
    Iprint(summary)
    if ROA:
        droid.dialogDismiss()
        title='I have processed %d File(s) in %d seconds' % (file_count, difftime)
        #droid.makeToast(title)
        #droid.ttsSpeak(title)
        #summary = 'renamed: %d, simulated: %d, skipped existing: %d, skipped defective: %d' % (renamed_count, simulated_count, skipped_count, skipped_defective_count)
        droid.dialogCreateAlert(title, summary)
        droid.dialogSetPositiveButtonText('OK')
        droid.dialogShow()
        dummy = droid.dialogGetResponse().result
    else:
        final_message('wait %d sec or press strg c' % (WAIT_AFTER_JOB_DONE))

def Dprint(text2print):
    if verbosity == 2:
        print(text2print)

def Iprint(text2print):
    if verbosity != 0:
        print(text2print)

def get_timestamp(messages):
    for m in messages:
        #Dprint('messages %s' % (m))
        fields = m.fields
        for f in fields:
            #Dprint('field %s' % (f))
            #if f.name == 'timestamp':
            if f.name == 'time_created':
                if isinstance(f.value,int):
                    Dprint('timestamp is integer: %d' % (f.value))
                    return None
                else:
                    return f.value
    return None

def get_event_type(messages):
    for m in messages:
        fields = m.fields
        for f in fields:
            if f.name == 'sport':
                return f.value
    return DEFAULT_EVENT_TYPE

def get_manufacturer(messages):
    for m in messages:
        fields = m.fields
        for f in fields:
            if f.name == 'manufacturer':
                if f.value == 'garmin':# orux set falseflag garmin
                    Dprint ('manufacturer was garmin, using \"%s\"' % DEFAULT_MANUFACTURER)
                    return DEFAULT_MANUFACTURER
                Dprint('manufacturer %s' % (f.value))
                return f.value
    return DEFAULT_MANUFACTURER

def get_enhanced_altitude(messages):
    enh_alt_max=0.0
    for m in messages:
        fields = m.fields
        for f in fields:
            if f.name == 'total_ascent' and f.value != None:
                if f.value > enh_alt_max:
                    enh_alt_max = f.value
                #print('alt: ',str(int(float(enh_alt_max))))
    return str(int(float(enh_alt_max)))


def create_filelist(dir):
    fit_files = glob.glob(os.path.join(dir,'*.[fF][iI][tT]'))
    return(fit_files)

def final_message(msg):
    Iprint(msg)
    if verbosity > 0:
        try:
            time.sleep(WAIT_AFTER_JOB_DONE)
        except KeyboardInterrupt:
            pass

#(fitfile, file, file_count)
def rename_fitfile(fitfile, original_filename=None, counter=0):
    global simulation
    Dprint('fitfile.messages')
    messages = fitfile.messages
    Dprint('search timestamp')
    timestamp = get_timestamp(messages)
    #Dprint('timestamp %s' % (timestamp))
    Dprint('search eventtime')
    event_type = get_event_type(messages)
    Dprint('search manufateur')
    manufacturer = get_manufacturer(messages)
    Dprint('search enhanced altitude')
    climb = get_enhanced_altitude(messages)
    Dprint('enhanced_altitude %s' % (climb))
    Dprint('analyzing done')
    if timestamp is not None:
        output_file = timestamp.strftime('%Y-%m-%d_%H-%M-%S') + '_' + manufacturer + '_' + climb + 'hm_' + str(counter) + '.fit'        
    else:
        modified_time = os.stat(original_filename).st_mtime
        date_string=time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(modified_time))
        output_file = date_string + '_modi_' + str(counter) + '.fit'
        Dprint('no Timestamp, using modification time: %s' % (date_string))
    Dprint('timestamp %s' % (timestamp))
    fitpath4renaming = os.path.split(original_filename)[0]
    Iprint ('creating %s in path: %s' % (output_file,fitpath4renaming))
    if not os.path.isfile(os.path.join(fitpath4renaming , output_file)):
        #if os.path.isfile(original_filename):
        Dprint('renaming from %s to %s' % (original_filename,os.path.join(fitpath4renaming,output_file)))
        if not simulation:
            os.rename(original_filename, os.path.join(fitpath4renaming,output_file))
            returncode = 'renamed'
        else:
            Iprint('in simulation mode, skipping renaming')
            returncode = 'simulated_renaming'
    else:
        Iprint("skipping existing File: %s" % (output_file))
        returncode = 'skipped'
    Dprint ('-------------------')
    return(returncode)

if __name__=='__main__':
    main()


