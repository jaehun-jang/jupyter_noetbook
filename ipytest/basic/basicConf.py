# funBaConf.py

# $language = "python"
# $interface = "1.0"

from logging import root
from netmiko import ConnectHandler
import paramiko
import sys
import time
import os

def login(testName):
    child = connect() 
    fout = open('./log/' + testName +'_log.txt', 'wt' )
    child.logfile = fout
    child.logfile_read = sys.stdout
    return child

def connect(host):
    login ={
        'device_type':'cisco_ios',
        'ip': host, 
        'username':'root', 
        'password':'admin',
        'session_timeout': 120,
        'timeout': 120,
        'global_delay_factor': 2,
        }
    device = ConnectHandler(**login)
    device.enable() ## Enable mode ##
    return device

def telnet(host):
    login ={
        'device_type':'cisco_ios_telnet',
        'ip': host, 
        'username':'root', 
        'password':'admin',
        'session_timeout': 120,
        'timeout': 120,
        'global_delay_factor': 2,
        }
    device = ConnectHandler(**login)
    device.enable() ## Enable mode ##
    return device

def connectbcm(host):
    login ={
        'device_type':'cisco_ios',
        'ip': host, 
        'username':'root', 
        'password':'admin',
        'session_timeout': 120,
        'timeout': 120,
        'global_delay_factor': 2,
        }
    device = ConnectHandler(**login)
    # with ConnectHandler(**login) as device:
    return device
                      
### Print Title  ###	
def disTitle(devices,Title):
    for host in devices: 
        with connect(host) as child:
            child.send_command(Title)

def defaultSetup(devices,blockport):
    for host in devices:    
        with connect(host) as child:
            child.enable()
            default_config = ["logging console", "aaa auth attempts login 0"]
            child.send_config_set(default_config)
            int_shutdown_config = f'interface range {blockport}', "shutdown"
            child.send_config_set(int_shutdown_config)
            time.sleep(1)
            hostname_config = {
                "192.168.0.201": "hostname LAB1",
                "192.168.0.202": "hostname LAB2",
                "192.168.0.203": "hostname LAB3", 
                "192.168.0.211": "hostname LAB4"
                } 
            """  Using Dictionary """
            if host in hostname_config:
                child.send_config_set(hostname_config[host])
                time.sleep(1)

def defaultFor6424(host,blockport):
    with connect(host) as child:
        child.enable()
        default_config = ["logging console", "aaa auth attempts login 0"]
        child.send_config_set(default_config)
        int_shutdown_config = f'interface range {blockport}', "shutdown"
        child.send_config_set(int_shutdown_config)
        time.sleep(1)
        hostname_config = {
            "192.168.0.201": "hostname LAB1",
            "192.168.0.202": "hostname LAB2",
            "192.168.0.211": "hostname LAB3", 
            "192.168.0.212": "hostname LAB4"
            } 
        """  Using Dictionary """
        if host in hostname_config:
            child.send_config_set(hostname_config[host])
            time.sleep(1)
            
def noshutblockport(hosts,blockport): 
    for host in hosts:
        with connect(host) as child:   
            config_set = [f'interface range {blockport}', 'no shutdown']
            child.send_config_set(config_set)
            time.sleep(1) 

def shutblockport(hosts,blockport):
    for host in hosts: 
        with connect(host) as child:              
            config_set = [f'interface range {blockport}', 'shutdown']
            child.send_config_set(config_set)
            time.sleep(1) 

def noshutStpBlockPort(hosts,stpblockport): 
    for host in hosts: 
        with connect(host) as child:   
            config_set = [f'interface range {stpblockport}', 'no shutdown']
            child.send_config_set(config_set)
            time.sleep(1) 

def shutStpBlockPort(hosts,stpblockport): 
    for host in hosts: 
        with connect(host) as child:              
            config_set = [f'interface range {stpblockport}', 'shutdown']
            child.send_config_set(config_set)
            time.sleep(1) 
                        
### Create maximum numberof VLAN  ###	  
def crtVlan(host,vlans):
    with connect(host) as sub_child:
        result= sub_child.send_config_set('vlan 2-%s' % str(vlans))
        return result 

def addiproute(host):
    with connect(host) as sub_child:
        sub_child.send_config_set('ip route 0.0.0.0/0 192.168.0.2')
        pass 

def ping(host):
    with connect(host) as child:
        if host == '192.168.0.201':
            command = child.send_command('ping 168.126.63.1', expect_string= 'icmp_seq=10')
            time.sleep(5)
            print(command)
            child.write_channel('\x03') 
            result = command.splitlines()[-1].split()[4]
            if result == 'icmp_seq=10':
                return True
            else:
                return False

        if host == '192.168.0.211':
            command = child.send_command('ping 168.126.63.1')
            time.sleep(7)
            print(command)
            result = command.splitlines()[-2].split()[5]
            if result == '0%':
                return True
            else:
                return False 

### Delet maximum numberof VLAN  ###	  
def dltVlan(host,vlans):
    with connect(host) as child:
        if vlans == 1:
            return
        else:
            child.send_config_set("no vlan 2-%s" % str(vlans))    
            time.sleep(1) 

### Delet maximum numberof VLAN  ###	  
def dltDevVlan(host,vlans):
    with connect(host) as sub_child:
        if vlans == 1:
            return
        else:
            groups = []
            quotient, remainder = divmod(vlans, 10)
            start = 1
            for i in range(10):
                if remainder > 0:
                    end = start + quotient
                    remainder -= 1
                    sub_child.send_config_set("no vlan %s-%s" % (str(start), str(end)))
                else:
                    end = start + quotient - 1
                    sub_child.send_config_set("no vlan %s-%s" % (str(start), str(end)))
                groups.append([start, end])
                start = end + 1
        time.sleep(0.5) 

def defVlan(host):
    with connect(host) as sub_child:
        sub_child.send_config_set("no vlan 2-4095" )

### Config maximum numberof vty session  ###	  
def confVty(host,vty):
    with connect(host) as sub_child:
        sub_child.send_config_set("no line vty %s 39" % vty)

### Restore maximum numberof vty session  ###	  
def deftVty(host):
    with connect(host) as child:
        child.send_config_set("line vty 0 39")
       
### Restore maximum numberof vty session  ###	  
def deftSystem(host):
    with connect(host) as child:   
        child.send_command('write memory') 
        write = child.send_command_timing('write default')
        write += child.send_command_timing('y')
        reload = child.send_command_timing('reload')
        reload += child.send_command_timing('n')
        reload += child.send_command_timing('y')
        time.sleep(180) 

def chgProfile(host,profile):
    with connect(host) as child:   
        child.send_command('write memory') 
        write = child.send_command_timing(f'write profile {profile}')
        write += child.send_command_timing('y')
        reload = child.send_command_timing('reload')
        reload += child.send_command_timing('n')
        reload += child.send_command_timing('y')
        time.sleep(180) 
        
def deliproute(host):
    with connect(host) as sub_child:
        sub_child.send_config_set('no ip route 0.0.0.0/0 192.168.0.2')
        pass


### Detach ###  
def translate(host):
    with connect(host) as child:
        for intCon in range(10, 17):
            config_set = [f'flexport-group {intCon}', 'detach']
            child.send_config_set(config_set)
            time.sleep(1.5)
        config_set = [f'flexport-group 9', 'max-speed 25 ']
        child.send_config_set(config_set)
        time.sleep(1.5)

### Send CLI in configuration mode ###          
def sendConfigSet(host,command):
    with connect(host) as child:
        child.send_config_set(command)
        time.sleep(2)
        