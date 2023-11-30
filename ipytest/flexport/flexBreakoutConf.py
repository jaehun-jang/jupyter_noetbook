# $language = "python"
# $interface = "1.0"


import sys
import time
import os
import basic.basicConf as bc
import flexport.flexVef as fv


###### Element of Main Function  ######

def disSubTitle(child,Title):
    print(child.send_command(Title ))

###### Element of Flexport Function  ######

### Breakout to 25G*4 ###	 	  
def breakoutTo25G(child):
    config_set = [f"flexport-group {13}","breakout 25g-4x"]
    child.send_config_set(config_set)
    time.sleep(1) 

### Breakout to 10G*4  ###	   
def breakoutTo10G(child):
    config_set = [f"flexport-group {14}","breakout 10g-4x"]
    child.send_config_set(config_set)
    time.sleep(1) 

### Detach 100G ### 	   
def detachBreakout(child):
    config_set = [f"flexport-group {14}","detach member all "]
    child.send_config_set(config_set)
    time.sleep(1) 

### Attach 100G ### 	   
def attachBreakout(child):
    config_set = [f"flexport-group {14}","attach member all "]
    child.send_config_set(config_set)
    time.sleep(1) 

### No Breakout###	   
def noBreakout(child):
    for intCon in range (13, 15):
        config_set = [f"flexport-group {intCon}","no breakout"]
        child.send_config_set(config_set)
        time.sleep(1) 

############################################################################
 
    
#+++++++++++++++++++++++ Flex-Port Main Function ++++++++++++++++++++++++++!

def flexPortBreakout(host):
    result = []
    with bc.connect(host) as child:
        ### Breakout to 25G*4 ###
        title = "### Breakout to 25G*4 ###"
        action = '100Gto25G'
        disSubTitle(child,title)
        breakoutTo25G(child)
        time.sleep(5)
        result.append(fv.checkBreakout(action,host))
        time.sleep(1)
        print(result)

        ### Breakout to 10G*4 ###       
        title = "### Breakout to 10G*4 ###"
        action = '100Gto10G'
        disSubTitle(child,title)
        breakoutTo10G(child)
        time.sleep(5)
        result.append(fv.checkBreakout(action,host))
        time.sleep(1)
        print(result)

        ### The functions below are prohibited. ###     
        # ### breakoutIntDetach ###       
        # title = "### breakoutIntDetach ###"
        # action = 'detach'
        # disSubTitle(child,title)
        # detachBreakout(child)
        # time.sleep(5)
        # result.append(fv.checkBreakout(action,host))
        # time.sleep(1)
        # print(result)

        # ### breakoutIntAttach ###       
        # title = "### breakoutIntAttach ###"
        # action = 'attach'
        # disSubTitle(child,title)
        # attachBreakout(child)
        # time.sleep(5)
        # result.append(fv.checkBreakout(action,host))
        # time.sleep(1)
        # print(result)

        ### release Breakout  ###       
        title = "### release Breakout ###"
        action = 'noBreakout'
        disSubTitle(child,title)
        noBreakout(child)
        time.sleep(5)
        result.append(fv.checkBreakout(action,host))
        time.sleep(1)
        print(result)
        return result.count('Ok')

## ++++++++++++++++++++++++++++++++++++++ ##

