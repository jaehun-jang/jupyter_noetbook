# funBaConf.py

# $language = "python"
# $interface = "1.0"
import pytest, sys, time, os, logging ,datetime
from logging import root
import time, paramiko
import basic.basicConf as bc


def disTitle(child,Title):
    child.sendline('\n') 
    child.sendline(Title )
    child.sendline('\n')

################################################################################### 

def stpModeCheck(dut):
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree')
        # print(command_output)
        lines = command_output.splitlines()
        for line in lines:
            columns = line.split()           
            # Check spanning-tree Mode
            if columns and columns[0] == 'spanning-tree': 
                xstp = columns[3] 
                print(f"## The Spanning mode is {xstp} ##") 
 
def stpPortStateCheck(child,interface):
    # To reduce process time, this method uses child processes.
    command_output = child.send_command('show spanning-tree')
    lines = command_output.splitlines()
    for line in lines:
        columns = line.split()           
        if columns and columns[0] == interface: 
            state = columns[2] 
            print(f"The Spanning port state is {state}")
            return state

def get_stp_addrAndPri(dut):
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree')
        lines = command_output.splitlines()

        root_address = None
        bridge_address = None
        reading_root = False
        reading_bridge = False

        for line in lines:
            columns = line.split()
            if not columns:
                continue

            if columns[0] == 'ROOT':
                reading_root = True
                reading_bridge = False
                rootPri = columns[3] 
            elif columns[0] == 'BRIDGE':
                reading_bridge = True
                reading_root = False
                bridgePri = columns[3] 
            if reading_root and columns[0] == 'address':
                root_address = columns[1]
            elif reading_bridge and columns[0] == 'address':
                bridge_address = columns[1]
                
        print('root_address: ', root_address, 'bridge_address: ', bridge_address)
        print('root_pri: ', rootPri, 'bridge_Pri: ', bridgePri)
        return root_address, bridge_address, rootPri, bridgePri

def get_stp_timer(dut,bridge):
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree')
        lines = command_output.splitlines()

        root_timer = None
        bridge_timer = None
        reading_root = False
        reading_bridge = False

        for line in lines:
            columns = line.split()
            if not columns:
                continue

            if columns[0] == 'ROOT':
                reading_root = True
                reading_bridge = False
            elif columns[0] == 'BRIDGE':
                reading_bridge = True
                reading_root = False
            if reading_root and columns[0] == 'Hello':
                root_timer = [columns[2], columns[5], columns[8]]
            elif reading_bridge and columns[0] == 'Hello':
                bridge_timer = [columns[2], columns[5], columns[8]]        

        if bridge == 'root':
            print(f'Root Bridge Hello_Time: {root_timer[0]}, Max_age: {root_timer[1]}, Forward_Delay: {root_timer[2]}')
            return root_timer
        elif bridge == 'bridge':
            print(f'Bridge Hello_Time: {bridge_timer[0]}, Max_age: {bridge_timer[1]}, Forward_Delay: {bridge_timer[2]}')
            return bridge_timer
        
def get_stp_cli_result(dut,string,cloum):
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree')
        lines = command_output.splitlines()
        # print(command_output)
        for line in lines:
            columns = line.split()         
            # Check spanning-tree Mode
            if columns and columns[0] == string : 
                result = columns[cloum] 
                print(f"The result of reding spanning CLI is {result} ")
                return result 
            
def get_stp_cli_Multi_colum(dut,string,column,column2):
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree')
        lines = command_output.splitlines()
        # print(command_output)
        for line in lines:
            columns = line.split()         
            # Check spanning-tree Mode
            if columns and columns[0] == string : 
                if column2 == 6 and len(columns) != 7:
                    result.append('Non')
                else:
                    result = columns[column],columns[column2] 
                print(f"The result of reding spanning CLI is {result} ")
                return result 
       
def get_cli_result(dut,command,string,cloum):
    with bc.connect(dut) as child:
        command_output = child.send_command(command)
        lines = command_output.splitlines()
        print(command_output)
        for line in lines:
            columns = line.split()        
            # Check spanning-tree Mode
            if columns and columns[0] == string : 
                result = columns[cloum] 
                print(f'The result of reding spanning CLI is "{result}" ')
                return result


def get_mst_multi_root(dut):
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree mst')
        lines = command_output.splitlines()
        print(command_output)

        root = []
        reading_mst0 = False
        reading_mst1 = False
        reading_mst2 = False

        for line in lines:
            columns = line.split()
            if not columns:
                continue

            if columns[1] == 'MST0':
                reading_mst0 = True
                reading_mst1 = False
                reading_mst2 = False
            elif columns[1] == 'MST1':
                reading_mst0 = False
                reading_mst1 = True
                reading_mst2 = False
            elif columns[1] == 'MST2':
                reading_mst0 = False
                reading_mst1 = False
                reading_mst2 = True
                
            if reading_mst0 and columns[0] == 'Root':
                print(columns)
                root.append(columns[5])
            elif reading_mst1 and columns[0] == 'Root':
                print(columns)
                root.append(columns[4])   
            elif reading_mst2 and columns[0] == 'Root':
                print(columns)
                root.append(columns[4])        

        return root

