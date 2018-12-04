#! /usr/bin/python3

import difflib
import re
import subprocess
import sys
import tempfile
import time
import transform
import config_storcli


# If this is invoked from cron, let users know the name of the script.
if not sys.stdout.isatty():
    print( "Output from", sys.argv[0], "\n" )

if len( sys.argv ) != 2:
    print( "Usage:", sys.argv[0], "storcli-output-file" )
    sys.exit(0)

# this is the master file which contains the saved output from a prior good storcli run
mf = sys.argv[1]
fh = open( mf, "r" )


diffCount = 0
tmpfh = tempfile.TemporaryFile( mode="w+t" )
# Command defined in config_storcli.py file
pOutput = subprocess.run( config_storcli.cmd_detail, stdout=subprocess.PIPE, universal_newlines=True )
transform.saveOutput( pOutput.stdout, tmpfh )
tmpfh.seek(0)

# compare the output from a previous run with output from the current run
for l in difflib.unified_diff( fh.readlines(), tmpfh.readlines(), mf, tofiledate=time.ctime(), n=0 ):
    if diffCount == 0:
        print( "RAID Changes\n============" )
    print( l.rstrip() )
    diffCount += 1
fh.close()

diskString = "State :"
failString = "\APredictive"
saveString = ""

predictCount = 0
# Command defined in config_storcli.py file
pOutput = subprocess.run( config_storcli.cmd_predict, stdout=subprocess.PIPE, universal_newlines=True )

# look for predictive failures counts that are not zero
for line in pOutput.stdout:
    if re.search( diskString, line ):
        saveString = line.rstrip()
    elif re.search( failString, line ):
        if not re.search( "= 0", line):
            if predictCount == 0:
                if diffCount != 0:
                    print( " " )
                print( "Predict Failure Counts\n======================" )
            print( saveString )
            print( line.rstrip() )
            predictCount += 1

# print the all clear if we didn't see any obvious errors or differences
if diffCount == 0 and predictCount == 0:
    print( "No problems found\n+++++++++++++++++" )
    exitStatus = 0
else:
    exitStatus = 1
print( " " )

sys.exit(exitStatus)
