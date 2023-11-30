# funBaConf.py

# $language = "python"
# $interface = "1.0"

from logging import root
import time, paramiko
import basic.basicConf as bc


def disTitle(child,Title):
    child.sendline('\n') 
    child.sendline(Title )
    child.sendline('\n')

################################################################################### 
        
def check_mng_gw(child,state):
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

def check_mng_process(child,state):        
    successExpect = ['disable','20','disable','60','reboot','alive','normal']
    failureExpect = ['enable','2','enable','5','restart','dead','fail']
    result = []  
    command = child.send_command('show mng process') 
    cmd_split = (command.splitlines())
    command_list = [line for line in cmd_split if line.strip()]             
    result.append(command_list[2].split()[2]) 
    result.append(command_list[3].split()[2])
    result.extend(command_list[6].split()[1:4])  
    result.extend(command_list[19].split()[2:4])        
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
        
def check_mng_memory(child,state):
    successExpect = ['disable','60','10','5','80 %','60','normal','normal']
    failureExpect = ['enable','11','10','1','20 %','10','normal','normal']
    result = []  
    command = child.send_command('show mng memory') 
    cmd_split = (command.splitlines())
    command_list = [line for line in cmd_split if line.strip()] 
    # print(command_list)            
    result.append(command_list[2].split(':')[1].strip()) 
    result.append(command_list[3].split(':')[1].strip()) 
    result.append(command_list[4].split(':')[1].strip())  
    result.append(command_list[5].split(':')[1].strip()) 
    result.append(command_list[6].split(':')[1].strip())   
    result.append(command_list[7].split(':')[1].strip())   
    result.append(command_list[13].split(':')[1].strip())   
    result.append(command_list[15].split(':')[1].strip())        
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

def check_mng_evm_conf(child,state):
    successExpect = ['Disable','Disable','30','5','Normal','0']
    failureExpect = ['Enable','enable','10','1','Lockout','1']
    result = []  
    command = child.send_command('show mng evm') 
    cmd_split = (command.splitlines())
    command_list = [line for line in cmd_split if line.strip()] 
    # print(command_list)            
    result.append(command_list[2].split(':')[1].strip()) 
    result.append(command_list[3].split(':')[1].strip()) 
    result.append(command_list[4].split(':')[1].strip())  
    result.append(command_list[5].split(':')[1].strip()) 
    result.append(command_list[10].split(':')[1].strip())   
    result.append(command_list[11].split(':')[1].strip())          
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
                
def check_mng_evm(child,state):
    command = child.send_command('show mng evm') 
    cmd_split = (command.splitlines())
    command_list = [line for line in cmd_split if line.strip()]                        
    print(len(command_list))
    if len(command_list) >= 15:
        if state == 'gw':
            process = command_list[15].split(':')[1].strip()  
            action = command_list[16].split(':')[1].strip()     
            print(f'Reserved Actions: {process} & {action}')        
            if 'gate mon' == process and 'reboot' == action:
                return True
            else:
                return False
        elif state == 'process':
            process = command_list[15].split(':')[1].strip() 
            action = command_list[16].split(':')[1].strip()    
            print(f'Reserved Actions: {process} & {action}')        
            if 'mstpd' == process and 'restart' == action:
                return True
            else:
                return False
        elif state == 'memory':
            process = command_list[15].split(':')[1].strip() 
            action = command_list[16].split(':')[1].strip()    
            print(f'Reserved Actions: {process} & {action}')        
            if 'memory mon' == process and 'reboot' == action:
                return True
            else:
                return False
        elif state == 'watchdog':
            result1 = command_list[10].split(':')[1].strip()   
            result2 = command_list[11].split(':')[1].strip()     
            print(result1,result2)        
            if 'Normal' == result1 and '1' == result2:
                return True
            else:
                return False
    else:
        return False

##################################################################################
   
