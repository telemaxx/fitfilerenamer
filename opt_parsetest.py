import os
import sys
import optparse
import glob
from fitparse import FitFile, FitParseError

# DEBUG 0=silent, 1=some infos, 2=many output
VERBOSITY = 2
FIT_DEFAULT_PATH = 'C:\\Users\\top\\BTSync\\SA5\\Documents\\LezyneGpsAlly\\6745th\\'

def main():
    parser = optparse.OptionParser()
    (optionen, args) = parser.parse_args()
    if len(args) == 1: # exact one argument
        print(u"Looking for File or directory: %s" % args[0])
        if args[0][-4:].lower()=='.fit' and os.path.isfile(args[0]): # if the one argument is a file, create a list with one entry
            filelist = [args[0]]
        elif os.path.isdir(args[0]): # if the one argument is a dir, create a list with the fit files
            print("argument given, it is a directory: %s" % (args[0]))
            filelist = create_filelist(args[0])
        else:
            print('argument given, but nothing found')
            input("Press Enter to quit...")
            sys.exit(2)

    elif  len(args) == 0: # no argument given
        print(u"No argument, looking at default Path: %s" % (FIT_DEFAULT_PATH))
        if os.path.isdir(FIT_DEFAULT_PATH): #looking at default path
            print('no argument, but default path exist: %s' % (FIT_DEFAULT_PATH))
            filelist = create_filelist(FIT_DEFAULT_PATH)
        else: # no argument and no defaultlocation found
            print("No Argument and Defaultlocation does not exist: %s" % (FIT_DEFAULT_PATH))
            input("Press Enter to quit...")
            sys.exit(2)
    else: # more than 1 arguments, todo: filtering *.fit
        print('much arguments: %d' % (len(args)))
        filelist = []
        for next_file in args:
            if next_file[-4:].lower()=='.fit' and os.path.isfile(next_file):
                print('file %s' % (next_file))
                print('path %s and filename %s' % os.path.split(next_file))
                filelist.append(next_file)
        if len(filelist) == 0:
            print('no fitfiles found')
            input("Press Enter to quit...")
            sys.exit(6)
    print('fitfiles: %s' % (filelist))
    input("Press Enter to quit...")	



def create_filelist(dir):
    fit_files = glob.glob(os.path.join(dir,'*.[fF][iI][tT]'))
    #fit_files = [dir + file for file in files if file[-4:].lower()=='.fit']
    return(fit_files)

		
if __name__=='__main__':
    main()