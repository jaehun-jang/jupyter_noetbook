# $language = "python"
# $interface = "1.0"

import sys
import time
import os
import basic.basicConf as bc


###### Element of Main Function  ######
def disTitle(child,Title):
    child.send_command(Title )

### Flex-Port check Function             
def count_result(result_list, keyword, expected_count):
    print(keyword)
    print(expected_count)
    result = result_list.count(keyword)
    print(result)
    return 'Ok' if result == expected_count else 'Nok'

def checkFlexP(status, host):
    check_dict = {
        "Detach": lambda: count_result(result_list, 'disable', 16),
        "Attach": lambda: count_result(result_list, 'enable', 12),
        "CPRI": lambda: count_result(result_list, 'cpri', 12),
        "CPRI10": lambda: count_result(result_list, '60(Gb)', 12),
        "CPRI8": lambda: count_result(result_list, '50(Gb)', 12),
        "CPRI7": lambda: count_result(result_list, '20(Gb)', 12),
        "CPRI5": lambda: count_result(result_list, '4915', 8),
        "CPRI3": lambda: count_result(result_list, '2457', 8),
        "ETH": lambda: count_result(result_list, 'ethernet', 16),
        "25G": lambda: count_result(result_list, '50(Gb)', 12),
        "10G": lambda: count_result(result_list, '20(Gb)', 8),
        "1G" : lambda: count_result(result_list, '(ge)', 8)
    }
    
    with bc.connect(host) as sub_child:
        result_list = []
        flexport = sub_child.send_command('show flexport')
        result_list.append(flexport.splitlines())
        interfacestate = sub_child.send_command('show int status')
        result_list.append(interfacestate.splitlines())
        result_list= str(result_list).split()
        
        checkProcess = sub_child.send_command('sh interface statistics avg-type 1/19')
        print(checkProcess)
        
        if status in check_dict: 
        # With in, we can check whether the dictionary has a corresponding key.
            return check_dict[status]()  # Enter the Key of Dictionary
        else:
            return "Invalid status"


# Flex-Port Example check Function 
def checkFlexPExam(status, host):
    check_dict = {
        "Exampl1": lambda: count_result(result_list, "60(Gb)", 2),
        "Exampl2": lambda: count_result(result_list, "60(Gb)", 4),
        "Exampl3": lambda: count_result(result_list, "60(Gb)", 6),
        "Exampl4": lambda: count_result(result_list, "50(Gb)", 2),
        "Exampl5": lambda: count_result(result_list, "50(Gb)", 4),
    }
    
    with bc.connect(host) as sub_child:
        result_list = []
        flexport = sub_child.send_command('show flexport')
        result_list.append(flexport.splitlines())
        result_list= str(result_list).split()

        if status in check_dict: 
        # With in, we can check whether the dictionary has a corresponding key.
            return check_dict[status]()  # Enter the Key of Dictionary
        else:
            return "Invalid status"

# Flex-Port Breakout check Function 
def checkBreakout(status,host):               
    with bc.connect(host) as sub_child:
        flexport = sub_child.send_command('show flexport')
        print(flexport)
        result_list = flexport.splitlines() ## can,t use a "readlines" because the type
        result_list= str(result_list).split()

    if "100Gto25G" in status:   
        result1 = result_list.count('25(GbE)')
        result2 = result_list.count('breakout')
        result3 = result_list.count("1/25/1,1/25/2,1/25/3,1/25/4',")
        if result1 == 1 and result2 == 1 and result3 == 1: 
            return 'Ok' 
        else:
            return 'Nok'
    elif "100Gto10G" in status:  
        result1 = result_list.count('40(Gb)')
        result2 = result_list.count('breakout')
        result3 = result_list.count("1/26/1,1/26/2,1/26/3,1/26/4',")
        if result1 == 1 and result2 == 2 and result3 == 1: 
            return 'Ok' 
        else:
            return 'Nok'
    elif "detach" in status: ## Check a flexport type is CPRI
        result = result_list.count('breakout')
        if result == 2:
            return 'Ok' 
        else:
            return 'Nok'
    elif "attach" in status: ## Check a flexport type is CPRI
        result = result_list.count('enable')
        if result == 16:
            return 'Ok' 
        else:
            return 'Nok'
    elif "noBreakout" in status: ## Check a flexport type is CPRI
        result = result_list.count('breakout')
        if result == 0:
            return 'Ok' 
        else:
            return 'Nok'
        

### Show Flex Port ###	  
def ShowInFlex(child):
    child.send_command("show flexport")
    
### Show Interface ###	  
def ShowInt(child):
    child.send_command("show interface status")