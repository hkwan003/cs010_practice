#!/usr/bin/env python

# @file execute.py
# @author Adam Koehler
# @date June 5, 2013
#
# @brief Python script used to execute programs for N seconds and terminate
#        them if they do not finish in time.
#

import sys
import os
import subprocess
import threading
from time import sleep


##
# @brief A task is a single process that is executed for a given amount of time
#
#       If no time is executed then no timeout will exist and the task will 
#       execute until completion
#
class Task:
    def __init__(self, timeout=None):
        self.timeout = timeout
        self.process = None

    def check_call(self, *args, **kwargs):
        "Essentially subprocess.check_call with kill switch for compatibility."
        
        def target():
            self.process = subprocess.Popen(*args, **kwargs)
            self.process.communicate()
        
        thread = threading.Thread(target=target)
        thread.start()
    
        thread.join(self.timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
    
        if self.process.returncode != 0:
            raise SystemError((self.process.returncode, str(args[0])))
        else:
            return 0



def printUsage():
    # Assumes command has been aliased as run 
    print "usage: run executable_name"
    print "usage: run executable_name timeout_in_seconds"
    print ""
    print "Please use one of the two usage cases displayed above."

def main():
    helpList = ["-h", "-help", "--help"]
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        printUsage()
        sys.exit()
    elif len(sys.argv) == 2: 
        if sys.argv[1] in helpList:
               printUsage()
               sys.exit()
        else:
            cmd = sys.argv[1]
            timeout = 5
    elif len(sys.argv) == 3:
        cmd = sys.argv[1]
        timeout = int(sys.argv[2])
    
    curDirectory = os.getcwd()
    executable_path = os.path.join(curDirectory, cmd)
    
    try:
        if os.path.isfile(executable_path):
            t = Task(timeout)
            t.check_call([executable_path])
        else:
            message = "ERROR:\n\nThe file you wish to execute cannot be found. "
            message += "Make sure you are "
            message += "in the same\ndirectory as the file "
            message += "or you are providing a proper path to it."
            message += "\n\nAttempted to execute file with path:\n   "
            message += executable_path
            print message
    except SystemError as e:
        if e[0][0] == -15:
            message = "Program execution did not complete within allowed "
            message += str(timeout) + " second time period.\n"
            message += "If you wish to increase time allotment then please "
            message += "use alternate 'run' usage.\nType 'run --help' "
            message += "for more information."
        elif e[0][0] == -11:
            message = "Program execution was terminated with a "
            message += "segmentation fault."
        else:
            message = "Program execution was aborted."
        print "\n\n"+message+"\n"
    except:
        pass

if __name__ == "__main__":
    sys.exit(main())
