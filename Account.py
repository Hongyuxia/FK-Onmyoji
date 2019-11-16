import threading
import keyboard
import win32gui
import win32con
import win32clipboard
import os

from Util import *
from Config import *
from GUI import *

screenWidth,screenHeight=pyautogui.size()

IMAGE_FAILED_PATH="./screenshots/failed.png"
IMAGE_SCREENSHOT_PATH="./screenshots/screenshot.png"
IMAGE_CONNECTING_PATH="./screenshots/connecting.png"
IMAGE_ASSISTANCE_PATH="./screenshots/assistance.png"
IMAGE_ACCEPT_PATH="./screenshots/accept.png"
IMAGE_OCCUPIED_PATH="./screenshots/occupied.png"
IMAGE_FOOD_INSUFFICIENCY_PATH="./screenshots/food.png"
IMAGE_CLOSE_DIALOG_PATH="./screenshots/close.png"

IMAGE_MITAMA_START_PATH="./screenshots/Mitama/start.png"
IMAGE_MITAMA_FINISHED1_PATH="./screenshots/Mitama/finished1.png"
IMAGE_MITAMA_FINISHED2_PATH="./screenshots/Mitama/finished2.png"

IMAGE_STROY_INVITE_PATH="./screenshots/Story/invite.png"
IMAGE_STROY_INVITATION_CONFIRMED_PATH="./screenshots/Story/invitationConfirmed.png"
IMAGE_STROY_START_PATH="./screenshots/Story/start.png"
IMAGE_STROY_FIGHT_PATH="./screenshots/Story/fight.png"
IMAGE_STROY_FIGHT_BOSS_PATH="./screenshots/Story/fightBoss.png"
IMAGE_STROY_FINISHED1_PATH="./screenshots/Story/finished1.png"
IMAGE_STROY_FINISHED2_PATH="./screenshots/Story/finished2.png"
IMAGE_STROY_ACCEPT_PATH="./screenshots/Story/accept.png"
IMAGE_STROY_BACK_PATH="./screenshots/Story/back.png"
IMAGE_STROY_GET_REWARD_PATH="./screenshots/Story/getReward.png"
IMAGE_STROY_REWARD_CONFIRMED_PATH="./screenshots/Story/rewardConfirmed.png"
IMAGE_STROY_READY_PATH="./screenshots/Story/ready.png"
IMAGE_STROY_READY_MARK_PATH="./screenshots/Story/readyMark.png"
IMAGE_STROY_SELECT_LEVEL_PATH="./screenshots/Story/selectLevel.png"
IMAGE_STROY_FULL1_PATH="./screenshots/Story/full1.png"
IMAGE_STROY_FULL2_PATH="./screenshots/Story/full2.png"
IMAGE_STROY_FOOD_PATH="./screenshots/Story/food.png"
IMAGE_STROY_CHERRY_CAKE_PATH="./screenshots/Story/cherryCake.png"

IMAGE_STROY_SHIKIGAMI_SELECTED_PATH="./screenshots/Story/shikigamiSelected.png"
IMAGE_STROY_SELECTED_LEVEL_PATH="./screenshots/Story/selectedLevel.png"

IMAGE_MITAMA_X_START_PATH="./screenshots/MitamaX/start.png"
IMAGE_MITAMA_X_FINISHED1_PATH="./screenshots/MitamaX/finished1.png"
IMAGE_MITAMA_X_FINISHED2_PATH="./screenshots/MitamaX/finished2.png"

IMAGE_BREACH_START_PATH="./screenshots/Breach/start.png"
IMAGE_BREACH_SECTION_PATH="./screenshots/Breach/section.png"
IMAGE_BREACH_FINISHED1_PATH="./screenshots/Breach/finished1.png"
IMAGE_BREACH_FINISHED2_PATH="./screenshots/Breach/finished2.png"
IMAGE_BREACH_SHIKIGAMI_SELECTED_PATH="./screenshots/Breach/shikigamiSelected.png"
IMAGE_BREACH_SELECTION_MARK_PATH="./screenshots/Breach/selectionMark.png"

