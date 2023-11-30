# funMefVef.py
# $language = "python"

import sys
import time
import os
import basic.basicConf as bc

###### Element Function  ######


### Check Number of Service ###
def checkNmbrSvc(host):                 
    with bc.connect(host) as sub_child: 
        print('#'*3 + ' check Nmmber of SVCs ' + '#'*3)
        Command = "show ethernet nni"
        cmdResult = sub_child.send_command(Command)
        maxService = cmdResult.splitlines()[6].split(':')[1]
        print(maxService)
    return int(maxService) # 'Number of EVC in NNI#

### Check Number of UNI ###
def checkNmbrUni(host):                 
    with bc.connect(host) as sub_child:
        print('#'*3 + ' check Nmmber of UNIs ' + '#'*3)
        Command = 'show ethernet uni brief'
        cmdResult = sub_child.send_command(Command)
        cmdResult_list = cmdResult.splitlines()
        readResult = str(cmdResult_list)
        numofUni = readResult.count('uni')
        print(numofUni)
    return numofUni # 'UNI count by show ethernet uni brief#

### Check Number of SEP ###
def checkNmbrSep(uni,host):                 
    with bc.connect(host) as sub_child: 
        print('#'*3 + ' check Nmmber of SEPs ' + '#'*3)   
        Command = "show ethernet uni uni"
        resultSum = 0
        for i in range (1,uni+1,1):
                cmdResult = sub_child.send_command(Command+str(i))
                time.sleep(1)             
                readResult = cmdResult.splitlines()[12]
                result = readResult.split(':')
                resultSum  += int(result[1])
    print(resultSum)
    return resultSum # 'SUM of sep of UNIs#


# def checkDflSvc(host):                 
def checkDflSvc(host):
    result = 0
    with bc.connect(host) as sub_child:
        result += len(sub_child.send_command('show ethernet service').splitlines())
        result += len(sub_child.send_command('show ethernet uni').splitlines())
        result += len(sub_child.send_command('show ethernet nni').splitlines())
    time.sleep(1)
    print(result)
    return result