def get_mst_pri_of_instance(dut,dutIndex):
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree mst')
        lines = command_output.splitlines()
        print(command_output)

        root = ''
        reading_mst0 = False
        reading_mst1 = False
        reading_mst2 = False

        for line in lines:
            columns = line.split()
            if not columns:
                continue

            if columns[1] == 'MST0':
                reading_mst0 = True
                reading_mst1 = False
                reading_mst2 = False
            elif columns[1] == 'MST1':
                reading_mst0 = False
                reading_mst1 = True
                reading_mst2 = False
            elif columns[1] == 'MST2':
                reading_mst0 = False
                reading_mst1 = False
                reading_mst2 = True
                
            if dutIndex == 0 and reading_mst0 and columns[0] == 'Root':
                print(columns)
                root = columns[5]
            elif dutIndex == 1 and reading_mst1 and columns[0] == 'Root':
                print(columns)
                root = columns[4]   
            elif dutIndex == 2 and reading_mst2 and columns[0] == 'Root':
                print(columns)
                root = columns[4]        

        return root
    
def get_mst_interface_cost(dut):
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree mst')
        lines = command_output.splitlines()
        print(command_output)

        result = []
        reading_mst0 = False
        reading_mst1 = False
        reading_mst2 = False

        for line in lines:
            columns = line.split()
            if not columns:
                continue

            if columns[1] == 'MST0':
                reading_mst0 = True
                reading_mst1 = False
                reading_mst2 = False
            elif columns[1] == 'MST1':
                reading_mst0 = False
                reading_mst1 = True
                reading_mst2 = False
            elif columns[1] == 'MST2':
                reading_mst0 = False
                reading_mst1 = False
                reading_mst2 = True
                
            if reading_mst0 and columns[0] == '1/16':
                print(columns)
                mst0 = [columns[1],columns[3]]
                result.extend(mst0)
                
            elif reading_mst1 and columns[0] == '1/16':
                print(columns)               
                mst1 = [columns[1],columns[3]] 
                result.extend(mst1)  
                
            elif reading_mst2 and columns[0] == '1/16':
                print(columns)
                mst2 = [columns[1],columns[3]]   
                result.extend(mst2)      

        return result

def get_mst_instancee_cloumns(dut,string,column):
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree mst')
        lines = command_output.splitlines()
        print(command_output)

        result = []
        reading_mst0 = False
        reading_mst1 = False
        reading_mst2 = False

        for line in lines:
            columns = line.split()
            if not columns:
                continue

            if columns[1] == 'MST0':
                reading_mst0 = True
                reading_mst1 = False
                reading_mst2 = False
            elif columns[1] == 'MST1':
                reading_mst0 = False
                reading_mst1 = True
                reading_mst2 = False
            elif columns[1] == 'MST2':
                reading_mst0 = False
                reading_mst1 = False
                reading_mst2 = True
                
            if reading_mst0 and columns[0] == string:
                if column == 6 and len(columns) != 7:
                    result.append('Non')
                else:
                    mst0 = columns[column]
                    result.append(mst0)
                
            elif reading_mst1 and columns[0] == string:
                if column == 6 and len(columns) != 7:
                    result.append('Non')
                else:               
                    mst1 = columns[column]
                    result.append(mst1)  
                
            elif reading_mst2 and columns[0] == string:
                if column == 6 and len(columns) != 7:
                    result.append('Non')
                else: 
                    mst2 = columns[column]  
                    result.append(mst2)      

        return result

def get_mst_instancee_multi_cloumns(dut,string,column1,column2):
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree mst')
        lines = command_output.splitlines()
        print(command_output)

        result = []
        reading_mst0 = False
        reading_mst1 = False
        reading_mst2 = False

        for line in lines:
            columns = line.split()
            if not columns:
                continue

            if columns[1] == 'MST0':
                reading_mst0 = True
                reading_mst1 = False
                reading_mst2 = False
            elif columns[1] == 'MST1':
                reading_mst0 = False
                reading_mst1 = True
                reading_mst2 = False
            elif columns[1] == 'MST2':
                reading_mst0 = False
                reading_mst1 = False
                reading_mst2 = True
                
            if reading_mst0 and columns[0] == string:
                if column2 == 6 and len(columns) != 7:
                    result.append('Non')
                else:
                    mst0 = [columns[column1],columns[column2]]
                    result.append(mst0)
                
            elif reading_mst1 and columns[0] == string:
                if column2 == 6 and len(columns) != 7:
                    result.append('Non')
                else:               
                    mst1 = [columns[column1],columns[column2]]
                    result.append(mst1)  
                
            elif reading_mst2 and columns[0] == string:
                if column2 == 6 and len(columns) != 7:
                    result.append('Non')
                else: 
                    mst2 = [columns[column1],columns[column2]]
                    result.append(mst2)      

        return result

        
###########################################################################################         

