# $language = "python"
# $interface = "1.0"


import sys
import time
import os

import basic.basicConf as bc
import flexport.flexVef as fv


###### Element of Main Function  ######

def disTitle(child,Title):
    print(child.send_command(Title))


###### Element of Flexport Function  ######
    
### Detach ###  
def detach(child):
    for intCon in range(1, 13):
        flexport_config = f"flexport-group {intCon}"
        detach_config = [f"detach member {i}" for i in range(1, 3)]
        config_set = [flexport_config] + detach_config
        child.send_config_set(config_set)
        time.sleep(1.5)
    for intCon in range(13, 17):
        flexport_config = f"flexport-group {intCon}"
        detach_config = ["detach member all"]
        config_set = [flexport_config] + detach_config
        child.send_config_set(config_set)
        time.sleep(1.5)

### Detach 100G ### 	   
def detach100g(child):
    for intCon in range (13, 17, 1):
        config = ["flexport-group " + str(intCon),"detach member all "]   
        child.send_config_set(config)
        time.sleep(1)
            
### Attach ### 	  
def attach(child):
    for intCon in range(1, 13):
        flexport_config = f"flexport-group {intCon}"
        detach_config = [f"attach member {i}" for i in range(1, 3)]
        config_set = [flexport_config] + detach_config
        child.send_config_set(config_set)
        time.sleep(1.5)
    # for intCon in range(13, 17):
    #     flexport_config = f"flexport-group {intCon}"
    #     detach_config = ["attach member all"]
    #     config_set = [flexport_config] + detach_config
    #     child.send_config_set(config_set)
    #     time.sleep(1.5)

### Attach 100G ### 	  
def attach100g(child):
    for intCon in range (13, 17, 1):
        config_set = ["flexport-group " + str(intCon),"attach member all "]   
        child.send_config_set(config_set)
        time.sleep(1.5)
            

### Change ETH to CPRI ###	 	  
def chgEthToCpri(child): 
    for intCon in range (1, 13, 1):
        config_set = ["flexport-group " + str(intCon),"port-type cpri "]   
        child.send_config_set(config_set)
        time.sleep(1.5)

### Change CPRI to ETH ###	   
def chgCpriToEth(child): 
    for intCon in range (1, 13, 1):
        config = ["flexport-group " + str(intCon),"port-type ethernet "]   
        child.send_config_set(config)
        time.sleep(1.5)

### Change CPRI Speed CPRI10###	   
def chgCpriSpeed10(child):
    for intCon in range (1, 13, 1):
        config = ["flexport-group " + str(intCon),"max-speed cpri10 "]   
        child.send_config_set(config)
        time.sleep(1.5)

### Change CPRI Speed  CPRI8###	   
def chgCpriSpeed8(child):
    for intCon in range (1, 13, 1):
        config = ["flexport-group " + str(intCon),"max-speed cpri8 "]   
        child.send_config_set(config)
        time.sleep(1.5)

### Change CPRI Speed  CPRI7###	   
def chgCpriSpeed7(child):
    for intCon in range (1, 13, 1):
        config = ["flexport-group " + str(intCon),"max-speed cpri7 "]   
        child.send_config_set(config)
        time.sleep(1.5)

### Change CPRI Speed  CPRI5###	   
def chgCpriSpeed5(child):
    for intCon in range (9, 17, 1):
        config = ["interface 1/" + str(intCon),"roe cpri option 5 "]   
        child.send_config_set(config)
        time.sleep(1.5)

### Change CPRI Speed  CPRI3###	   
def chgCpriSpeed3(child):
    for intCon in range (1, 9, 1):
        config = ["interface 1/" + str(intCon),"roe cpri option 3 "]   
        child.send_config_set(config)
        time.sleep(1.5)

### ### Restore Speed  CPRI7###	   
def restCpriSpeed7(child):
    for intCon in range (1, 13, 1):
        config = ["flexport-group " + str(intCon),"max-speed cpri7 "]   
        child.send_config_set(config)
        time.sleep(1.5)

### Change Speed 25G ### 	  
def chgEthSpeed25G(child): 
    for intCon in range (1, 13, 1):
        config = ["flexport-group " + str(intCon),"max-speed 25 "]   
        child.send_config_set(config)
        time.sleep(1.5)

### Change Speed 10G ### 	 	  
def chgEthSpeed10G(child):
    for intCon in range (1, 9, 1):
        config = ["flexport-group " + str(intCon),"max-speed 10"]   
        child.send_config_set(config)
        time.sleep(1.5)

### Change Speed 1G ### 	  
def chgEthSpeed1G(child):
    for intCon in range (1, 9, 1):
        config = ["interface 1/" + str(intCon),"speed 1000"]   
        child.send_config_set(config)
        time.sleep(1.5)

### Restore Speed 10G ### 	 	  
def restEthSpeed10G(child):
    for intCon in range (1, 13, 1):
        config = ["flexport-group " + str(intCon),"max-speed 10"]   
        child.send_config_set(config)
        time.sleep(1.5)

