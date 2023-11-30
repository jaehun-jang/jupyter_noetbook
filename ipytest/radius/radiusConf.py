
import pytest, sys, time, os, logging ,datetime ,pyautogui
from netmiko import ConnectHandler
import basic.basicConf as bc

RADIUS_Server1 = '192.168.0.157'
RADIUS_Server2 = '192.168.6.1'

def configAaaRadius(host):
    with bc.connect(host) as child:
        child.enable()
        config_commands = [
            # f"radius-server host {RADIUS_Server1} key radius auth-port 1812",
            f"radius-server host {RADIUS_Server2} key radius auth-port 1812",
            "radius-server retransmit 1",
            "radius-server timeout 1", 
            "aaa auth login default group radius",
            "aaa auth login default fallback error local", 
            "aaa auth attempts login 0"
        ]
        output = child.send_config_set(config_commands)
        print(output)

def removeAaaRadius(host):
    with bc.connect(host) as child:
        child.enable()
        config_commands = [
            "no aaa auth attempts login ",
            "no aaa auth login default group radius",
            "no aaa auth login default fallback error local",
            "no radius-server retransmit ",
            "no radius-server timeout ",
            # f"no radius-server host {RADIUS_Server1}",             
            f"no radius-server host {RADIUS_Server2}"
        ]
        output = child.send_config_set(config_commands)
        print(output)

def privilige(net_connect,role):
        print('# Check user privilige #')
        if role == 'network-admin':
            net_connect.enable()
            config_commands = [
                " username radius password radius123" 
            ]
            output = net_connect.send_config_set(config_commands)
            print(output)
            if "%" in output:
                return False
            else:
                return True

        elif role == 'network-operator':
            net_connect.enable()
            config_commands = [
                "username" 
            ]
            output = net_connect.send_config_set(config_commands)
            print(output)
            if "%" in output:
                return True 
            else:
                return True

        elif role == 'network-viewer':
            output = net_connect.send_command("config terminal")
            print(output)
            if "%" in output:
                return True
            else:
                return True

def login_with_credentials(device, username, password,role):
    try:
        temp_device = device.copy()
        temp_device['username'] = username
        temp_device['password'] = password        
        net_connect = ConnectHandler(**temp_device)  
        command1 = net_connect.send_command('show users')
        print(command1) 
        checkPriv = privilige(net_connect,role)
        print(f"Successful login - Username: {username}, Password: {password}")      
        net_connect.disconnect()
        if checkPriv == True:
            return True 
    except Exception as e:
        print(f"Failed login - Username: {username}, Password: {password}")
        print(e)
        return False

def checklogin(host):
    ssh_device = {
        'device_type': 'cisco_ios',
        'ip': host,
        'username': 'root',
        'password': 'admin',
        'port': 22
    }
    telnet_device = {
        'device_type': 'cisco_ios_telnet',
        'ip': host,
        'username': 'root',
        'password': 'admin',
        'port': 23,
        'timeout': 30,
    }
    new_users = [
        ('root', 'admin','network-admin'),
        ('admin', 'hfrn','network-admin'),
        ('operator', 'hfrn','network-operator'),
        ('viewer', 'hfrn','network-viewer'),
    ]
    okcount = [] 

    '// For Telnet Connection //'
    print('# For RADIUS authentication with Telnet #')
    for new_username, new_password, role in new_users:  
        result = login_with_credentials(telnet_device, new_username, new_password, role)
        print(result)
        if result == True:
            okcount.append('Ok')
        else:
            okcount.append('Nok')
        time.sleep(2) 

    '// For SSH Connection //'
    print('# For RADIUS authentication with SSH #')
    for new_username, new_password, role in new_users:  
        result = login_with_credentials(ssh_device, new_username, new_password, role)
        print(result)
        if result == True:
            okcount.append('Ok')
        else:
            okcount.append('Nok')
        time.sleep(2) 

    print(okcount)
    return okcount.count('Ok')