##### check_stp_[PORT ROLE] #####                                                               
def check_stp_PortRole(dut,mode):
    # Define the list of interfaces you want to check
    intList = ['1/11', '1/12', '1/13', '1/15', '1/16']  

    # Define the expected result as a dictionary
    expectResult = {
        '1/11': 'Desg',
        '1/12': 'Bakp',
        '1/13': 'Desg',
        '1/15': 'Root',
        '1/16': 'Altn',
    }

    # Initialize the portRoles dictionary with default values
    readResult = {
        '1/11': 'Unknown',
        '1/12': 'Unknown',
        '1/13': 'Unknown',
        '1/15': 'Unknown',
        '1/16': 'Unknown',
    }
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree')
        lines = command_output.splitlines()

        for line in lines:
            columns = line.split()
            
            # Check if the line starts with the spanning-tree 
            if columns and columns[0] == 'spanning-tree': 
                xstp = columns[3] 
                print(f"The Spanning mode is {xstp}")   
                                                   
        for interface in intList:
            for index, line in enumerate(lines):
                columns = line.split()

                # Check if the line starts with the interface name
                if columns and columns[0] == interface:
                    # print(f"The index, including the interface {interface}, is {index}.")              
                    # Store the readResult in the dictionary
                    readResult[interface] = columns[1]
                
    # Print the port roles for the specified interfaces
    # for interface, role in readResult.items():
    #     print(f"Interface {interface}: Port Role is {role}")

    print("Read Roles:", readResult)
    print("Expected Result:", expectResult)
    
    # Compare readResult with expectResult
    if readResult == expectResult and xstp == mode:
        return True
    else:
        return False

##### check_stp_[PORT STATE] #####                                                   
def check_stp_PortState(dut,mode):
    normalport = '1/10'
    blockport = '1/12'
       
    with bc.connect(dut) as child:
        stp_mode_config =[
        f'spanning mode {mode}'       
        ]
        child.send_config_set(stp_mode_config)     
                         
        if mode == 'stp': 
            expectResult = ['LSN','LRN','FWD','BLK']
            readResult = []
            # Check the STP state of the interface.
            readResult.append(stpPortStateCheck(child,normalport))
            time.sleep(15) 
            readResult.append(stpPortStateCheck(child,normalport))
            time.sleep(15)            
            readResult.append(stpPortStateCheck(child,normalport))
            time.sleep(2)            
            readResult.append(stpPortStateCheck(child,blockport)) 
            
            print("Read Roles:", readResult) 
             
            stpModeCheck(dut) 
            time.sleep(2)  
                            
            # Compare readResult with expectResult
            if readResult == expectResult:
                return True
            else:
                return False  

        else: 
            expectResult = ['DSC','LRN','FWD','DSC']
            readResult = []
            # Check the STP state of the interface.
            readResult.append(stpPortStateCheck(child,normalport))
            time.sleep(2.5)  
            readResult.append(stpPortStateCheck(child,normalport))
            time.sleep(2)           
            readResult.append(stpPortStateCheck(child,normalport))
            time.sleep(1)             
            readResult.append(stpPortStateCheck(child,blockport))  
                        
            print("Read Roles:", readResult)  
            # Compare readResult with expectResult
            
            stpModeCheck(dut) 
            time.sleep(2)  
            
            if readResult == expectResult:
                return True
            else:
                return False    

##### check_stp_[ROOT BRIDGE ELECTION] #####
def check_stp_RouteBridge(dut,mode):     
    result =[] 
    syspri = 4096
    bridge = 32768 

    stpModeCheck(dut) 
    time.sleep(2)
                
    # Check the bridge which has higher MAC address is elected as root bridge.
    root_address, bridge_address, root_pri, bridge_pri = get_stp_addrAndPri(dut)
    if root_address ==  bridge_address:
        result.append('True')
    else:
        result.append('False') 

    # Configure STP system priority                    
    stpSystemPri(dut,mode,syspri)
    time.sleep(3) 
    
    root_address, bridge_address, root_pri, bridge_pri = get_stp_addrAndPri(dut)
    
    if root_address == bridge_address and (root_pri == '4096' or root_pri == '4097'):
        result.append('True')
    else:
        result.append('False') 
                        
    # Configure STP system priority   
    stpSystemPri(dut,mode,bridge)
    time.sleep(3) 
                                    
    print(result)
    if result == ['False', 'True']:
        return True
    else:
        return False

##### check_stp_[PATH-COST] #####
def check_stp_system_config(dut):     
    result =[]
    cloum = 0
    string = 'Cost'
    
    stpModeCheck(dut) 
    time.sleep(2)
                    
    cloum = 1  # cost value of the interface            
    Costvalue = get_stp_cli_result(dut,string,cloum)
    # Costvalue = get_stp_cli_result(dut,string,cloum)
    print(Costvalue)  
    time.sleep(2)  
        
    if Costvalue == '2000':
    # if Portrole ==  'Altn' and Costvalue == '2000':
        result.append('True')
    else:
        result.append('False') 
    
    # Configure STP Path-Cost as Shot                    
    stpPathCost(dut,'short')
    time.sleep(3) 
      
    cloum = 1  # cost value of the interface            
    Costvalue = get_stp_cli_result(dut,string,cloum)
    # Costvalue = get_stp_cli_result(dut,string,cloum)
    print(Costvalue)  
    time.sleep(2)  
    
    if Costvalue == '2':
    # if Portrole ==  'Desg' and Costvalue == '2':
        result.append('True')
    else:
        result.append('False') 

    # Configure STP Path-Cost as Shot                    
    stpPathCost(dut,'long')
    time.sleep(5) 
        
    print(result)                                            
    if result == ['True','True']:
        return True
    else:
        return False

