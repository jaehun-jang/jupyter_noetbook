# funBaVef.py

# $language = "python"
# $interface = "1.0"

import sys
import time
import os

import basic.basicConf as bc

### Check LLDP Neighbor ###

def checkEoamNeighborDisc(host,state,nni):               
    with bc.connect(host) as sub_child:
        command = sub_child.send_command(f'sh ethernet oam discovery interface {nni}')
        # print(command)

        if 'passive' in state:
            # spResult = command.splitlines()
            spResult = command.splitlines()[28].split()
            print(spResult)
            if spResult[1] == 'passive': 
                return 'Ok'
            else:
                return 'Nok'
        elif 'active' in state:
            spResult = command.splitlines()[28].split()
            print(spResult)
            if spResult[1] == 'active': 
                return 'Ok'
            else:
                return 'Nok'
        elif 'startLBTest' in state:
            spResult = command.splitlines()[13].split()
            print(spResult)
            if spResult[2] == 'local': 
                return 'Ok'
            else:
                return 'Nok'
        elif 'stopLBTest' in state:
            spResult = command.splitlines()[13].split()
            print(spResult)
            if spResult[2] == 'no': 
                return 'Ok'
            else:
                return 'Nok'
        else:
            return 'Nok' 
         
def checkEoamStatus(host,state,nni):
    with bc.connect(host) as sub_child:
        command = sub_child.send_command(f'sh ethernet oam status interface {nni}')               
        # print(command)

        if 'dying-gasp' in state:
            spResult = command.splitlines()[47].split()
            print (spResult)  
            if spResult[1] == 'disable': 
                return 'Ok'
            else:
                return 'Nok'
        elif 'link-fault' in state:
            spResult = command.splitlines()[46].split()
            print (spResult) 
            if spResult[1] == 'disable': 
                return 'Ok'
            else:
                return 'Nok'
        elif 'link-monitor' in state:
            spResult = command.splitlines()[18].split()
            print (spResult) 
            if spResult[1] == 'supported(on)': 
                return 'Ok' 
            else:
                return 'Nok' 
        else:
            return 'Nok'   


def RLBTestResult(host): 
    with bc.connect(host) as sub_child:
        command = sub_child.send_command('sh ethernet oam remote-loopback test result ')     
        # print(command)
        cmd_split = command.splitlines()
        read_list = [line for line in cmd_split if line.strip()]       
        spResult = read_list[5] 
        spResult = str(spResult).split()    
        print (spResult)          
        if spResult[6] == '15': 
            return 'Ok'
        else:
            return 'Nok'