def mngGwConf(dut1):
    result = []
    with bc.connect(dut1) as child:
        gw_success_config = [
            'mng configuration',
            'ping monitor type gw 192.168.0.2', 
            'ping monitor type interval 10', 
            'ping monitor type threshold 1', 
            'enable ping monitor'
            ]
        child.send_config_set(gw_success_config)
        time.sleep(10)
        result.append(check_mng_gw(child,'normal'))

        gw_failure_config = [
            'mng configuration',
            'ping monitor type gw 10.1.1.1', 
            'ping monitor type interval 11', 
            'ping monitor type threshold 2', 
            'enable ping monitor'
            ]
        child.send_config_set(gw_failure_config)
        time.sleep(30)
        result.append(check_mng_gw(child,'failure'))
        time.sleep(1)        
        result.append(check_mng_evm(child,'gw'))
        print(result)

        if result.count(True) == 3 :
            return True
        else:
            return False

def mngProcessConf(dut1):    
    result = []
    with bc.connect(dut1) as child:
        proc_enable_config = [
            'mng configuration',
            'process monitor type process all enable ',
            'process monitor type process all action restart',
            'process monitor type process all threshold 5 ',
            'process monitor type interval 2',
            'enable process monitor '
            ]
        result.append(check_mng_process(child,'normal'))
        time.sleep(1)
        child.send_config_set(proc_enable_config)  
        time.sleep(5)
        killall_process(dut1)
        time.sleep(5) 

    with bc.connect(dut1) as child:   # To avoid the console prompt hanging,       
        time.sleep(1)
        result.append(check_mng_process(child,'failure'))
        time.sleep(12)               
        result.append(check_mng_evm(child,'process'))
        time.sleep(1)
        remove_plog(dut1)
        print(result)
        if result.count(True) == 3 :
            return True
        else:
            return False

def mngMemoryConf(dut1):
    result = []
    with bc.connect(dut1) as child:
        mem_enable_config = [
            'mng configuration',
            'memory monitor type count 1 ',
            'memory monitor type duration 10',
            'memory monitor type interval 10',
            'memory monitor type period 11 ',
            'memory monitor type usage 20',
            'enable memory monitor'
            ]
        result.append(check_mng_memory(child,'normal'))
        time.sleep(1)
        child.send_config_set(mem_enable_config)  
        time.sleep(1)      
        result.append(check_mng_memory(child,'failure'))
        time.sleep(1)              
        print(result)
        if result.count(True) == 2 :
            return True
        else:
            return False

# def mngEvmConf(dut1):
#     result = []
#     with bc.connect(dut1) as child:
#         evm_enable_config = [
#             'mng configuration',
#             'evm tcpdump 100',
#             'evm lockout count 1',
#             'evm lockout interval 10 ',
#             'enable evm watchdog',
#             'enable evm lockout',
#             ]
#         mem_enable_config = [
#             'mng configuration',
#             'memory monitor type count 1 ',
#             'memory monitor type duration 10',
#             'memory monitor type interval 10',
#             'memory monitor type period 11 ',
#             'memory monitor type usage 20',
#             'enable memory monitor'
#             ]
#         result.append(check_mng_evm_conf(child,'normal'))
#         time.sleep(1)
#         child.send_config_set(evm_enable_config)  
#         time.sleep(1)
#         child.send_config_set(mem_enable_config)
#         child.send_command('write memory')
#         generate_mrmory_overload(dut1)                
#         time.sleep(300) 