##### check_stp_[TIMER] ##### 
def check_stp_timer_config(devs): 
        
    stpModeCheck(devs[0]) 
    time.sleep(2)
    
    with bc.connect(devs[0]) as child:  # Connect to DUT1                      
        # Configure STP Path-Cost as Shot  
        hello = 4
        forwardDelaty = 30
        maxage = 40                  
        stpTimerConf(devs[0],hello,forwardDelaty,maxage)
        time.sleep(5) 

        #Check the bridge which has higher MAC address is elected as root bridge.        
        bridge = 'bridge'  # Get Port role of the interface      
        rootTimer = get_stp_timer(devs[0],bridge)
        # Costvalue = get_stp_cli_result(dut,string,cloum)
        print(rootTimer)     
        time.sleep(5)
                
    with bc.connect(devs[1]) as child:  # Connect to DUT1               
        # Check the bridge which has higher MAC address is elected as root bridge.        
        bridge = 'root'  # Get Port role of the interface      
        bridgeTimer = get_stp_timer(devs[1],bridge)
        # Costvalue = get_stp_cli_result(dut,string,cloum)
        print(bridgeTimer)     
        time.sleep(5)

    with bc.connect(devs[0]) as child:  # Connect to DUT1                      
        # Configure STP Path-Cost as Shot  
        hello = 2
        forwardDelaty = 15
        maxage = 20                    
        stpTimerConf(devs[0],hello,forwardDelaty,maxage)
        time.sleep(5) 
                                                  
    if rootTimer == bridgeTimer:
        return True
    else:
        return False

##### check_stp_[RootGuard] #####
def check_stp_RootGuard(devs,mode):
    result = []  
    command =['interface 1/14','shutdown'] 
    bc.sendConfigSet(devs[0],command)  
    
    syspri = 8192        
    stpRootGuardConf(devs[0])
    time.sleep(1)    
    stpSystemPri(devs[0],mode,syspri) 
    time.sleep(1) 
            
    syspri = 4096    
    stpSystemPri(devs[1],mode,syspri) 
    
    # Check if the root bridge is protected..            
    with bc.connect(devs[0]) as child:  # Connect to DUT1               
        startString = '1/15'
        cloum = 6
        
    reString = get_stp_cli_result(devs[0],startString,cloum)
        
    root_address, bridge_address, root_pri, bridge_pri = get_stp_addrAndPri(devs[0])    
    
    if reString == 'Root-Inc' and root_address == bridge_address:
        result.append('True')
    else:
        result.append('False')

    # Check if the root bridge is changed.      
    noStpRootGuardConf(devs[0]) # Disable Root Guard in the interface
    time.sleep(10) 

    root_address, bridge_address, root_pri, bridge_pri = get_stp_addrAndPri(devs[0])  
    
    if  root_address != bridge_address:
        result.append('True')
    else:
        result.append('False')

    syspri = 32768    
    stpSystemPri(devs[1],mode,syspri) 
    
    command =['interface 1/14','no shutdown'] 
    bc.sendConfigSet(devs[0],command)
                                                                    
    if  result.count('True') == 2:
        return True
    else:
        False

##### check_stp_BpduGuard #####
def check_stp_BpduGuard(devs):
    result = []

    stpModeCheck(devs[2]) 
    time.sleep(2)
                                      
    stpBpduGuardConf(devs[2])
    time.sleep(2)    
    errdisBpduGuar(devs[2])
    time.sleep(5) 
        
    # Check if the bpduguard is detected..                         
    command = 'sh errdisable recovery'
    startString = 'bpduguard(1/16)'
    cloum = 0        
    reString = get_cli_result(devs[2],command,startString,cloum)
    
    time.sleep(2) 
    noStpBpduGuardConf(devs[2])
    time.sleep(2) 
        
    if reString == 'bpduguard(1/16)':
        return True
    else:
        return False


##### check_stp_BpduFilter #####
def check_stp_BpduFilter(dut,mode):
    result = []

    stpModeCheck(dut) 
    time.sleep(1)
                                      
    # Check if the bpduguard is detected..                         
    command = 'sh spanning-tree'
    startString = '1/16'
    cloum = 1        
    reString = get_cli_result(dut,command,startString,cloum)
    
    if reString == 'Root':
        result.append('True')
    else:
        result.append('False')
        
    # Config BPDU filter on the interface. #         
    stpBpduFilterConf(dut)
    # stpBpduFilterConf(dut)
    time.sleep(1)    
        
    # Wait until the MAX-Age time has elapsed. # 
    if mode == 'stp':
        time.sleep(25) 
    else:
        time.sleep(7)       

    reString = get_cli_result(dut,command,startString,cloum)
    
    if reString == 'Desg':
        result.append('True')
    else:
        result.append('False')

    noStpBpduFilterConf(dut)
    time.sleep(2) 
        
    time.sleep(2) 

    print(result)            
    if  result.count('True') == 2:
        return True
    else:
        False
       
