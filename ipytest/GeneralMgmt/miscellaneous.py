# funBaConf.py

# $language = "python"
# $interface = "1.0"

from logging import root
import unittest
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
        # print(cmd_split)       
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

def check_mirror(host,nni,direction):
    with bc.connect(host) as child:  
        command = child.send_command('show mirror')       
        if direction == "transmit":
            if len(command.splitlines()) == 0:
                return True
            else:
                return False
        else:         
            dst = command.splitlines()[0].split()[4]         
            dir = command.splitlines()[2].split()[2]
            src = command.splitlines()[3].split()[3] 

            if direction == "both":
                print(f'mirror dst: {dst}, dir: {dir}, src: {src}')
                if  dst == '1/2' and dir == 'both' and src == nni:
                    return True
                else:
                    return False
            
            elif direction == "receive":
                print(f'mirror dst: {dst}, dir: {dir}, src: {src}')
                if  dst == '1/2' and dir == 'transmit' and src == nni:
                    return True
                else:
                    return False 


def check_feature(host,connection,state):
    if connection == 'telnet':
        with bc.telnet(host) as child:
            result = []  
            gnmi = child.send_command('show gnmi agent')
            '// Added to remove empty space //'
            shGnmi_split = (gnmi.splitlines())
            gnmi_list = [line for line in shGnmi_split if line.strip()] 
            
            netconf = child.send_command('show netconf agent')       
            ssh = child.send_command('show ssh server')               
            result.append(gnmi_list[1].split(':')[1].strip())         
            result.append(netconf.splitlines()[1].split()[1])
            result.append(ssh.splitlines()[0].split()[2])
            print(result)            
            result_count = result.count(state)
            print(result_count)
            if result_count == 3:
                return True
            else:
                return False
    else:
        with bc.connect(host) as child:
            result = []         
            telnet = child.send_command('show telnet server')               
            result.append(telnet.splitlines()[0].split()[1])
            print(result)   
            result_count = result.count(state)
            print(result_count)
            if result_count == 1:
                return True
            else:
                return False  
             
##################################################################################
    
def tcpdump(dut1): 
    with bc.connect(dut1) as child: 
        command = child.send_command('tcpdump -vi eth0', expect_string= 'length')
        time.sleep(1) 
        # print(command)
        child.write_channel('\x03')
        result = command.splitlines() 
        resultlen = len(result) 
        print(f'tcpdump count: {resultlen}')
        return resultlen

def traceRT(dut1): 
    dnsserver = '168.126.63.1'
    with bc.connect(dut1) as child: 
        command = child.send_command(f'traceroute {dnsserver}', expect_string= 'ms')   
        time.sleep(1)
        print(command)
        ctlPC = child.write_channel('\x03')  
        result = command.splitlines()[-2].split()[1]
        print(result)
        return result

def mirror(dut1,nni):
    result = []
    with bc.connect(dut1) as child:
        config_commands = ['interface 1/2', f'mirror interface {nni} direction both']
        child.send_config_set(config_commands)
        time.sleep(1)
        result.append(check_mirror(dut1,nni,'both'))

        config_commands = ['interface 1/2', f'no mirror interface {nni} direction receive']
        child.send_config_set(config_commands)
        time.sleep(1)
        result.append(check_mirror(dut1,nni,'receive'))

        config_commands = ['interface 1/2', f'no mirror interface {nni} direction transmit']
        child.send_config_set(config_commands)
        time.sleep(1)
        result.append(check_mirror(dut1,nni,'transmit'))

        print(result)
        if result.count(True) == 3:
            return True
        else:
            return False
    
def feature(dut1):
    result = []
    with bc.telnet(dut1) as child:
        config_commands = ['no feature gnmi', 'no feature netconf', 'no feature ssh']
        child.send_config_set(config_commands)
        time.sleep(1)
        result.append(check_feature(dut1,'telnet','disabled'))

        config_commands = ['feature gnmi', ' feature netconf', 'feature ssh']
        child.send_config_set(config_commands)
        time.sleep(1)
        result.append(check_feature(dut1,'telnet','enabled'))
            
    with bc.connect(dut1) as child:
        config_commands = ['no feature telnet']
        child.send_config_set(config_commands)
        time.sleep(1)
        result.append(check_feature(dut1,'ssh','disabled'))

        config_commands = ['feature telnet']
        child.send_config_set(config_commands)
        time.sleep(1)
        result.append(check_feature(dut1,'ssh','enabled'))
    print(result)
    if result.count(True) == 4 :
        return True
    else:
        return False
    

def default_feature(dut1):
    with bc.connect(dut1) as child:
        config_commands = ['no feature gnmi','feature netconf','feature ssh','feature telnet']
        child.send_config_set(config_commands)
        time.sleep(1)
