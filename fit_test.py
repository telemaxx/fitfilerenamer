import sys

from fitparse import FitFile, FitParseError

# set to 1 to get some more debug, or 0 to be more silent
DEBUG = 1
#FIT_FILE = 'C:\\Users\\top\\BTSync\\SA5\\Documents\\LezyneGpsAlly\\6745th\\activity-activity-filecrc.fit'
FIT_FILE = 'C:\\Users\\top\\BTSync\\SA5\\Documents\\LezyneGpsAlly\\6745th\\test.fit'

try:
    fitfile = FitFile(FIT_FILE)
    print('parsing start')
    fitfile.parse()
    print('parsing done')
except FitParseError as e:
    for m in e.args:
        print(m)
    print('args',e.args[0])
    print ('Error while parsing .FIT file: %s' % FIT_FILE)
    input("Press Enter to quit...")
    sys.exit(1)
print('getmessages')
messages = fitfile.messages
print('messages done')
enh_alt_max=0.0
for m in messages:
    #print('messages %s' % (m))
    fields = m.fields
    for f in fields:
        #print('field %s' % (f))
        if f.name == 'enhanced_altitude':
        #if 'created' in f.name:
            if f.value > enh_alt_max:
                enh_alt_max = f.value
            #print('value %f' % (f.value))
            if isinstance(f.value,int):
                dumyy=2
                #print('timestamp is integer: %d' % (f.value))
                #return None
            else:
                #print('timename and timestamp %s %s' % (f.name,f.value))
                dummy=1
                #return f.value
#print (messages)
print (enh_alt_max)