##### check_stp_EdgePort #####
def check_stp_EdgePort(devs,mode):
    result = []

    stpModeCheck(devs[1]) 
    time.sleep(2)
                                              
    # Check if the edgeport is configured.                         
    command = 'sh spanning-tree'
    startString = '1/13'
    cloum = 5   

    stpEdgePortConf(devs[1],startString)
    time.sleep(3)         
         
    reString = get_cli_result(devs[1],command,startString,cloum)

    print('reString :', reString)    
    
    if reString == 'Edge':
        result.append('True')
    else:
        result.append('False')
    
    # Enable STP on dut#3 
    stpModeConf([devs[2]],mode)
    
    if mode == 'stp':
        time.sleep(15) # To ensure forward delay (DIS -> LSN)
    else:
        time.sleep(3) # To ensure forward delay (DIS -> LSN) 
               
    stpModeCheck(devs[2]) 
    time.sleep(2)
            
    # Check if the edgeport is released.
    reString = get_cli_result(devs[1],command,startString,cloum)

    print('reString :', reString) 
    
    if reString == 'point-to-point':
        result.append('True')
    else: # If DUT don't resceive  
        bc.sendConfigSet(devs[1],["int 1/13", "shutdown"])
        time.sleep(2) 
        bc.sendConfigSet(devs[1],["int 1/13", "no shutdown"]) 
        time.sleep(2) 
        reString = get_cli_result(devs[1],command,startString,cloum) 
        time.sleep(3) 
        if reString == 'point-to-point':
            result.append('True')
        else:             
            result.append('False') 
                   
    time.sleep(5) 
   
    noStpEdgePortConf(devs[1],startString)     

    # Disable STP on dut#3 
    stpModeConf([devs[2]],'disable')
    
    print(result)            
    if  result.count('True') == 2:
        return True
    else:
        False
       
##### check_stp_Port_Priority #####
def check_stp_PortPri(devs):
    result = []

    stpModeCheck(devs[1]) 
    time.sleep(2)
                                              
    # Check if the edgeport is configured.                         
    command = 'sh spanning-tree'
    startString = '1/16'
    cloum = 1   

    # Set a higher port priority on int 1/16 than int 1/15 on the root switch.
    stpPortPridConf(devs[0],startString)
    time.sleep(5)         
         
    reString = get_cli_result(devs[1],command,startString,cloum)

    print('reString :', reString)    
    
    if reString == 'Root':
        result.append('True')
    else:
        result.append('False')

    time.sleep(5)      

    # Set a default port priority on int 1/16 on the root switch
    noStpPortPridConf(devs[0],startString)
    time.sleep(5)         
         
    reString = get_cli_result(devs[1],command,startString,cloum)

    print('reString :', reString)    
    
    if reString == 'Altn':
        result.append('True')
    else:
        result.append('False')
    
    print(result)            
    if  result.count('True') == 2:
        return True
    else:
        False

       
##### check_stp_Port_Cost #####
def check_stp_PortCost(devs):
    result = []

    stpModeCheck(devs[1]) 
    time.sleep(2)
                                              
    # Check if the edgeport is configured.                         
    command = 'sh spanning-tree'
    startString = '1/16'
    cloum = 1   

    # Set a higher port priority on int 1/16 than int 1/15 on the root switch.
    stpPortCostConf(devs[1],startString)
    time.sleep(5)         
         
    reString = get_cli_result(devs[1],command,startString,cloum)

    print('reString :', reString)    
    
    if reString == 'Root':
        result.append('True')
    else:
        result.append('False')

    time.sleep(5)      

    # Set a default port priority on int 1/16 on the root switch
    noStpPortCostConf(devs[1],startString)
    time.sleep(5)         
         
    reString = get_cli_result(devs[1],command,startString,cloum)

    print('reString :', reString)    
    
    if reString == 'Altn':
        result.append('True')
    else:
        result.append('False')
    
    print(result)            
    if  result.count('True') == 2:
        return True
    else:
        False
               

##### check_MSTP_INstance #####
def check_mstp_MultiInstance(devs):
                                                            
    # for i in dutIndex:  # Assuming you want to iterate from 0 to 2                                    
    reString = get_mst_multi_root(devs[0])
    print('reString :', reString)
             
    print(reString)            
    if  reString == ['CIST','MST1','MST2']:
        return True
    else:
        False
        
##### check_MSTP_INstance_Priority #####
def check_mstp_priority_of_instance(devs):
    result = []
    dutIndex = [0,1,2]   
        
    # To configure priority of each MST instance. 
    for i in range(3):  # Assuming you want to iterate from 0 to 2
        command = [f'spanning-tree mst {i} priority 4096']
        bc.sendConfigSet(devs[i], command)
                                                            
    # Check if the edgeport is configured. 
    for i in dutIndex:  # Assuming you want to iterate from 0 to 2                                    
        reString = get_mst_pri_of_instance(devs[i],i)
        print('reString :', reString)
        result.append(reString)
        time.sleep(5)   
    
    # To remove priority of each MST instance. 
    for i in range(3):  # Assuming you want to iterate from 0 to 2
        command3 = [f'no spanning-tree mst {i} priority']
        bc.sendConfigSet(devs[i], command3)
                     
    print(result)            
    if  result == ['CIST','MST1','MST2']:
        return True
    else:
        False 
          

