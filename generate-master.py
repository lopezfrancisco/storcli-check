#! /usr/bin/python3

import sys
import subprocess
import transform
import config_storcli


if len( sys.argv ) != 2:
    print( "Usage:", sys.argv[0], "storcli-output-file" )
    sys.exit(0)

# Command defined in config_storcli.py file
pOutput = subprocess.run( config_storcli.cmd_detail, stdout=subprocess.PIPE, universal_newlines=True )

fw = open( sys.argv[1], "w" )
transform.saveOutput( pOutput.stdout, fw )
fw.close()