IMAGE_CLUB_BREACH_READY_PATH="./screenshots/ClubBreach/ready.png"
IMAGE_CLUB_BREACH_FINISHED2_PATH="./screenshots/ClubBreach/finished2.png"
#
_localVariable=threading.local()
_DETECTION_INTERVAL=0.25
_GLOBAL_CONFIG_PATH="./config.ini"
_globalConfig=Config(_GLOBAL_CONFIG_PATH)
_accountCount=0
_fullShikigamiCount=0

_detectPauseThread=threading.Thread()
_accountLocker=threading.Lock()
_feedbackerLocker=threading.Lock()
#
class Account(threading.Thread):
    def __init__(self,gameMode,total,startX=0,startY=0,windowWidth=screenWidth,windowHeight=screenHeight,isCaptain=False,feedbackerName=None):
        threading.Thread.__init__(self)
        global _globalConfig
        global _accountCount
        global _detectPauseThread
        global _accountLocker

        self.__startX=startX
        self.__startY=startY
        self.__windowWidth=windowWidth
        self.__windowHeight=windowHeight
        self.__gameMode=gameMode
        self.__total=total
        self.__isCaptain=isCaptain
        self.__feedbackerName=feedbackerName

        self.__gui=GUI(startX,startY,windowWidth,windowHeight)
        self.__id=_accountCount
        _accountCount+=1

        self._detectFailureThread=threading.Thread(None,self.detectFailure,args=())
        self._detectFailureThread.start()
        self._detectAssistance=threading.Thread(None,self.detectAssistance,args=())
        self._detectAssistance.start()
        self._detectOccupation=threading.Thread(None,self.detectOccupation,args=())
        self._detectOccupation.start()
        self._detectFoodInsufficiency=threading.Thread(None,self.detectFoodInsufficiency,args=())
        self._detectFoodInsufficiency.start()

        _accountLocker.acquire()

        if not _detectPauseThread.isAlive():
            _detectPauseThread=threading.Thread(None,self.detectPause)
            _detectPauseThread.start()

        _accountLocker.release()
#
    @property
    def accountCount(self):
        return _accountCount
#
    def gameModeMitama(self):
        printWithTime("消息:账户:%s:多人御魂/觉醒"%(str(self.__id)))
        while True:
            screenshot = self.__gui.getScreenshot()
            time.sleep(_DETECTION_INTERVAL)

            if self.__isCaptain:
                position=self.__gui.getImagePositionInScreenshot(IMAGE_MITAMA_START_PATH,screenshot)
                if position != None:
                    printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_MITAMA_START_PATH,position.left,position.top))
                    self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                    continue
            
            position=self.__gui.getImagePositionInScreenshot(IMAGE_MITAMA_FINISHED1_PATH,screenshot)
            if position != None:
                printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_MITAMA_FINISHED1_PATH,position.left,position.top))
                self.__gui.clickPositionWithOffsets(position,2,0.2,self.__startX,self.__startY)
                continue

            position=self.__gui.getImagePositionInScreenshot(IMAGE_MITAMA_FINISHED2_PATH,screenshot)
            if position != None:
                printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_MITAMA_FINISHED2_PATH,position.left,position.top))
                self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                
                while True:
                    if not self.__gui.clickImageWithOffsets(IMAGE_MITAMA_FINISHED2_PATH,1,0.2):
                        break
                    printWithTime("消息:账户:%s:检测到图像:%s:位置"%(str(self.__id),IMAGE_MITAMA_FINISHED2_PATH))
                break  