def mngEvmConf(dut1):
    result = []
    with bc.connect(dut1) as child:
        evm_enable_config = [
            'mng configuration',
            'evm tcpdump 100',
            'evm lockout count 1',
            'evm lockout interval 10 ',
            'enable evm watchdog',
            'enable evm lockout',
            ]
        gw_failure_config = [
            'mng configuration',
            'ping monitor type gw 10.1.1.1', 
            'ping monitor type interval 11', 
            'ping monitor type threshold 2', 
            'enable ping monitor'
            ]
        result.append(check_mng_evm_conf(child,'normal'))
        time.sleep(1)
        child.send_config_set(evm_enable_config)  
        time.sleep(1)
        child.send_config_set(gw_failure_config)
        child.send_command('write memory')            
        time.sleep(180) 

    with bc.connect(dut1) as child:                
        result.append(check_mng_evm_conf(child,'failure'))
        time.sleep(1)               
    if result.count(True) == 2 :
        return True
    else:
        return False

def enable_evm(host):
    with bc.connect(host) as child:
        config_commands =['mng configuration','enable evm watchdog','enable evm lockout']
        child.send_config_set(config_commands )
        time.sleep(1)

def disable_evm(host):
    with bc.connect(host) as child:
        config_commands =['mng configuration','disable evm watchdog','disable evm lockout']
        child.send_config_set(config_commands )
        time.sleep(1)

def default_mng_gw_config(dut1):
    with bc.connect(dut1) as child:
        default_config_commands = [
            'mng configuration',
            'no ping monitor type gw',
            'no ping monitor type interval', 
            'no ping monitor type threshold', 
            'disable ping monitor'
            ]
        child.send_config_set(default_config_commands)
        time.sleep(1)

def default_mng_process_config(dut1):
    with bc.connect(dut1) as child:
        default_config_commands = [
            'mng configuration',
            'process monitor type process all action reboot',             
            'no process monitor type process all',
            'no process monitor type process all threshold', 
            'no process monitor type interval',
            'disable process monitor'
            ]
        child.send_config_set(default_config_commands)
        time.sleep(1)

        reinit_mstpd = [
            'spanning mode mstp',
            'spanning mode disable',             
            ]
        child.send_config_set(reinit_mstpd)
        time.sleep(1)
        
def default_mng_mem_config(dut1):
    with bc.connect(dut1) as child:
        default_config_commands = [
            'mng configuration',
            'no memory monitor type duration',
            'memory monitor type period 60',
            'no memory monitor type interval',
            'no memory monitor type usage',
            'memory monitor type count 5',
            'disable memory monitor '
            ]
        child.send_config_set(default_config_commands)
        time.sleep(1)

def default_mng_evm_config(dut1):
    with bc.connect(dut1) as child:
        default_config_commands = [
            'mng configuration',
            'no evm tcpdump',
            'no evm lockout count',
            'no evm lockout interval ',
            'disable evm watchdog ',
            'disable evm lockout '
            ]
        child.send_config_set(default_config_commands)
        child.send_command('write memory')
        time.sleep(1)

# def killall_process(host):
#     with bc.connect(host) as child:
#         child.send_command('debug no-auth')
#         child.send_command('system-shell', expect_string='sh-4.3#')
#         child.send_command('killall mstpd', expect_string='sh-4.3#')
#         child.send_command('exit', expect_string='logout')
#         time.sleep(1)

def killall_process(host):
    with bc.connect(host) as child:  
        child.send_command('debug no-auth') 
        shell = child.send_command_timing('system-shell')
        shell += child.send_command_timing('killall mstpd')
        time.sleep(2)
        shell += child.send_command_timing('killall imish') # To avoid the console prompt hanging, 

def generate_mrmory_overload(host):
    with bc.connect(host) as child:  
        child.send_command('debug no-auth') 
        shell = child.send_command_timing('system-shell')
        shell += child.send_command_timing('cat /dev/zero | head -c 1000m | tail')
        time.sleep(10)             

def remove_plog(host):
    with bc.connect(host) as child:
        show_plog = child.send_command('show process plog')
        plogs = show_plog.splitlines()
        plog = show_plog.splitlines()[0].split(':')[0]  
        print(plog)
        if plog == 'ls':
            pass
        else:
            for i in plogs:
                child.send_command('remove file log ' + i)
        