
import pytest, sys, time, os, logging ,datetime
from netmiko import ConnectHandler

def create_user(device, username, password, role):
    device.enable()
    config_commands = [
        f"username {username} role {role} password encrypted {password}",
    ]
    output = device.send_config_set(config_commands)
    if "%" in output:
        return False 
    print(output)

def delete_user(device, username):
    device.enable()
    config_commands = [
        f"no username {username}",
    ]
    output = device.send_config_set(config_commands)
    if "%" in output:
        return False 
    print(output)

def login_with_credentials(device, username, password):
    try:
        temp_device = device.copy()
        temp_device['username'] = username
        temp_device['password'] = password        
        net_connect = ConnectHandler(**temp_device)  
        command1 = net_connect.send_command('show users')
        print(command1)                
        command2 = net_connect.send_command('show user-account')
        # print(command2) 
        print(f"Successful login - Username: {username}, Password: {password}")      
        net_connect.disconnect()
        return True
    except Exception as e:
        print(f"Failed login - Username: {username}, Password: {password}")
        print(e)
        return False


def useraccount(host):
    device_info = {
        'device_type': 'cisco_ios',
        'ip': host,
        'username': 'root',
        'password': 'admin',
        'port': 22,
    }
    new_users = [
        ('actus', 'actus1234', 'network-admin'),
        ('hfrn', 'hfrn1234', 'network-operator'),
        ('cisco', 'cisco1234', 'network-viewer')
    ]
    okcount = [] 
    for new_username, new_password, role in new_users:
        net_connect = ConnectHandler(**device_info)
        command = create_user(net_connect, new_username, new_password, role)
        if command == False:
            break
        time.sleep(2)

        net_connect.disconnect()
        time.sleep(2)

        result = login_with_credentials(device_info, new_username, new_password)
        print(result)
        if result == True:
            okcount.append('Ok')
        else:
            okcount.append('Nok')
        time.sleep(2) 

        net_connect = ConnectHandler(**device_info)
        command = delete_user(net_connect, new_username)
        if command == False:
            break
        time.sleep(2) 

        net_connect.disconnect()
        time.sleep(2)

        result = login_with_credentials(device_info, new_username, new_password)      
        print(result)
        if result == False:
            okcount.append('Ok')
        else:
            okcount.append('Nok')
        time.sleep(2) 

        net_connect.disconnect()
        time.sleep(2) 

    print(okcount)
    return okcount.count('Ok')



