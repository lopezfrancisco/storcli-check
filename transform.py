import re

def saveOutput( readfh, writefh ):
    convertDriveStatus = False
    separatorCount = 0

    isTopologyHeader = re.compile( "DG Arr Row EID:Slot DID Type  State BT       Size PDC  PI SED DS3  FSpace TR " )
    isUnconfiguredHeader = re.compile( "EID:Slt DID State DG     Size Intf Med SED PI SeSz Model            Sp Type " )
    isSeparator = re.compile( "^-+$" )
    
    for line in readfh.splitlines():
        if convertDriveStatus:
            if isSeparator.match( line ):
                if separatorCount == 1:
                    separatorCount = 0
                    convertDriveStatus = False
                else:
                    separatorCount += 1
            else:
                if line[36] == "Y":
                    # set background task status to N for topology report
                    line = line[0:36] + "N" + line[37:]
                elif line[68] == "U" or line[68] == "T":
                    # set drive spun status to D for un-configured drives report
                    line = line[0:68] + "D" + line[69:]
        else:
            if isTopologyHeader.match( line ) or isUnconfiguredHeader.match( line ):
                convertDriveStatus = True
        writefh.write( line + "\n" )
