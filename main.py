import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

# Setting up the web camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# creating hand detector
detector = HandDetector(detectionCon=0.8)

# Creating List for keys
keys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',';'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M',',','.','/'],
]

finalText = ""

keyboard = Controller()

def drawALL(img, buttonList):
    for button in buttonList:
    # Draw a button
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x+w, y+h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 5, y + 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
    return img


class Button():
    def __init__(self ,pos ,text , size = [45,45]):
        self.pos = pos
        self.size = size
        self.text = text
        
        
    
buttonList = []
for i in range(len(keys)) :
        for j , key in enumerate(keys[i]):
            buttonList.append(Button([60 * j + 50, 80 * i + 50],key))

while True:
    success, img = cap.read()  # Web camera
    hands, img = detector.findHands(img)  # Get hand data and modified image

    lmList = []

    if hands:
        lmList = hands[0]['lmList']       # Landmark list
        bboxInfo = hands[0]['bbox']       # Bounding box info
    img = drawALL(img, buttonList)
    

    if lmList:
         for button in buttonList:
              x,y = button.pos
              w, h = button.size

              if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h :
                   cv2.rectangle(img, button.pos, (x+w, y+h), (175, 0, 175), cv2.FILLED)
                   cv2.putText(img, button.text, (x + 5, y + 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
                   l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img )
                   #print(l)
               
                   if l<15:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x+w, y+h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 5, y + 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
                        finalText += button.text
                        sleep(0.20)
    cv2.rectangle(img, (50, 310), (600, 370), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 350), cv2.FONT_HERSHEY_PLAIN, 2.5, (255, 255, 255), 2)


    cv2.imshow("Image", img)
    cv2.waitKey(1)


 