##### check_MSTP_cost_of_iNterface__INstance #####
def check_mstp_interface_cost(devs):
       
    # To configure priority of each MST instance. 
    command = [
        'interface 1/16',
        'spanning-tree mst 1 cost 1600',
        'spanning-tree mst 2 cost 1800'
        ]
    bc.sendConfigSet(devs[1], command)
                                                            
    # for i in dutIndex:  # Assuming you want to iterate from 0 to 2                                    
    reString = get_mst_interface_cost(devs[1])
    print('reString :', reString)
    
    # To remove priority of each MST instance. 
    command = [
        'interface 1/16',
        'no spanning-tree mst 1 cost',
        'no spanning-tree mst 2 cost'
        ]
    bc.sendConfigSet(devs[1], command)
         
    print(reString)            
    if  reString == ['Altn','2000','Root','1600','Root','1800']:
    # if  reString == [['Altn','2000'],['Root','1600'],['Root','1800']]:
        return True
    else:
        False
 
 
 ##### check_MSTP_cost_of_interface__instance #####
def check_mstp_interface_pri(devs):    
    result =[]
    
    # To configure priority of each MST instance. 
    command = [
        'interface 1/16',
        'spanning-tree mst 1 port-priority 64',
        'spanning-tree mst 2 port-priority 96'
        ]
    bc.sendConfigSet(devs[0], command)
                                                            
    # check priority of root bridge
    string = '1/16' 
    column =   4                               
    reString = get_mst_instancee_cloumns(devs[0],string,column)
    result.extend(reString)
    print('reString :', reString)
    time.sleep(3)

    # check port role of per bridge       
    string = '1/16' 
    column =   1 
    reString = get_mst_instancee_cloumns(devs[1],string,column)
    result.extend(reString)
    print('reString :', reString)
    
    # To remove priority of each MST instance. 
    command = [
        'interface 1/16',
        'no spanning-tree mst 1 port-priority',
        'no spanning-tree mst 2 port-priority'
        ]
    bc.sendConfigSet(devs[0], command)
         
    print(result)            
    if  result == ['128','64','96','Altn','Root','Root']:
    # if  reString == [['Altn','2000'],['Root','1600'],['Root','1800']]:
        return True
    else:
        False
 

 ##### check_MSTP_Regions(VLAN,NAME,REVISION) #####
def check_mstp_region_vlan(devs):  
    result =[]
       
    # To configure priority of each MST instance. 
    command = [
        'spanning-tree mst configuration',
        'instance 2 vlan 3-4'
        ]
    bc.sendConfigSet(devs[0], command)
                                                            
    # check priority of root bridge
    string = '1/16' 
    column =   6                              
    reString = get_mst_instancee_cloumns(devs[0],string,column)
    result.extend(reString)
    print('reString :', reString)
    time.sleep(3)
    
    # To remove priority of each MST instance. 
    command = [
        'spanning-tree mst configuration',
        'no instance 2',
        'instance 2 vlan 3'        
        ]
    bc.sendConfigSet(devs[0], command)

    # check priority of root bridge
    string = '1/16' 
    column =   6                              
    reString = get_mst_instancee_cloumns(devs[0],string,column)
    result.extend(reString)
    print('reString :', reString)
    time.sleep(3)
             
    print(result)            
    if  result == ['boundary','boundary','boundary','Non','Non','Non']:
        return True
    else:
        False     

 ##### check_MSTP_Regions(VLAN,NAME,REVISION) #####
def check_mstp_region_name(devs):   
    result =[]
        
    # To configure priority of each MST instance. 
    command = [
        'spanning-tree mst configuration',
        'name hfrn'
        ]
    bc.sendConfigSet(devs[0], command)
                                                           
    # check priority of root bridge
    string = '1/16' 
    column =   6                              
    reString = get_mst_instancee_cloumns(devs[0],string,column)
    result.extend(reString)
    print('reString :', reString)
    time.sleep(3)
    
    # To remove priority of each MST instance. 
    command = [
        'spanning-tree mst configuration',
        'no name',     
        ]
    bc.sendConfigSet(devs[0], command)

    # check priority of root bridge
    string = '1/16' 
    column =   6                              
    reString = get_mst_instancee_cloumns(devs[0],string,column)
    result.extend(reString)
    print('reString :', reString)
    time.sleep(3)
             
    print(result)            
    if  result == ['boundary','boundary','boundary','Non','Non','Non']:
        return True
    else:
        False     
      
 ##### check_MSTP_Regions(VLAN,NAME,REVISION) #####
