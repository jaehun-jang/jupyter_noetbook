# funBaConf.py

# $language = "python"
# $interface = "1.0"

from logging import root
import sys
import time
import os
import basic.basicConf as bc
import mef.mefConf as mc
import lag.lagVef as lav


def disSubTitle(child,Title):
    child.send_command(Title )


def staticLag(child,lagin):
    config_set = [
                f'interface {lagin[0]}',  
                'channel-group 1 mode on working',
                f'interface {lagin[1]}',
                'channel-group 1 mode on protection'
    ]
    child.send_config_set(config_set)

def activeLacp(child,lagin):
    config_set = [
                f'interface {lagin[0]}',  
                'channel-group 1 mode active',
                'lacp timeout short',
                f'interface {lagin[1]}',
                'channel-group 1 mode active',
                'lacp timeout short'
    ]
    child.send_config_set(config_set)

def passiveLacp(child,lagin):
    config_set = [
                f'interface {lagin[0]}',  
                'channel-group 1 mode passive',
                'lacp timeout short',
                f'interface {lagin[1]}',
                'channel-group 1 mode passive',
                'lacp timeout short'
    ]
    child.send_config_set(config_set)

def changeMaxMember(child,maxmember):
    child.send_config_set(f'port-channel 1 max-member {maxmember}')

def delNniInt(child):
    config_set = ['ethernet nni nni1', 'no map interface']
    child.send_config_set(config_set)    

def addNniInt(child):
    config_set = ['ethernet nni nni1', 'map interface po1']
    child.send_config_set(config_set)     

def delPortCh(child,lagin):    
    config_set = [f'interface range {lagin[0]}-{lagin[1]}', 'no channel-group']
    child.send_config_set(config_set)

def deflacpTime(child,lagin):    
    config_set = [f'interface range {lagin[0]}-{lagin[1]}', 'lacp timeout long']
    child.send_config_set(config_set)

def noshutLagInt(child,lagin):    
    config_set = [f'interface range {lagin[0]}-{lagin[1]}', 'no shutdown']
    # config_set = ['interface po1', 'no shutdown']
    child.send_config_set(config_set)

def shutLagInt(child,lagin):    
    config_set = [f'interface range {lagin[0]}-{lagin[1]}', 'shutdown']
    # config_set = ['interface po1', 'shutdown']
    child.send_config_set(config_set)

###################################################################################

### Static Link Aggregation ###	  
def confLag(host,lagin):
    with bc.connect(host) as child:
        time.sleep(1)
        delNniInt(child)
        time.sleep(1)
        staticLag(child,lagin)
        time.sleep(1)
        addNniInt(child)
        time.sleep(1)
        noshutLagInt(child,lagin)
        time.sleep(1)

### Static Link Aggregation ###	  
def confLacp(host,lagin):
    with bc.connect(host) as child:
        time.sleep(1)
        delNniInt(child)
        time.sleep(1)
        activeLacp(child,lagin)
        time.sleep(1)
        addNniInt(child)
        time.sleep(1)
        noshutLagInt(child,lagin)
        time.sleep(5)

### Pure Static Link Aggregation ###	  
def removeLag(host,lagin):
    with bc.connect(host) as child:
        shutLagInt(child,lagin)
        time.sleep(1)
        delNniInt(child)
        time.sleep(1)
        delPortCh(child,lagin)
        time.sleep(1)   


### Pure Static Link Aggregation ###	  
def removeLacp(host,lagin):
    with bc.connect(host) as child:
        svc = 1
        uni = 1
        shutLagInt(child,lagin)
        time.sleep(1)
        delNniInt(child)
        time.sleep(1)
        deflacpTime(child,lagin)
        time.sleep(1)
        delPortCh(child,lagin)
        time.sleep(1)   
        mc.dltServi(host,svc,uni)
        time.sleep(1)

### Redundant Static Link Aggregation ###	  

def confStaticLag(host,lagin):
        result = []
        confLag(host,lagin)
        print('#' * 3 + ' check static channel-group ' + '#' * 3)
        result.append(lav.checkPortChannel(host,'static',lagin))
        time.sleep(1)
        print('#' * 3 + ' check BCM Port state ' + '#' * 3)
        result.append(lav.checkBcmPort(host,'hotstandby'))
        print(result)
        return result.count('Ok')

def confBasicLacp(host,lagin): 
    with bc.connect(host) as child: 
        result = []
        confLacp(host,lagin)
        time.sleep(10)
        print('#' * 3 + ' check lacp active Mode ' + '#' * 3)
        result.append(lav.checkPortChannel(host,'lacp',lagin))
        result.append(lav.checkLacpInternal(host,'active')) 
        time.sleep(1)
        delNniInt(child)
        time.sleep(1)
        passiveLacp(child,lagin)
        time.sleep(1)    
        addNniInt(child)
        time.sleep(5)
        print('#' * 3 + ' check lacp passive Mode ' + '#' * 3)    
        result.append(lav.checkPortChannel(host,'lacp',lagin))
        result.append(lav.checkLacpInternal(host,'passive'))
        time.sleep(1)
        changeMaxMember(child,1)
        time.sleep(5)
        print('#' * 3 + ' check lacp MaxMember 1 ' + '#' * 3) 
        result.append(lav.checkPortChannel(host,'hotstandby',lagin))
        result.append(lav.checkLacpInternal(host,'hotstandby'))
        time.sleep(1)
        print('#' * 3 + ' check BCM Port state ' + '#' * 3)            
        result.append(lav.checkBcmPort(host,'hotstandby'))
        changeMaxMember(child,8)
        time.sleep(5)
        print('#' * 3 + ' check lacp MaxMember 8 ' + '#' * 3) 
        result.append(lav.checkPortChannel(host,'lacp',lagin))
        result.append(lav.checkLacpInternal(host,'passive'))
        time.sleep(1)  
        result.append(lav.checkBcmPort(host,'normal'))
        time.sleep(1)
        removeLacp(host,lagin)  
        print(result)  
        return result.count('Ok')

