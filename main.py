

import keyboard
import mouse
import cv2
import numpy as np
from pynput import keyboard
import pyautogui
from mss import mss

from PIL import Image


class ScrrenShotArea():
    def __init__(self):
        self.NumberOfActions = 0
        self.ReadingHeight = 300
        #{'left': 160, 'top': 160, 'width': 200, 'height': 200}
        self.ScreenWidth = pyautogui.size()[0]
        self.ScreenHight = pyautogui.size()[1]
        print("Size = ",self.ScreenHight,self.ScreenWidth)
        self.SearchFor = 'ball_base.png'
        self.StartPosition = None
     
     

    def FullScreenMode(self):
        self.StartPosition = {'left':0, 'top': 0, 'width': self.ScreenWidth, 'height': self.ScreenHight}
        self.Width = self.ScreenWidth
        self.Height = self.ScreenHight
        self.Run()


    def UpdateScreen(self):
        with mss() as sct:
            screenShot = sct.grab(self.StartPosition)
            img = np.flip(Image.frombytes(
                        'RGB', 
                        (screenShot.width, screenShot.height), 
                        screenShot.rgb, 
                    ),axis=-1)
            res = cv2.matchTemplate(np.array(img), cv2.imread(self.SearchFor), cv2.TM_CCOEFF_NORMED) 
            threshold = .7
            print(res)
            loc = np.where(res >= threshold)
            return loc,img

    def Run(self):
            while True:
                loc = self.UpdateScreen()[0]
                for pt in zip(*loc[::-1]):  # Switch columns and rows
                    img = self.UpdateScreen()[1]
                    FoundImage = cv2.rectangle(np.array(img), pt, (self.Width, pt[1] + 30), (0, 0, 255), 2)   
                    cv2.imwrite('MatchResult.png',np.array(FoundImage))
                    pyautogui.click(pt[0]+11,pt[1]+9)
                    if(self.NumberOfActions > 55):
                        return
                    self.NumberOfActions+=1
                    break

                    
                if cv2.waitKey(33) & 0xFF in (
                    ord('q'), 
                    27, 
                ):
                    break
        
    def StartLoopClick(self):
        image = cv2.imread('ImageToTranslate.png', cv2.IMREAD_COLOR)
        template = self.SearchFor
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        threshold = .8
        w = 20
        h = 20
        loc = np.where(res >= threshold)
        
        for pt in zip(*loc[::-1]):  # Switch columns and rows
            cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            mouse.move((pt[0]+w/2),pt[1]+h/2)
        cv2.imwrite('result.png', image)
    def StartListener(self):
            
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()  # start to listen on a separate thread
        listener.join()  # remove if main thread is polling self.keys



ScrrenShotArea().FullScreenMode()