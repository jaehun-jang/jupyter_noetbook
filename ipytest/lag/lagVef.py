# funBaVef.py

# $language = "python"
# $interface = "1.0"

import sys
import time
import os
import basic.basicConf as bc

### Check port-channel ###
def checkPortChannel(host, state,lagin):
    with bc.connect(host) as child:
        results = []
        pass_count = 0
        command = child.send_command('show port-channel summary')
        results.extend(command.splitlines()[8].split())
    print(results)
    check_lists = {'static': ['po1', '(SU)', 'NONE', lagin[0]+'(P)*', lagin[1]+'(P)'],
                    'lacp': ['(SU)', 'LACP', '8', lagin[0]+'(P)', lagin[1]+'(P)'],
                    'hotstandby': ['(SU)', 'LACP', '1', lagin[0]+'(P)', lagin[1]+'(D)']}
    for i in check_lists[state]:
        pass_count += results.count(i)
    # print(pass_count)
    if state == 'hotstandby':
        return 'Ok' if pass_count == 6 else 'Nok'
    else:
        return 'Ok' if pass_count == 5 else 'Nok'    

def checkLacpInternal(host, state):                  
    with bc.connect(host) as child:
        command = child.send_command('sh lacp 1 internal ')
        # print(command)
        results = command.splitlines()[8:10]
        results = str(results).split()
        print(results) 
    check_lists = {'active': ['FA', 'bndl'],
                   'passive': ['FP', 'bndl'],
                   'hotstandby': ['FP', 'standby']}
    pass_count = sum(results.count(i) for i in check_lists[state])
    # print(pass_count)
    if state == 'hotstandby':
            return 'Ok' if pass_count == 3 else 'Nok'
    else:
        return 'Ok' if pass_count == 4 else 'Nok'

def checkBcmPort(host,state):                 
    with bc.connectbcm(host) as child: 
        child.send_command('debug no-auth')
        child.send_command('bcm-shell',expect_string='BCM.0>')
        command = child.send_command('ps',expect_string='BCM.0>')
        cmd_split = command.splitlines()
        read_list = [line for line in cmd_split if line.strip()]    
        readResult = str(read_list[17]).split()
        print(readResult)
    if state == 'hotstandby' and readResult[7] == 'Block': 
        return 'Ok' 
    elif state == 'normal' and readResult[7] == 'Forward': 
        return 'Ok' 
    else:
        return 'Nok'

 
# def check_mng_gw(child,state):
    successExpect = ['enable','10','1','192.168.0.2','success','normal']
    failureExpect = ['enable','11','2','10.1.1.1','failure','fail']
    result = []  
    command = child.send_command('show mng ping') 
    cmd_split = (command.splitlines())
    command_list = [line for line in cmd_split if line.strip()] 
    # print(type(command_list),command_list )               
    result.append(command_list[2].split()[2]) 
    result.append(command_list[3].split()[2])
    result.append(command_list[4].split()[2])  
    result.append(command_list[5].split()[3]) 
    result.append(command_list[10].split()[3]) 
    result.append(command_list[11].split()[3])         
    print(result)            
    if state == 'normal':           
        if successExpect == result:
            return True
        else:
            return False
    if state == 'failure':           
        if failureExpect == result:
            return True
        else:
            return False