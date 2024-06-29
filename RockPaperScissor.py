import random
import cv2
import time
import numpy as np
import keyboard as kb
from cvzone.HandTrackingModule import HandDetector as hd
moves=["rock","paper","scissor"]
gallery={'pScore': 0, 
         'cScore':0,
         'pMove':'Rock',
         'cMove':'Rock',
         'conPlay': True,
         'ppMove':'Undecided',
         'pcMove':'Undecided'
        }
def generateComputerMove():
    cc=random.randint(0,2)
    gallery['cMove']=moves[cc]    
def assignScore(move1,move2):
    if move1=="rock":
        if move2=="rock":
            return 0
        elif move2=="scissor":
            return 1
        else:
            return -1
    elif move1=="paper":
        if move2=="rock":
            return 1
        elif move2=="scissor":
            return -1
        else:
            return 0
    else:
        if move2=="rock":
            return -1
        elif move2=="scissor":
            return 0
        else:
            return 1
def showScore():
    print(f'Your Score: {gallery["pScore"]}     My Score: {gallery["cScore"]}')

def play():
        cap = cv2.VideoCapture(0)
        # Check that a camera connection has been established
        if not cap.isOpened():
            print("Error establishing connection")
            exit()
        pTime = 0 # prev time initially is 0
        while cap.isOpened():
            # Read an image frame
            ret, frame = cap.read()
            cTime = time.time()  #current time
            fps = 1/(cTime-pTime) # frame rate= 1/time diff
            pTime = cTime #current time becomes prev time
            cv2.putText(frame,f'FPS:{int(fps)}',(20,20),cv2.FONT_HERSHEY_PLAIN, 1.5, (255,0,255),3)
            if ret:
                #Defining Hands and Properties
                detector=hd(detectionCon=0.8,maxHands=1)
                hands,frame=detector.findHands(frame)
                
                if hands:
                    cv2.putText(frame,f'My Move:{gallery["cMove"]}',(400,350),cv2.FONT_HERSHEY_PLAIN, 1.5, (255,0,255),3)
                    hand1=hands[0]
                    fingersup1=detector.fingersUp(hand1)
                    if(fingersup1==[0,1,1,0,0]):
                        gallery["pMove"]=moves[2]
                    elif(fingersup1==[1,1,1,1,1]):
                        gallery["pMove"]=moves[1]
                    elif(fingersup1==[0,0,0,0,0]):
                        gallery["pMove"]=moves[0]
                    cv2.putText(frame,f'Your Move:{gallery["pMove"]}',(20,350),cv2.FONT_HERSHEY_PLAIN, 1.5, (255,0,255),3)
                    if gallery["ppMove"]!=gallery["pMove"]:
                        gallery["pcMove"]=gallery["cMove"]
                        generateComputerMove()
                    if gallery['cMove']!=gallery['pcMove']:
                        res=assignScore(gallery["pMove"],gallery['cMove'])
                        if res==1:
                            gallery["pScore"]+=1
                            gallery['ppMove']=gallery["pMove"]
                            gallery["pcMove"]=gallery["cMove"]
                            cv2.putText(frame,"+1 for You!",(300,300),cv2.FONT_HERSHEY_PLAIN, 1.5, (255,0,255),3)
                        elif res==-1:
                            gallery["cScore"]+=1
                            gallery['ppMove']=gallery["pMove"]
                            gallery["pcMove"]=gallery["cMove"]
                            cv2.putText(frame,"+1 for Me!",(300,300),cv2.FONT_HERSHEY_PLAIN, 1.5, (255,0,255),3)
                        else:
                            gallery['ppMove']=gallery["pMove"]
                            gallery["pcMove"]=gallery["cMove"]
                            cv2.putText(frame,"Same Same!",(300,300),cv2.FONT_HERSHEY_PLAIN, 1.5, (255,0,255),3)
                cv2.putText(frame,f'Player:{gallery["pScore"]}                           Computer:{gallery["cScore"]}',(20,50),cv2.FONT_HERSHEY_PLAIN, 1.5, (255,0,255),3)
                cv2.imshow('Rock Paper Scissor', frame)
        
            if cv2.waitKey(25) == 27:
                cap.release()
                cv2.destroyAllWindows()
play()
    


    