#
    def gameModeStory(self):
        global _fullShikigamiCount
        printWithTime("消息:账户:%s:章节探索"%(str(self.__id)))

        while True:
            screenshot = self.__gui.getScreenshot()
            time.sleep(_DETECTION_INTERVAL)

            if self.__isCaptain:
                if not self.__gui.getImagePositionInScreenshot(IMAGE_STROY_CHERRY_CAKE_PATH,screenshot):
                    position=self.__gui.getImagePositionInScreenshot(IMAGE_STROY_INVITE_PATH,screenshot)
                    '''
                    if position != None:
                        winsound.Beep(500,1000)
                    '''
                    if position != None:
                        _localVariable.isBossDetected=False
                        printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_STROY_INVITE_PATH,position.left,position.top))
                        self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                        continue

                    position=self.__gui.getImagePositionInScreenshot(IMAGE_STROY_INVITATION_CONFIRMED_PATH,screenshot)
                    if position != None:
                        _localVariable.isBossDetected=False
                        printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_STROY_INVITATION_CONFIRMED_PATH,position.left,position.top))
                        self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                        continue

                    position=self.__gui.getImagePositionInScreenshot(IMAGE_STROY_START_PATH,screenshot)
                    if position != None:
                        _localVariable.isBossDetected=False
                        printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_STROY_START_PATH,position.left,position.top))
                        self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                        continue

                #检测目标
                if not _localVariable.isBossDetected and self.__gui.getImagePositionInScreenshot(IMAGE_STROY_CHERRY_CAKE_PATH,screenshot) and _localVariable.detectCount:
                    _localVariable.detectCount-=1
                    if (not self.__gui.isImageDetected(IMAGE_STROY_FIGHT_PATH)
                        and not self.__gui.isImageDetected(IMAGE_STROY_FIGHT_BOSS_PATH)):
                        self.__gui.setMouseToRandomPosition()
                        self.__gui.dragMouseToRandomPosition(_localVariable.xDirection,random.uniform(0.01,0.1))
                        printWithTime("账户:%s:第%s次检测:%s"
                                    %(str(self.__id),str(8-_localVariable.detectCount),IMAGE_STROY_FIGHT_PATH))
                        printWithTime("账户:%s:第%s次检测:%s"
                                    %(str(self.__id),str(8-_localVariable.detectCount),IMAGE_STROY_FIGHT_BOSS_PATH))
                        if _localVariable.detectCount==0:
                            _localVariable.detectCount=8
                            _localVariable.xDirection=-_localVariable.xDirection
                            
                position=self.__gui.getImagePositionInScreenshot(IMAGE_STROY_FIGHT_PATH,screenshot)
                if position != None:
                    printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_STROY_FIGHT_PATH,position.left,position.top))
                    self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                    continue

                position=self.__gui.getImagePositionInScreenshot(IMAGE_STROY_FIGHT_BOSS_PATH,screenshot)
                if position != None:
                    printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_STROY_FIGHT_BOSS_PATH,position.left,position.top))
                    self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                    _localVariable.isBossDetected=True
                    continue

                position=self.__gui.getImagePositionInScreenshot(IMAGE_STROY_FINISHED1_PATH,screenshot)
                if position != None:
                    printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_STROY_FINISHED1_PATH,position.left,position.top))
                    self.__gui.clickPositionWithOffsets(position,2,0.2,self.__startX,self.__startY)
                    continue

                position=self.__gui.getImagePositionInScreenshot(IMAGE_STROY_FINISHED2_PATH,screenshot)
                if position != None:
                    printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_STROY_FINISHED2_PATH,position.left,position.top))
                    self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                    
                    while True:
                        if not self.__gui.clickImageWithOffsets(IMAGE_STROY_FINISHED2_PATH,1,0.2):
                            break
                        printWithTime("消息:账户:%s:检测到图像:%s:位置"%(str(self.__id),IMAGE_STROY_FINISHED2_PATH))
                    break  
            else:

                if _globalConfig.replaceShikigamiIfFull and self.__gui.isImageDetected(IMAGE_STROY_FULL1_PATH,accuracy=0.7):
                    printWithTime("消息:账户:%s:已完成%d个满经验式神"%(str(self.__id),_fullShikigamiCount))

                    def inner():
                        global _fullShikigamiCount 
                        while not self.__gui.isImageDetected(IMAGE_STROY_READY_MARK_PATH):
                            time.sleep(0.1)
                            continue

                        self.__gui.clickCoordinate(self.__startX+self.__windowWidth/3,self.__startY+self.__windowHeight*2/3,1,0.1)
                        while not self.__gui.isImageDetected(IMAGE_STROY_SELECT_LEVEL_PATH,accuracy=0.5):
                            time.sleep(0.1)
                            self.__gui.clickCoordinate(self.__startX+self.__windowWidth/3,self.__startY+self.__windowHeight*2/3,1,0.1)

                        position=self.__gui.getImagePosition(IMAGE_STROY_SELECT_LEVEL_PATH,accuracy=0.5)
                        while True:
                            if not position:
                                position=self.__gui.getImagePosition(IMAGE_STROY_SELECT_LEVEL_PATH,accuracy=0.5)
                                continue
                            
                            self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                            if self.__gui.isImageDetected(IMAGE_STROY_SELECTED_LEVEL_PATH,accuracy=0.7):
                                break
                        
                        position=self.__gui.getImagePosition(IMAGE_STROY_SELECTED_LEVEL_PATH,accuracy=0.7)
                        while True:
                            if not position:
                                position=self.__gui.getImagePosition(IMAGE_STROY_SELECTED_LEVEL_PATH,accuracy=0.7)
                                continue          

                            self.__gui.clickPositionWithOffsets(position,2,0.2,self.__startX,self.__startY)    
                            if not self.__gui.isImageDetected(IMAGE_STROY_SELECT_LEVEL_PATH,accuracy=0.5):
                                break      
                        
                        count=0
                        while count<3:
                            count+=1

                            while True:
                                position=self.__gui.getImagePosition(IMAGE_STROY_SHIKIGAMI_SELECTED_PATH)
                                if position:
                                    break
                                self.__gui.moveToCenter()
                                self.__gui.scroll(-200)
                            
                            self.__gui.moveToImage(IMAGE_STROY_SHIKIGAMI_SELECTED_PATH)
                            
                            position=self.__gui.getImagePosition(IMAGE_STROY_FULL2_PATH,accuracy=0.7)
                            if position:
                                position=self.__gui.dragMouseTo(position.left,position.top+position.height*8,duration=1.0,interval=1.0)

                            positionTmp=self.__gui.getImagePosition(IMAGE_STROY_FULL2_PATH,accuracy=0.7)
                            if position!=positionTmp:
                                printWithTime("消息:账户:%s:已替换1名满经验式神"%(str(self.__id)))
                                _fullShikigamiCount+=1

                            if not self.__gui.isImageDetected(IMAGE_STROY_FULL2_PATH,accuracy=0.7):
                                break
                    
                    innerThread=threading.Thread(None,inner,str(self.__id))
                    innerThread.start()

                    seconds=30
                    time.sleep(1.0)
                    while seconds and innerThread.isAlive():
                        time.sleep(1.0)
                        seconds-=1
                    stopThread(innerThread)
                
                position=self.__gui.getImagePositionInScreenshot(IMAGE_STROY_READY_PATH,screenshot)
                if position != None:
                    printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_STROY_READY_PATH,position.left,position.top))
                    self.__gui.clickPositionWithOffsets(position,2,0.2,self.__startX,self.__startY)
                    continue

                position=self.__gui.getImagePositionInScreenshot(IMAGE_STROY_FINISHED1_PATH,screenshot)
                if position != None:
                    printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_STROY_FINISHED1_PATH,position.left,position.top))
                    self.__gui.clickPositionWithOffsets(position,2,0.2,self.__startX,self.__startY)
                    continue

                position=self.__gui.getImagePositionInScreenshot(IMAGE_STROY_FINISHED2_PATH,screenshot)
                if position != None:
                    printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_STROY_FINISHED2_PATH,position.left,position.top))
                    self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                    
                    while True:
                        if not self.__gui.clickImageWithOffsets(IMAGE_STROY_FINISHED2_PATH,1,0.2):
                            break
                        printWithTime("消息:账户:%s:检测到图像:%s:位置"%(str(self.__id),IMAGE_STROY_FINISHED2_PATH))
                    break  

                position=self.__gui.getImagePositionInScreenshot(IMAGE_STROY_ACCEPT_PATH,screenshot)
                if position != None:
                    printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_STROY_ACCEPT_PATH,position.left,position.top))
                    self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                    continue
            #奖励结算
            if (self.__gui.getImagePositionInScreenshot(IMAGE_STROY_BACK_PATH,screenshot) 
                or self.__gui.getImagePositionInScreenshot(IMAGE_STROY_REWARD_CONFIRMED_PATH,screenshot)):
                position=self.__gui.getImagePositionInScreenshot(IMAGE_STROY_GET_REWARD_PATH,screenshot)
                if position != None:
                    printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_STROY_GET_REWARD_PATH,position.left,position.top))
                    self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)

                position=self.__gui.getImagePositionInScreenshot(IMAGE_STROY_REWARD_CONFIRMED_PATH,screenshot)
                if position != None:
                    printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_STROY_REWARD_CONFIRMED_PATH,position.left,position.top))
                    self.__gui.clickCoordinate(self.__startX+self.__windowWidth/4+random.uniform(0.1,1)*self.__windowWidth/20,
                                            self.__startY+self.__windowHeight/8+random.uniform(0.1,1)*self.__windowHeight/20)
