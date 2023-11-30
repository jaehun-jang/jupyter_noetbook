# funBaConf.py

# $language = "python"
# $interface = "1.0"

from logging import root
import sys
import time, datetime
import os

import basic.basicConf as bc
import mef.mefConf as mc
import lldp.lldpVef as llv


def disTitle(child,Title):
    child.sendline('\n') 
    child.sendline(Title )
    child.sendline('\n')

################################################################################### 
### Check LLDP Neighbor ###

def checkntpconf(host): 
    with bc.connect(host) as child:  
        command = child.send_command('show ntp associations')        
        cmd_split = command.splitlines()[1].split()
        print(cmd_split)       
        readResult = str(cmd_split[0])
        print(f"Server status: {readResult}")
        if readResult == '*~106.247.248.106':
            return True
        else: 
            return False

def checktime(host):
    with bc.connect(host) as child:  
        command = child.send_command('show clock')         
        cmd_split = command.splitlines()[0] 
        #output_string = cmd_split[:5] + cmd_split[8:] # To delete :%S 
        output_string = cmd_split[:2] + cmd_split[8:] # To delete %M:%S 
        print(f"Current time: {output_string}")
        return output_string

def checkmaxntpserver(host):
    with bc.connect(host) as child:  
        command = child.send_command('show ntp associations')        
        cmd_split = command.splitlines()[1:5] 
        output_string = str(cmd_split)
        output_string.split()       
        servercount = output_string.count('~1')
        print(f"server count: {servercount}")
        return servercount

##################################################################################
    
### Set TWAMP Configuration ###	  
def ntpConf(dut1): 
    with bc.connect(dut1) as child: 
        TIME_config_set = ('clock set 00:00:00 1 1 2002')
        child.send_command(TIME_config_set)    
        time.sleep(1)
        time_zone_config_set = ['time-zone asia seoul']
        child.send_config_set(time_zone_config_set)        
        time.sleep(1)    
        NTP_config_set = ['ntp server 106.247.248.106 prefer']
        child.send_config_set(NTP_config_set)
        time.sleep(1) 
       
def maxntpserver(dut1): 
    with bc.connect(dut1) as child:    
        NTP_config_set = [
            'ntp server 10.1.1.1',
            'ntp server 10.1.1.2' ,
            'ntp server 10.1.1.3' ,
            'ntp server 106.247.248.106 prefer'
        ]
        for command in NTP_config_set:
            child.send_config_set(command)
            time.sleep(1)

def overmaxntpserver(dut1): 
    with bc.connect(dut1) as child:    
        NTP_config_set = ['ntp server 100.1.1.1']
        result = child.send_config_set(NTP_config_set)
        time.sleep(1)
        if "Error ntp entry is full" in result:
            return True
        else:
            return False     

def delntpconfe(dut1): 
    with bc.connect(dut1) as child: 
        time_zone_config_set = ['time-zone europe london']
        child.send_config_set(time_zone_config_set)        
        time.sleep(1)  
        NTP_config_set = ['no ntp server 106.247.248.106']
        child.send_config_set(NTP_config_set)
        time.sleep(1) 

def delmaxntpserver(dut1): 
    with bc.connect(dut1) as child:    
        NTP_config_set = [
            'no ntp server 10.1.1.1',
            'no ntp server 10.1.1.2',
            'no ntp server 10.1.1.3' ,
            'no ntp server 106.247.248.106' ,
        ]
        for command in NTP_config_set:
            child.send_config_set(command)
            time.sleep(1)