def check_mstp_region_revision(devs):    
    result =[]
        
    # To configure priority of each MST instance. 
    command = [
        'spanning-tree mst configuration',
        'revision 11'
        ]
    bc.sendConfigSet(devs[0], command)
                                                            
    # check priority of root bridge
    string = '1/16' 
    column =   6                              
    reString = get_mst_instancee_cloumns(devs[0],string,column)
    result.extend(reString)
    print('reString :', reString)
    time.sleep(3)
   
    # To remove priority of each MST instance. 
    command = [
        'spanning-tree mst configuration',
        'no revision',        
        ]
    bc.sendConfigSet(devs[0], command)

    # check priority of root bridge
    string = '1/16' 
    column =   6                              
    reString = get_mst_instancee_cloumns(devs[0],string,column)
    result.extend(reString)
    print('reString :', reString)
    time.sleep(3)
             
    print(result)            
    if  result == ['boundary','boundary','boundary','Non','Non','Non']:
        return True
    else:
        False     

 ##### check_MSTP_PortRole_Master #####
def check_mstp_portRole_master(devs):    
    result =[]

    # Configure DUT1 xSTP mode as STP
    time.sleep(3)       
    stpModeConf([devs[0]],'stp') # To input list

    time.sleep(15)                                                              
    # check priority of root bridge
    string = '1/15' 
    column =  1 
    column2 =  6    
                               
    # reString = get_mst_instancee_cloumns(devs[1],string,column)
    reString = get_mst_instancee_multi_cloumns(devs[1],string,column,column2)
    result.extend(reString)
    print('reString :', reString)
    time.sleep(2)

    # To remove priority of each MST instance. 

    # Configure DUT1 xSTP mode as MSTP and Multi Instance    
    stpModeConf([devs[0]],'mst') # To input list
    time.sleep(2)
        
    mstpMultiInstance([devs[0]])  # To input list
    time.sleep(10) 
               
    # check priority of root bridge
    string = '1/15' 
    column =   1  
                                
    # reString = get_mst_instancee_cloumns(devs[1],string,column)
    reString = get_mst_instancee_multi_cloumns(devs[1],string,column,column2)
    result.extend(reString)
    print('reString :', reString)
    time.sleep(2)
             
    print(result)            
    if  result == [['Root', 'boundary'], ['Mstr', 'boundary'], ['Mstr', 'boundary'], 'Non', 'Non', 'Non']:
        return True
    else:
        False  


##### check_xstp_with_LACP #####
def check_STP_compatibility_with_xSTP(devs):    
    result =[]

    # To remove priority of each MST instance. 
    mode = 'stp'
    command = [ f'spanning-tree mode {mode} ']
    bc.sendConfigSet(devs[0], command)

    mode = 'rstp'
    command = [ f'spanning-tree mode {mode} ']
    bc.sendConfigSet(devs[1], command)

    mode = 'mst'
    command = [ f'spanning-tree mode {mode} ']
    bc.sendConfigSet(devs[2], command)

    
    time.sleep(15)                                                              
    # check priority of root bridge
    string = '1/15' 
    column =  1 
    column2 = 6 
                              
    reString = get_stp_cli_Multi_colum(devs[1],string,column,column2)
    result.extend(reString)
    print('reString :', reString)
    time.sleep(2)

    # check priority of root bridge
    string = '1/16' 
    column =  1 
    column2 = 6 
                              
    reString = get_stp_cli_Multi_colum(devs[2],string,column,column2)
    result.extend(reString)
    print('reString :', reString)
    time.sleep(2)
                  
    print(result)            
    if  result == ['Root', '(STP)', 'Root', 'boundary']:
        return True
    else:
        False 


 ##### check_xstp_with_LACP #####
def check_xstp_with_LACP(devs):    
    result =[]

    # To remove priority of each MST instance. 
    command = [
        'interface range 1/15-1/16',
        'channel-group 1 mode active'        
        ]
    bc.sendConfigSet(devs[0], command)
    bc.sendConfigSet(devs[1], command)
    
    time.sleep(30)  #                                                            
    # check priority of root bridge
    string = 'po1' 
    column =  1 
    column2 =  3 
                              
    reString = get_stp_cli_Multi_colum(devs[1],string,column,column2)
    result.extend(reString)
    print('reString :', reString)
    time.sleep(5)
    
    # To remove priority of each MST instance. 
    command = [
        'interface range 1/15-1/16',
        'no channel-group '        
        ]
    bc.sendConfigSet(devs[0], command)
    bc.sendConfigSet(devs[1], command)
             
    # check priority of root bridge
    string = '1/15' 
    column =   1
    column2 =  3   
                                
    reString = get_stp_cli_Multi_colum(devs[1],string,column,column2)
    result.extend(reString)
    print('reString :', reString)
    time.sleep(2)
             
    print(result)            
    if  result == ['Root', '1000', 'Root', '2000']:
        return True
    else:
        False 
                                                   
##############################################################################
        
def stpSystemPri(dut,mode,syspri):
    with bc.connect(dut) as child:
        if mode == 'mst':            
            stp_mode_config =[
            f'spanning-tree mst 0 priority {syspri}'
            ]
            child.send_config_set(stp_mode_config)
            time.sleep(1)                            
        else:                
            stp_mode_config =[
            f'spanning-tree priority {syspri}'
            ]
            child.send_config_set(stp_mode_config) 
            time.sleep(1)     
                                                                                                       
def stpModeConf(devs,mode):
    for dev in devs:    
        with bc.connect(dev) as child:
            stp_mode_config = f'spanning mode {mode}'
            child.send_config_set(stp_mode_config)
            time.sleep(1)               

                       
