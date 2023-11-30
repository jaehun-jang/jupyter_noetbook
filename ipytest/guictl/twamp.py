import pyautogui
import time

def twampclient():
    # Open Windows start manu
    pyautogui.press('win')
    time.sleep(3)  # 

    # Execute the twampclirnt
    pyautogui.typewrite('twampclient')
    pyautogui.press('enter')
    time.sleep(7)  # 

    # Click Destination text box
    pyautogui.click(530, 100)
    time.sleep(2)  # 

    # Enter the destination address
    pyautogui.typewrite('\b'*10 +'2001:db8:1:1::201')
    pyautogui.press('enter')
    time.sleep(2)  #

    # Click light mode check box
    pyautogui.click(772, 141)
    time.sleep(2)  # 

    # Click start button 
    pyautogui.click(414, 161)
    time.sleep(12)  # 

    # Click result button 
    pyautogui.click(727, 384)
    time.sleep(2)  # 
   
     # Click close the program button  
    pyautogui.click(972, 64)
    time.sleep(2)  # 