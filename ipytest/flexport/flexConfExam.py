# $language = "python"
# $interface = "1.0"


import sys
import time
import os
import basic.basicConf as bc
import flexport.flexVef as fv

###### Element of Main Function  ######

def dissubTitle(child,Title):
    print(child.send_command(Title))

##++++++++++++++++++++++++++++++++++++++++++=====================+++###  
### Sample Code Jae-Hun-Jang ### 
def attach100g(child):
    for intCon in range (13, 17, 1):
        config_set = ["flexport-group " + {str(intCon)},"attach member all"]
        child.send_config_set(config_set)
        time.sleep(1)
### Sample Code Formatting ### 
def sample_code(child):
    for intCon in range(13, 17):
        config_set = [f"flexport-group {intCon}", "attach member all"]
        child.send_config_set(config_set)
        time.sleep(1)
### Sample Code list comprehension ### 
def sample_code(child):
    config_sets = [[f"flexport-group {intCon}", "attach member all"] for intCon in range(13, 17)]
    [child.send_config_set(config_set) for config_set in config_sets]
    time.sleep(1)
### Sample Code Generator ### 
def attach100g(child):
    config_sets = ([f"flexport-group {intCon}", "attach member all"] for intCon in range(13, 17))
    for config_set in config_sets:
        child.send_config_set(config_set)
        time.sleep(1)
##++++++++++++++++++++++++++++++++++++++====================+++++++###   

### Detach 100G ### 	   
def detach100g(child):
    for intCon in range (13, 17, 1):
        config_set = [f"flexport-group {intCon}","detach member all"]
        child.send_config_set(config_set)
        time.sleep(1)

### Attach 100G ### 	   
def attach100g(child):
    for intCon in range (13, 17, 1):
        config_set = [f"flexport-group {intCon}","attach member all"]
        child.send_config_set(config_set)
        time.sleep(1)

### Change ETH to CPRI ###	 	  
def chgEthToCpri(child):
    for intCon in range (1, 13, 1):
        config_set = [f"flexport-group {intCon}","port-type cpri max-speed cpri7"]
        child.send_config_set(config_set)
        time.sleep(1) 

### Change CPRI to ETH ###	   
def chgCpriToEth(child):
    for intCon in range (1, 13, 1):
        config_set = [f"flexport-group {intCon}","port-type ethernet max-speed 10"]
        child.send_config_set(config_set)
        time.sleep(1) 

### ### Restore Speed  CPRI7###	   
def restCpriSpeed7(child):
    for intCon in range (1, 13, 1):
        config_set = [f"flexport-group {intCon}","max-speed cpri7"]
        child.send_config_set(config_set)
        time.sleep(1) 

### Exanple 1  ###  
def example1(child):
    config_G1_cpri10 = ('flexport-group 1','max-speed cpri10')
    child.send_config_set(config_G1_cpri10)
    time.sleep(1.5)
    config_G2_cpri10 = ('flexport-group 2','max-speed cpri10')
    child.send_config_set(config_G2_cpri10)
    time.sleep(1.5)

### Exanple 2  ###  
def example2(child):
    config_G4_cpri8 = ('flexport-group 4','max-speed cpri8')
    child.send_config_set(config_G4_cpri8)
    time.sleep(1.5)
    config_G4_cpri10 = ('flexport-group 4','max-speed cpri10')
    child.send_config_set(config_G4_cpri10)
    time.sleep(1.5)
    config_G3_cpri10 = ('flexport-group 3','max-speed cpri10')
    child.send_config_set(config_G3_cpri10)
    time.sleep(1.5)  

### Exanple 3  ###  
def example3(child):
    config_G5_cpri8 = ('flexport-group 5','max-speed cpri8')
    child.send_config_set(config_G5_cpri8)
    time.sleep(1.5)
    config_G6_cpri8 = ('flexport-group 6','max-speed cpri8')
    child.send_config_set(config_G6_cpri8)
    time.sleep(1.5)
    config_G5_cpri7 = ('flexport-group 5','max-speed cpri7')
    child.send_config_set(config_G5_cpri7)
    time.sleep(1.5)  
    config_G6_cpri10 = ('flexport-group 6','max-speed cpri10')
    child.send_config_set(config_G6_cpri10)
    time.sleep(1.5) 
    config_G5_cpri10 = ('flexport-group 5','max-speed cpri10')
    child.send_config_set(config_G5_cpri10)
    time.sleep(1.5) 

