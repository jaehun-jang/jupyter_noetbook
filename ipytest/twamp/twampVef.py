# funBaVef.py

# $language = "python"
# $interface = "1.0"

import sys
import time
import os
import basic.basicConf as bc


### Check LLDP Neighbor ###

def checkTwampResult(host): 
    with  bc.connect(host) as child:
        command = child.send_command('sh twamp session-reflector ') 
        # print(command)
        cmd_split = (command.splitlines())
        read_list = [line for line in cmd_split if line.strip()]
        print(read_list)       
        readResult = str(read_list[10]).split()
        print(readResult)
        if readResult[9] == str(1):
            readResult = str(read_list[12]).split()
            print(readResult)
            return readResult[6]
        else: 
            return 0
  