def stpEdgePortConf(dev,int):
    with bc.connect(dev) as child:
        stp_edgeport_config =[
            f'interface {int}',
            'spanning port type edge'
        ]
        child.send_config_set(stp_edgeport_config)  
        time.sleep(1)
            
def noStpEdgePortConf(dev,int):
    with bc.connect(dev) as child:
        stp_edgeport_config =[
            f'interface {int}',
            'no spanning port type'
        ]
        child.send_config_set(stp_edgeport_config)  
        time.sleep(1)
            
def stpPathCost(dut, mode):
    with bc.connect(dut) as child:
        stp_edgeport_config =[
            f'spanning-tree pathcost method {mode}',
        ]
        child.send_config_set(stp_edgeport_config)  
        time.sleep(1)
                                           

def stpTimerConf(dut,hello,forwardDelaty,maxage):
    with bc.connect(dut) as child:
        stp_timer_config =[
            f'spanning-tree hello-time {hello}',
            f'spanning-tree forward-time {forwardDelaty}',
            f'spanning-tree max-age {maxage}',
        ]
        child.send_config_set(stp_timer_config)  
        time.sleep(1)

def stpRootGuardConf(dut):
    with bc.connect(dut) as child:
        stp_rootguard_config =[
            'interface range 1/15-1/16',
            'spanning-tree guard root'                
        ]
        child.send_config_set(stp_rootguard_config)  
        time.sleep(1)

def noStpRootGuardConf(dut):
    with bc.connect(dut) as child:
        stp_rootguard_config =[
            'interface range 1/15-1/16',
            'no spanning-tree guard root'
        ]
        child.send_config_set(stp_rootguard_config)  
        time.sleep(1)                                    

def stpBpduGuardConf(dut):
    with bc.connect(dut) as child:
        stp_bpduguard_config =[
            'interface range 1/16',
            'spanning-tree bpduguard enable'                
        ]
        child.send_config_set(stp_bpduguard_config)  
        time.sleep(1)

def noStpBpduGuardConf(dut):
    with bc.connect(dut) as child:
        stp_bpduguard_config =[
            'interface range 1/16',
            'no spanning-tree bpduguard'
        ]
        child.send_config_set(stp_bpduguard_config)  
        time.sleep(1)  
                
def errdisBpduGuar(dut):
    with bc.connect(dut) as child:
        stp_bpduguard_config =[
            'errdisable recovery reason bpduguard'            
        ]
        child.send_config_set(stp_bpduguard_config)  
        time.sleep(1)        
                
def stpBpduFilterConf(dut):
    with bc.connect(dut) as child:
        stp_bpdufilter_config =[
            'interface 1/16',
            'spanning-tree bpdufilter enable'                
        ]
        child.send_config_set(stp_bpdufilter_config)  
        time.sleep(1)          
        
def noStpBpduFilterConf(dut):
    with bc.connect(dut) as child:
        stp_bpdufilter_config =[
            'interface 1/16',
            'no spanning-tree bpdufilter'             
        ]
        child.send_config_set(stp_bpdufilter_config)  
        time.sleep(1)       

def stpPortPridConf(dut,str):
    with bc.connect(dut) as child:
        stp_bpduguard_config =[
            f'interface range {str}',
            'spanning-tree port-priority 96'                
        ]
        child.send_config_set(stp_bpduguard_config)  
        time.sleep(1)

def noStpPortPridConf(dut,str):
    with bc.connect(dut) as child:
        stp_bpduguard_config =[
           f'interface range {str}',
            'no spanning-tree port-priority'
        ]
        child.send_config_set(stp_bpduguard_config)  
        time.sleep(1)
        
def stpPortCostConf(dut,str):
    with bc.connect(dut) as child:
        stp_bpduguard_config =[
            f'interface range {str}',
            'spanning-tree cost 1800'                
        ]
        child.send_config_set(stp_bpduguard_config)  
        time.sleep(1)

def noStpPortCostConf(dut,str):
    with bc.connect(dut) as child:
        stp_bpduguard_config =[
            f'interface range {str}',
            'no spanning-tree cost'
        ]
        child.send_config_set(stp_bpduguard_config)  
        time.sleep(1)

def mstpMultiInstance(devs):
    for dev in devs:    
        with bc.connect(dev) as child:
        # To configure MST Multi instance.  
            command1 = [
                'vlan 2-3',
                'interface range 1/10,1/11-1/16',
                'switchport mode trunk',
                'switchport trunk allowed vlan 1-3' 
            ]
            bc.sendConfigSet(dev,command1)

            command2 = [
                'spanning-tree mst configuration',
                'instance 1 vlan 2',
                'instance 2 vlan 3'   
            ]
            bc.sendConfigSet(dev,command2)

def noMstpMultiInstance(devs):
    for dev in devs:    
        with bc.connect(dev) as child:
        # To configure MST Multi instance. 
            command1 = [
                'spanning-tree mst configuration',
                'no instance 1',
                'no instance 2' 
            ]
            bc.sendConfigSet(dev,command1)
            command2 = [
                'interface range 1/10,1/11-1/16',
                'switchport mode access',
                'no vlan 2-3'
            ]
            bc.sendConfigSet(dev,command2)

