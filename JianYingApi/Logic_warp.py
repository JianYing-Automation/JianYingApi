"""
    Some Logic Warps

"""
import os
import subprocess
import multiprocessing
import uiautomation as api32
import time

lag_t = 0.5
def lag(lag:float=lag_t): time.sleep(lag)

def _creat_exe(exepath:str): return multiprocessing.Process(target=os.system,args=(exepath,))

def _has_running()->bool:
        if ("jianyingpro") in os.popen("tasklist").read().lower():return True
        if ("vedetector") in os.popen("tasklist").read().lower():return True
        return False

def _kill_jianYing(): 
    while _has_running():
        subprocess.Popen('%s%s' % ("taskkill /F /T /IM ","VEDetector.exe"),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).wait()
        subprocess.Popen('%s%s' % ("taskkill /F /T /IM ","JianYingPro.exe"),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).wait()
        subprocess.Popen('%s%s' % ("taskkill /F /T /IM ","jy.exe"),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).wait()
        time.sleep(0.5)

def _Get_JianYing_Default_Path()->str:
        # When U install Jian Ying On Default Path, It would Be This
        return "C:/Users/{}/AppData/Local/JianyingPro".format(os.popen("whoami").read().replace("\n","").split("\\")[1])

def echo(message):
    os.system(f"echo {message}")

def _install_JianYing(Installer_Path:str):
    _path_will_install = os.path.join(_Get_JianYing_Default_Path() , "Apps" , "Configure.ini")
    assert os.path.exists(os.path.join(_path_will_install,"Apps","JianyingPro.exe")) == False , "Has Been Installed!"
    __install_process = _creat_exe(Installer_Path)
    __install_process.start()
    while not api32.WindowControl(searchDepth=1,ClassName="#32770").Exists() : lag() # Keep it Roll until it turns up
    __install_inst = api32.WindowControl(searchDepth=1,ClassName="#32770")
    api32.Click(
        x=__install_inst.BoundingRectangle.xcenter(),
        y=int(__install_inst.BoundingRectangle.ycenter()-__install_inst.BoundingRectangle.height()/8))
    while not os.path.exists(_path_will_install): lag()
    __install_process.terminate()
    _kill_jianYing()
    echo("Install Finished")