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
"""

__version__ = '0.64'
__author__ = 'telemaxx'

import os
import sys
import optparse
#import fitparse  # neccercary?
import datetime
import time
import glob
from fitparse import FitFile, FitParseError


# DEBUG 0=silent, 1=some infos, 2=many output
VERBOSITY = 1

# Directory where the FIT Files are located
HOME = os.path.expanduser('~')
FIT_DEFAULT_PATH = os.path.join(HOME,'BTSync','SA5','Documents','LezyneGpsAlly','6745th')
#FIT_DEFAULT_PATH = 'C:\\Users\\top\\BTSync\\SA5\\Documents\\LezyneGpsAlly\\6745th\\'
DEFAULT_MANUFACTURER = 'Samsung-A5-2017' # used, when no manufacturer given or manufacturer is set garmin by oruxmaps
DEFAULT_EVENT_TYPE = 'Cycling'
WAIT_AFTER_JOB_DONE = 10

def main():
    parser = optparse.OptionParser(usage="usage: %prog filename1.fit filename2.fit or %prog dirname or %prog [option]",version='%prog  {version}'.format(version=__version__))
    (optionen, args) = parser.parse_args()
    if len(args) == 1:
        Dprint(u"Looking for File or Directory: %s" % args[0])
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
        Dprint(u"No argument, looking at default Path: %s" % (FIT_DEFAULT_PATH))
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

    file_count = 0
    for file in filelist:
        Dprint('processing %s' % (file))
        Dprint('start datafitprocessor')
        if not os.path.isfile(file):
            Iprint('skipping folder: %s' % (file))
            continue
        try:
            fitfile = FitFile(file)
            Dprint('parsing start')
            fitfile.parse()
            Dprint('parsing done')
        except FitParseError as e:
            Iprint('skipping defective fitfile %s' % (file))
            for m in e.args:
                Dprint('Exception: %s' % (m))
            continue
        #Dprint('rename arguments: %s , %s , %d' % (fitfile, file, file_count))
        rename_fitfile(fitfile, file, file_count)
        file_count += 1
    Iprint('finished processing %d file(s)' % (file_count))
    final_message('wait %d sec or press strg c' % (WAIT_AFTER_JOB_DONE))



def Dprint(text2print):
    if VERBOSITY == 2:
        print(text2print)

def Iprint(text2print):
    if VERBOSITY != 0:
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
                Dprint("manufacturer %s" % (f.value))
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
    if VERBOSITY > 0:
        try:
            time.sleep(WAIT_AFTER_JOB_DONE)
        except KeyboardInterrupt:
            pass

#(fitfile, file, file_count)
def rename_fitfile(fitfile, original_filename=None, counter=0):
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
    Dprint("enhanced_altitude %s" % (climb))
    Dprint('analyzing done')
    if timestamp is not None:
        output_file = timestamp.strftime('%Y-%m-%d_%H-%M-%S') + '_' + manufacturer + '_' + climb + 'hm_' + str(counter) + '.fit'        
    else:
        modified_time = os.stat(original_filename).st_mtime
        date_string=time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(modified_time))
        output_file = date_string + '_modi_' + str(counter) + '.fit'
        Dprint('no Timestamp, using modification time: %s' % (date_string))
    Dprint("timestamp %s" % (timestamp))
    fitpath4renaming = os.path.split(original_filename)[0]
    Iprint ('creating %s in path: %s' % (output_file,fitpath4renaming))
    if not os.path.isfile(os.path.join(fitpath4renaming , output_file)):
        #if os.path.isfile(original_filename):
        Dprint("renaming orig, FITPATH+'\\'+outputfile %s %s" % (original_filename,os.path.join(fitpath4renaming,output_file)))
        os.rename(original_filename, os.path.join(fitpath4renaming,output_file))
    else:
        Iprint("skipping existing File: %s" % (output_file))
    Dprint ('-------------------')

if __name__=='__main__':
    main()


