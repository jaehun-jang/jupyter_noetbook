# funBaVef.py

# $language = "python"
# $interface = "1.0"

import sys
import time
import os
import basic.basicConf as bc


### Check LLDP Neighbor ###

def checkLldpNeighborTlvC(host,state): 
    with  bc.connect(host) as sub_child:
        command = sub_child.send_command('sh lldp neighbor')
        # print(command)
        cmd_split = (command.splitlines())
        read_list = [line for line in cmd_split if line.strip()]       
        readcount = len(read_list)

        print ('PRINT: ' + str(readcount))      

        if 'default' in state:
            if readcount == 40: 
                return 'Ok' 
            else:
                return 'Nok'
        elif 'enable' in state: 
            if readcount == 40: 
                return 'Ok' 
            else:
                return 'Nok'
        elif 'disable' in state:
            if readcount == 0: 
                return 'Ok' 
            else:
                return 'Nok'       
        else:
            return 'Nok'   

def checkLldpNeighborTlvCF(host,count): 
    with  bc.connect(host) as sub_child:
        countList = [ 39,38,37,34,32,30,29,22,18,14,14,11,11,11,12,13,14,17,19,21,22,29,33,37,37,40,40,40]
        command = sub_child.send_command('sh lldp neighbor')
        cmd_split = command.splitlines() 
        read_list = [line for line in cmd_split if line.strip()]       
        readcount = len(read_list)
        print ('PRINT TLV Count: ' + str(countList[count]), readcount)              
        return 'Ok' if readcount == countList[count] else 'Nok'

def checkLldpNeighborTlvD(host,state):                 
    with  bc.connect(host) as sub_child:              
        command = sub_child.send_command('sh lldp neighbor')
        cmd_split = command.splitlines() 
        read_list = [line for line in cmd_split if line.strip()]           

        if 'mgmt-subtype' in state:
            spResult = read_list[15]
            spResult = str(spResult).split(':')
            print(spResult)
            if spResult[1] == ' All 802': 
                return 'Ok'
            else:
                return 'Nok'
        elif 'lldp-timer'in state:
            spResult = read_list[6]
            spResult = str(spResult).split(':')
            print(spResult)
            if spResult[1] == ' 40': 
                return 'Ok'
            else:
                return 'Nok'
        elif 'sys-mgmt'in state:
            spResult = read_list[17]
            spResult = str(spResult).split(':')
            print(spResult)
            if spResult[1] == ' 25001  ':
                return 'Ok'
            else:
                return 'Nok'