#
    def gameModeMitamaX(self):
        printWithTime("消息:账户:%s:单人御魂/业原火/御灵"%(str(self.__id)))
        while True:
            screenshot = self.__gui.getScreenshot()
            time.sleep(_DETECTION_INTERVAL)

            position=self.__gui.getImagePositionInScreenshot(IMAGE_MITAMA_X_START_PATH,screenshot)
            if position != None:
                printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_MITAMA_X_START_PATH,position.left,position.top))
                self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                continue
            
            position=self.__gui.getImagePositionInScreenshot(IMAGE_MITAMA_X_FINISHED1_PATH,screenshot)
            if position != None:
                printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_MITAMA_X_FINISHED1_PATH,position.left,position.top))
                self.__gui.clickPositionWithOffsets(position,2,0.2,self.__startX,self.__startY)
                continue

            position=self.__gui.getImagePositionInScreenshot(IMAGE_MITAMA_X_FINISHED2_PATH,screenshot)
            if position != None:
                printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_MITAMA_X_FINISHED2_PATH,position.left,position.top))
                self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                
                while True:
                    if not self.__gui.clickImageWithOffsets(IMAGE_MITAMA_X_FINISHED2_PATH,1,0.2):
                        break
                    printWithTime("消息:账户:%s:检测到图像:%s:位置"%(str(self.__id),IMAGE_MITAMA_X_FINISHED2_PATH))
                break 