############################################################################
 
    
#+++++++++++++++++++++++ Flex-Port Main Function ++++++++++++++++++++++++++!

''' Previous Test Item
[1]Change Port status to Detach 
[2]Change Port status to Atach 
[3]Change Flex Port To CPRI 
[4]Change CPRI Speed CPRI10 
[5]Change CPRI Speed CPRI8 
[6]Change CPRI Speed CPRI7
[7]Change CPRI Speed CPRI3
[8]Change CPRI Speed CPRI5
[9]Change Flex Port To ETH
[10]Change Ethernet Speed 25G
[11]Change Ethernet Speed 10G
[12]Change Ethernet Speed 1G
'''
def confFlexPort(host):
    result = []
    with bc.connect(host) as child:
        ### Change Port status to Detach ###       
        title = "### Flex Port detach ###"
        action = 'Detach'
        disTitle(child,title)
        detach(child)
        time.sleep(15)
        result.append(fv.checkFlexP(action,host))
        time.sleep(1)
    #    print(result)

        ### Change Port status to Atach ###  
        title = "### Flex Port Attach ###"
        action = 'Attach'
        disTitle(child,title)
        attach(child)
        time.sleep(15)
        result.append(fv.checkFlexP(action,host))
        time.sleep(1)
    #    print(result)

        ### Change Flex Port To CPRI ###
        title = "### Change Flex Port To CPRI ###"
        action = 'CPRI'
        disTitle(child,title)
        chgEthToCpri(child)
        time.sleep(15)
        result.append(fv.checkFlexP(action,host))
        time.sleep(1)
    #    print(result)

        ### Change CPRI Speed CPRI10 ###	  
        title = "### Change CPRI Speed CPRI10###"	   
        action = 'CPRI10'
        disTitle(child,title)
        chgCpriSpeed10(child)
        time.sleep(15)
        result.append(fv.checkFlexP(action,host))
        time.sleep(1)
    #    print(result)

        ### Change CPRI Speed CPRI7 ###	  
        title = "### Change CPRI Speed CPRI7###"	   
        action = 'CPRI7'
        disTitle(child,title)
        chgCpriSpeed7(child)
        time.sleep(15)
        result.append(fv.checkFlexP(action,host))
        time.sleep(1)
    #    print(result)

        ### Change CPRI Speed CPRI5 ###	  
        title = "### Change CPRI Speed CPRI5###"	   
        action = 'CPRI5'
        disTitle(child,title)
        chgCpriSpeed5(child)
        time.sleep(15)
        result.append(fv.checkFlexP(action,host))
        time.sleep(1)
    #    print(result)

        ### Change CPRI Speed CPRI3 ###	  
        title = "### Change CPRI Speed CPRI3###"	   
        action = 'CPRI3'
        disTitle(child,title)
        chgCpriSpeed3(child)
        time.sleep(15)
        result.append(fv.checkFlexP(action,host))
        time.sleep(1)
    #    print(result)

        ### Change CPRI Speed CPRI8 ###	  
        title = "### Change CPRI Speed CPRI8###"	   
        action = 'CPRI8'
        disTitle(child,title)
        chgCpriSpeed8(child)
        time.sleep(15)
        result.append(fv.checkFlexP(action,host))
        time.sleep(1)
    #    print(result)

        ### Restore Cpri Speed CPRI7 ###
        restCpriSpeed7(child)
        time.sleep(1)

        ### Change Flex Port To ETH ###
        title = "### Change Flex Port To ETH ###"
        action = 'ETH'
        disTitle(child,title)
        chgCpriToEth(child)
        time.sleep(15)
        result.append(fv.checkFlexP(action,host))
        time.sleep(1)
    #    print(result)

        ### Change Ethernet Speed 25G ###
        Title = "### Change Ethernet Speed 25G ###" 
        action = '25G'
        disTitle(child,Title)
        chgEthSpeed25G(child)
        time.sleep(15) 
        result.append(fv.checkFlexP(action,host))
        time.sleep(1)
    #    print(result)

        ### Change Ethernet Speed 10G ###
        Title = "### Change Ethernet Speed 10G ###" 
        action = '10G'
        disTitle(child,Title)
        chgEthSpeed10G(child)
        time.sleep(15)      
        result.append(fv.checkFlexP(action,host))
        time.sleep(1)
    #    print(result)

        ### Change Ethernet Speed 1G ###
        Title = "### Change Ethernet Speed 1G ###"
        action = '1G'
        disTitle(child,Title)
        chgEthSpeed1G(child)
        time.sleep(15)   
        result.append(fv.checkFlexP(action,host))
        time.sleep(1)
    #    print(result)

        ### Restore Ethernet Speed 10G ###
        restEthSpeed10G(child)
        time.sleep(15)
        
        print(result)       
        return result.count('Ok')
## ++++++++++++++++++++++++++++++++++++++ ##

