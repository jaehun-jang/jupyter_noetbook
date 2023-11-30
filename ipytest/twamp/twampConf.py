# funBaConf.py

# $language = "python"
# $interface = "1.0"

from logging import root
import sys
import time
import os

import basic.basicConf as bc
import mef.mefConf as mc
import lldp.lldpVef as llv


def disTitle(child,Title):
    child.sendline('\n') 
    child.sendline(Title )
    child.sendline('\n')

################################################################################### 

### Config TWAMP Server ###	      

def shutInterface(child):
    shut_config_set = ['interface 1/6','shutdown']
    child.send_config_set(shut_config_set)

def noshutInterface(child):
    noshut_config_set = ['interface 1/6','speed 1000','no shutdown']
    child.send_config_set(noshut_config_set)

### Set TWAMP Configuration ###	  
def setTwampConf(child):
    IP_config_set = ['interface vlan 1006','ipv6 enable','ipv6 address 2001:db8:1:1::201/64']
    child.send_config_set(IP_config_set)
    time.sleep(1)        
    TWAMP_config_set = ['interface vlan 1006','twamp session-reflector ','enable','port 862']
    child.send_config_set(TWAMP_config_set)
    time.sleep(1) 
    child.send_command('clear twamp session-reflector Vlan1006 test-session ')

### Create ethernet service ###	  
def confCuEthService(child):
    svc_config_set = ['vlan 1006','ethernet service add evc1006','svlan 1006']
    child.send_config_set(svc_config_set)
    uni_config_set = ['ethernet uni add uni6','map interface 1/6', 'add service evc1006']
    child.send_config_set(uni_config_set)
    nni_config_set = ['ethernet nni add nni1','map interface 1/25', 'add service evc1006']
    child.send_config_set(nni_config_set)

### Delete ethernet service ###	  
def removeCuEthService(child):
    uni_config_set = ['ethernet uni uni6','no map interface', 'del service evc1006']
    child.send_config_set(uni_config_set)
    nni_config_set = ['ethernet nni nni1','no map interface 1/25', 'del service evc1006']
    child.send_config_set(nni_config_set)
    svc_config_set = ['ethernet service del evc1006','vlan 1006']
    child.send_config_set(svc_config_set)

def conftwamp(dut1): 
    with bc.connect(dut1) as child: 
        noshutInterface(child)
        time.sleep(1)        
        confCuEthService(child)
        time.sleep(1)
        setTwampConf(child)               
        time.sleep(1)

def removetwamp(dut1): 
    with bc.connect(dut1) as child: 
        shutInterface(child)
        time.sleep(1) 
        removeCuEthService(child)
        time.sleep(1)