#
    def gameModeBreach(self):
        printWithTime("消息:账户:%s:结界突破"%(str(self.__id)))
        while True:
            screenshot = self.__gui.getScreenshot()
            time.sleep(_DETECTION_INTERVAL*2)

            position=self.__gui.getImagePositionInScreenshot(IMAGE_BREACH_START_PATH,screenshot)
            if position != None:
                printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_BREACH_START_PATH,position.left,position.top))
                self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                continue

            position=self.__gui.getImagePositionInScreenshot(IMAGE_BREACH_SECTION_PATH,screenshot)
            if position != None:
                printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_BREACH_SECTION_PATH,position.left,position.top))
                self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                continue
            ''''''
            position=self.__gui.getImagePositionInScreenshot(IMAGE_BREACH_SELECTION_MARK_PATH,screenshot)
            if position != None:
                continue

            position=self.__gui.getImagePositionInScreenshot(IMAGE_BREACH_SHIKIGAMI_SELECTED_PATH,screenshot)
            if position != None:
                printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_BREACH_SHIKIGAMI_SELECTED_PATH,position.left,position.top))
                self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                continue
            ''''''
            position=self.__gui.getImagePositionInScreenshot(IMAGE_BREACH_FINISHED1_PATH,screenshot)
            if position != None:
                printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_BREACH_FINISHED1_PATH,position.left,position.top))
                self.__gui.clickPositionWithOffsets(position,2,0.2,self.__startX,self.__startY)
                continue

            position=self.__gui.getImagePositionInScreenshot(IMAGE_BREACH_FINISHED2_PATH,screenshot)
            if position != None:
                printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_BREACH_FINISHED2_PATH,position.left,position.top))
                self.__gui.clickPositionWithOffsets(position,1,0.2,self.__startX,self.__startY)
                
                while True:
                    if not self.__gui.clickImageWithOffsets(IMAGE_BREACH_FINISHED2_PATH):
                        break
                    printWithTime("消息:账户:%s:检测到图像:%s"%(str(self.__id),IMAGE_BREACH_FINISHED2_PATH))
                break  
