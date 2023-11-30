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

def check_pmConf(host,state):
    with bc.connect(host) as child:
        result = []  
        info = child.send_command('show pm info')
        int = child.send_command('sh pm interface 1/1 l0 current')       
        system = child.send_command('sh pm system current')               
        result.extend(info.splitlines()[5].split()[2:5:2])         
        result.append(int.splitlines()[1].split()[8])
        result.append(system.splitlines()[1].split()[9])
        print(result)            
        result_count = result.count(state)
        print(result_count)
        if result_count == 4:
            return True
        else:
            return False

def check_csvConf(host,state):
    with bc.connect(host) as child:
        disExpect = ['Disable','Disable','FTP','-','-','Off','Off','Off','Off','-','-','15','GMT+0']
        enExpect = ['Enable','Enable','SFTP','csv','192.168.0.157','On','On','On','On','On','On','10','Local']
        result = []  
        info = child.send_command('show pm info')    
        csv = child.send_command('sh pm csv-upload status')               
        result.append(info.splitlines()[9].split()[2])    # csv-upload in info      
        result.append(csv.splitlines()[3].split()[2])       # csv-upload in info in csv
        result.append(csv.splitlines()[5].split()[2])       # mode
        result.append(csv.splitlines()[6].split()[2])       # user
        result.append(csv.splitlines()[8].split()[2])       # IP address
        result.extend(csv.splitlines()[14].split()[2:5:2])  # pm
        result.extend(csv.splitlines()[16].split()[2:5:2])  # uplod group
        result.extend(csv.splitlines()[18].split()[3:6:2])  # 24 bin
        result.append(csv.splitlines()[22].split()[2])      # interval
        result.append(csv.splitlines()[26].split()[3])      # time
        print(result)
        if state == 'Disable':           
            if disExpect == result:
                return True
            else:
                return False
        if state == 'Enable':           
            if enExpect == result:
                return True
            else:
                return False

##################################################################################
    
def pmConf(dut1):
    result = []
    with bc.connect(dut1) as child:
        config_commands = ['pm configuration', 'no interface enable', 'no system enable']
        child.send_config_set(config_commands)
        time.sleep(1)
        result.append(check_pmConf(dut1,'Disable'))

        config_commands = ['pm configuration', 'interface enable', 'system enable']
        child.send_config_set(config_commands)
        time.sleep(1)
        result.append(check_pmConf(dut1,'Enable'))

        print(result)
        if result.count(True) == 2 :
            return True
        else:
            return False
    
def csvConf(dut1):
    result = []
    with bc.connect(dut1) as child:
        disconfig_commands = [
                        'pm configuration',
                        'no interface enable', 
                        'no system enable',                         
                        'csv-upload bin del all',
                        'csv-upload group del all',
                        'csv-upload mode ftp',
                        'csv-upload random-interval 15',
                        'csv-upload time-display gmt'
                        ]        
        enconfig_commands = [
                        'pm configuration',
                        'interface enable', 
                        'system enable', 
                        'csv-upload bin add all',
                        'csv-upload group add all',
                        'csv-upload mode sftp',
                        'csv-upload random-interval 10',
                        'csv-upload time-display local',
                        'csv-upload target 192.168.0.157 csv csv ./',
                        'csv-upload enable'
                        ]
        child.send_config_set(disconfig_commands)
        time.sleep(1)
        result.append(check_csvConf(dut1,'Disable'))

        child.send_config_set(enconfig_commands)
        time.sleep(1)
        result.append(check_csvConf(dut1,'Enable'))

        print(result)
        if result.count(True) == 2 :
            return True
        else:
            return False
    

def default_pm(dut1):
    with bc.connect(dut1) as child:
        config_commands = ['pm configuration', 'interface enable', 'system enable']
        child.send_config_set(config_commands)
        time.sleep(1)

def default_csv(dut1):
    with bc.connect(dut1) as child:
        config_commands = [
            'pm configuration', 
            'interface enable', 
            'system enable',
            'no csv-upload target',
            'no csv-upload enable' 
            ]
        child.send_config_set(config_commands)
        time.sleep(1)
