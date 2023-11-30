# funBaConf.py

# $language = "python"
# $interface = "1.0"

from logging import root
import sys
import time
import os

import basic.basicConf as bc
import mef.mefConf as mc
import eoam.eoamVef as eov


###################################################################################
def disSubTitle(child,Title):
    child.send_config(Title )

###################################################################################

def disbEoam(child,nni):
    config_set = [
                f'interface {nni}',
                'ethernet oam disable'
                ]
    child.send_config_set(config_set)

def enbEoamAct(child,nni):
    config_set = [
                f'interface {nni}',
                'ethernet oam enable',
                'ethernet oam mode active'
                ]
    child.send_config_set(config_set)

def enbEoamPsv(child,nni):
    config_set = [
                f'interface {nni}',
                'ethernet oam enable',
                'ethernet oam mode passive'
                ]
    child.send_config_set(config_set)

def confDyingGasp(child,nni):
    config_set = [
                f'interface {nni}',
                'no ethernet oam link-event dying-gasp enable'
                ]
    child.send_config_set(config_set) 

def confLinkFault(child,nni):
    config_set = [
                f'interface {nni}',
                'no ethernet oam link-event link-fault enable'
                ]
    child.send_config_set(config_set) 

def confMonitor(child,nni):
    config_set = [
                f'interface {nni}',
                'ethernet oam link-monitor on', 
                'ethernet oam link-monitor supported' 
                ]
    child.send_config_set(config_set) 

def confRemoteLB(child,nni):
    config_set = [
                f'interface {nni}',
                'ethernet oam remote-loopback supported', 
                'ethernet oam remote-loopback timeout 5' 
                ]
    child.send_config_set(config_set) 

def startRemoteLB(child,nni):
    config_set = [
                'ethernet oam remote-loopback test packet-count 15',
                'ethernet oam remote-loopback test packet-size 1500', 
                f'ethernet oam remote-loopback start interface {nni}',
                'ethernet oam remote-loopback test start'
                ]
    for i in config_set:
        child.send_command(i)

def stopRemoteLB(child,nni):
    child.send_command(f'ethernet oam remote-loopback stop interface {nni} ') 

###################################################################################

def confEoam(host,nni):
    svc = 1
    uni = 1
    with bc.connect(host) as child: 
        time.sleep(1)
        enbEoamAct(child,nni)
        time.sleep(1)

def removeEoam(host,nni):
    svc = 1
    uni = 1
    with bc.connect(host) as child: 
        time.sleep(1)
        disbEoam(child,nni)
        time.sleep(1)

def confBasicEoam(dut1,dut2,nni):
    with bc.connect(dut1) as child: 
        result = []
        confEoam(dut1,nni)
        time.sleep(2) 
        enbEoamPsv(child,nni)
        time.sleep(2) 
        print('#'*3 + ' Ethernet OAM Passive Mode ' + '#'*3 )
        result.append(eov.checkEoamNeighborDisc(dut2,'passive',nni))
        print(result)
        time.sleep(2)
        enbEoamAct(child,nni)
        time.sleep(2) 
        print('#'*3 + ' Ethernet OAM Active Mode ' + '#'*3 )                 
        result.append(eov.checkEoamNeighborDisc(dut2,'active',nni))
        print(result)
        time.sleep(2)
        confDyingGasp(child,nni)
    #    input("Enter!") 
        time.sleep(2)
        print('#'*3 + ' Ethernet OAM dying-gasp ' + '#'*3 )                    
        result.append(eov.checkEoamStatus(dut1,'dying-gasp',nni))
        print(result)
        time.sleep(2)
        confLinkFault(child,nni)
    #    input("Enter!") 
        time.sleep(2)
        print('#'*3 + ' Ethernet OAM link-fault ' + '#'*3 )                      
        result.append(eov.checkEoamStatus(dut1,'link-fault',nni))
        print(result)
        time.sleep(2)
        confMonitor(child,nni)
    #    input("Enter!") 
        time.sleep(2)
        print('#'*3 + ' Ethernet OAM link-monitor ' + '#'*3 )                
        result.append(eov.checkEoamStatus(dut1,'link-monitor',nni))
        print(result)
        time.sleep(2) 
        startRemoteLB(child,nni)
        time.sleep(2)
        print('#'*3 + ' Ethernet OAM Loopback Test(start) ' + '#'*3 )  
        result.append(eov.checkEoamNeighborDisc(dut2,'startLBTest',nni))  
        print(result)
        time.sleep(15) 
        stopRemoteLB(child,nni)
        time.sleep(2)
        print('#'*3 + ' Ethernet OAM Loopback Test(stop) ' + '#'*3 )  
        result.append(eov.checkEoamNeighborDisc(dut2,'stopLBTest',nni))  
        print(result)
        result.append(eov.RLBTestResult(dut1))  
        time.sleep(2)    
        print(result)
        removeEoam(dut1,nni)
        time.sleep(5)
        return result.count('Ok')