#
    def gameModeClubBreach(self):
        printWithTime("消息:账户:%s:道馆"%(str(self.__id)))
        while True:
            screenshot = self.__gui.getScreenshot()
            time.sleep(_DETECTION_INTERVAL*4)

            position=self.__gui.getImagePositionInScreenshot(IMAGE_CLUB_BREACH_READY_PATH,screenshot)
            if position != None:
                printWithTime("消息:账户:%s:检测到图像:%s:位置:X=%.4f,Y=%.4f"%(str(self.__id),IMAGE_CLUB_BREACH_READY_PATH,position.left,position.top))
                self.__gui.clickPositionWithOffsets(position,2,0.2,self.__startX,self.__startY)
                time.sleep(_DETECTION_INTERVAL*4)

                while True:
                    if not self.__gui.clickImageWithOffsets(IMAGE_CLUB_BREACH_READY_PATH):
                        break
                    printWithTime("消息:账户:%s:检测到图像:%s"%(str(self.__id),IMAGE_CLUB_BREACH_READY_PATH))
                break  

#
    def detectPause(self):
        while True:
            keyboard.wait(hotkey='f12')

            if self.__gui.GUIIsAcquired():
                self.__gui.GUIRelease()
                printWithTime("账户:%s:已继续"%(str(self.__id)))
            else:
                self.__gui.GUIAcquire()
                printWithTime("账户:%s:已暂停"%(str(self.__id)))
#
    def detectFailure(self):
        while True:
            time.sleep(_DETECTION_INTERVAL*15)
            if not self.__gui.isImageDetected(IMAGE_FAILED_PATH):
                continue

            message="错误:账户:%s:失败，请重新运行!"%(str(self.__id))
            printWithTime(message)

            def inner():
                self.__gui.updateOperationTime()
                winsound.Beep(800,30000)
                
                if _globalConfig.closeGamesAfterFailure:
                    os.system("taskkill /IM onmyoji.exe /F")
                if _globalConfig.exitAfterFailure:
                    sys.exit()

                winsound.Beep(800,1000)

            threading.Thread(None,inner,str(str(self.__id))).start()
            time.sleep(1.0)
#
    def detectAssistance(self):
        while True:
            time.sleep(_DETECTION_INTERVAL*16)
            if not self.__gui.isImageDetected(IMAGE_ASSISTANCE_PATH):
                continue

            message="消息:账户:%s:检测到悬赏封印邀请"%(str(self.__id))
            printWithTime(message)
            threading.Thread(None,self.feedback,str(self.__id),args=(message,)).start()

            winsound.Beep(1000,100)
            self.__gui.clickImageWithOffsets(IMAGE_ACCEPT_PATH)

            message="消息:账户:%s:已尝试接受悬赏封印邀请"%(str(self.__id))
            printWithTime(message)
            threading.Thread(None,self.feedback,str(self.__id),args=(message,)).start()