### Exanple 4  ###  
def example4(child):
    config_G7_cpri10 = ('flexport-group 7','max-speed cpri10')
    child.send_config_set(config_G7_cpri10)
    time.sleep(1.5)
    config_G8_cpri10 = ('flexport-group 8','max-speed cpri10')
    child.send_config_set(config_G8_cpri10)
    time.sleep(1.5)
    config_G7_cpri7 = ('flexport-group 7','max-speed cpri7')
    child.send_config_set(config_G7_cpri7)
    time.sleep(1.5)  
    config_G8_cpri8 = ('flexport-group 8','max-speed cpri8')
    child.send_config_set(config_G8_cpri8)
    time.sleep(1.5) 
    config_G7_cpri8 = ('flexport-group 7','max-speed cpri8')
    child.send_config_set(config_G7_cpri8)
    time.sleep(1.5) 
    

### Exanple 5  ###  
def example5(child):
    config_G9_25 = ('flexport-group 9','max-speed 25')
    child.send_config_set(config_G9_25)
    time.sleep(1.5)
    config_G10_25 = ('flexport-group 10','max-speed 25')
    child.send_config_set(config_G10_25)
    time.sleep(1.5)
    config_G9_10 = ('flexport-group 9','max-speed 10')
    child.send_config_set(config_G9_10)
    time.sleep(1.5)  
    config_G10_cpri7 = ('flexport-group 10','max-speed cpri7')
    child.send_config_set(config_G10_cpri7)
    time.sleep(1.5) 
    config_G9_cpri8 = ('flexport-group 9','max-speed cpri8')
    child.send_config_set(config_G9_cpri8)
    time.sleep(1.5) 
    config_G10_cpri8 = ('flexport-group 10','max-speed cpri8')
    child.send_config_set(config_G10_cpri8)
    time.sleep(1.5)     
 
############################################################################
 
    
#+++++++++++++++++++++++ Flex-Port Main Function ++++++++++++++++++++++++++!

''' Previous Test Item
[1]Example1 (CPRI7 to CPRI10)
[2]Example2 (CPRI7/8 to CPRI10)
[3]Example3 (CPRI8 to CPRI10)
[4]Example4 (CPRI10 to CPRI8)
[5]Example5 (Ethernet to CPRI8)
'''
def confFlexPortExam(host):
    result = []
    with bc.connect(host) as child:
        ### Change Flex Port To CPRI ###
        title = "### Change Flex Port To CPRI ###"
        action = 'CPRI'
        dissubTitle(child,title)
        detach100g(child)
        time.sleep(5)
        chgEthToCpri(child)
        time.sleep(10)
        result.append(fv.checkFlexP(action,host))
        time.sleep(1)

        ### Flex Port 'Exampl1 ###       
        title = "### Flex Port 'Exampl1' ###"
        action = 'Exampl1'
        dissubTitle(child,title)
        example1(child)
        time.sleep(5)
        result.append(fv.checkFlexPExam(action,host))
        time.sleep(1)

        ### Flex Port 'Exampl2 ###       
        title = "### Flex Port 'Exampl2' ###"
        action = 'Exampl2'
        dissubTitle(child,title)
        example2(child)
        time.sleep(5)
        result.append(fv.checkFlexPExam(action,host))
        time.sleep(1)

        ### Flex Port 'Exampl3 ###       
        title = "### Flex Port 'Exampl3' ###"
        action = 'Exampl3'
        dissubTitle(child,title)
        example3(child)
        time.sleep(5)
        result.append(fv.checkFlexPExam(action,host))
        time.sleep(1)

        ### Flex Port 'Exampl4 ###       
        title = "### Flex Port 'Exampl4' ###"
        action = 'Exampl4'
        dissubTitle(child,title)
        example4(child)
        time.sleep(5)
        result.append(fv.checkFlexPExam(action,host))
        time.sleep(1)

        ### Flex Port 'Exampl5 ###       
        title = "### Flex Port 'Exampl5' ###"
        action = 'Exampl5'
        dissubTitle(child,title)
        example5(child)
        time.sleep(5)
        result.append(fv.checkFlexPExam(action,host))
        time.sleep(1)

        ### Restore Cpri Speed CPRI7 ###
        restCpriSpeed7(child)
        time.sleep(10)

        ### Change Flex Port To ETH ###
        title = "### Change Flex Port To ETH ###"
        action = 'ETH'
        dissubTitle(child,title)
        attach100g(child)
        time.sleep(5)   
        chgCpriToEth(child)
        time.sleep(10)
        result.append(fv.checkFlexP(action,host))
        time.sleep(1)
        
        print(result)
        return result.count('Ok')
## ++++++++++++++++++++++++++++++++++++++ ##