#
    def detectOccupation(self):
        while True:
            time.sleep(_DETECTION_INTERVAL*16)
            if not self.__gui.isImageDetected(IMAGE_OCCUPIED_PATH):
                continue

            message="错误:账户:%s:检测到账户在其他设备登录"%(str(self.__id))
            printWithTime(message)
            threading.Thread(None,self.feedback,str(self.__id),args=(message,)).start()
            
            self.__gui.updateOperationTime()
            winsound.Beep(1000,10000)

            if _globalConfig.closeGamesIfOccupied:
                os.system("taskkill /IM onmyoji.exe /F")
            if _globalConfig.exitIfOccupied:
                sys.exit()
#
    def detectFoodInsufficiency(self):
        while True:
            time.sleep(_DETECTION_INTERVAL*20)
            if not self.__gui.isImageDetected(IMAGE_FOOD_INSUFFICIENCY_PATH):
                continue

            message="错误:账户:%s:检测到体力不足"%(str(self.__id))
            printWithTime(message)
            threading.Thread(None,self.feedback,str(self.__id),args=(message,)).start()
            self.__gui.clickImageWithOffsets(IMAGE_CLOSE_DIALOG_PATH)

            self.__gui.updateOperationTime()
            winsound.Beep(1000,5000)
            
            if _globalConfig.closeGamesIfFoodNotEnough:
                os.system("taskkill /IM onmyoji.exe /F")
            if _globalConfig.closeGamesIfFoodNotEnough:
                sys.exit()
                
            winsound.Beep(1000,1000)
#
    def feedback(self,message):
        global _feedbackerLocker

        printWithTime("账户:%s:反馈者:%s"%(str(self.__id),self.__feedbackerName))
        qqWindow = win32gui.FindWindow(None, self.__feedbackerName)
        if qqWindow==0:
            printWithTime("账户:%s:无法定位到反馈者:%s"%(str(self.__id),self.__feedbackerName))
            return
        _feedbackerLocker.acquire()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, message)
        win32clipboard.CloseClipboard()

        win32gui.SendMessage(qqWindow, 258, 22, 2080193)
        win32gui.SendMessage(qqWindow, 770, 0, 0)
        
        win32gui.SendMessage(qqWindow, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.SendMessage(qqWindow, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

        _feedbackerLocker.release()
#
    def run(self):
        count=0
        while self.__total:
            seconds=1
            while seconds:
                printWithTime("账户:%s:"%(str(self.__id))+str(seconds)+"s后开始")
                time.sleep(1)
                seconds-=1
            printWithTime("账户:%s:"%(str(self.__id))+"开始")
            printWithTime("账户:%s:"%(str(self.__id))+"\n"
                +"\t窗口起始位置X:"+str(self.__startX)+"\n"
                +"\t窗口起始位置Y:"+str(self.__startY)+"\n"
                +"\t窗口宽度:"+str(self.__windowWidth)+"\n"
                +"\t窗口高度:"+str(self.__windowHeight)+"\n"
                +"\t局数:"+str(self.__total)+"\n"
                +"\t是否为房主(Y/N):"+str(self.__isCaptain))

            if self.__gameMode==1:
                self.gameModeMitama()
            elif self.__gameMode==2:
                _localVariable.isEntered=False
                _localVariable.isFighting=False
                _localVariable.detectCount=8
                _localVariable.xDirection=-1.0
                self.gameModeStory()
            elif self.__gameMode==3:
                self.gameModeMitamaX()
            elif self.__gameMode==4:
                self.gameModeBreach()
            elif self.__gameMode==5:
                self.gameModeClubBreach()
    
            count+=1
            message="%s:账户:%s:游戏类型:%s,已完成%s局,还剩余%s局"%(getTimeFormatted(),str(self.__id),str(self.__gameMode),str(count),str(self.__total-count))
            threading.Thread(None,self.feedback,str(self.__id),args=(message,)).start()
            printWithTime(message)

        message="%s:账户:%s:游戏类型:%s,已完成"%(getTimeFormatted(),str(self.__id),str(self.__gameMode))
        threading.Thread(None,self.feedback,str(self.__id),args=(message,)).start()