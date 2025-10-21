import cv2
import mediapipe as mp
import time
import os
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

folderPath = r"C:\Users\ASUS\PycharmProjects\GoruntuIsleme\goruntuIsleme\parmakSayma\fingerImages"

if os.path.exists(folderPath):
    myList = os.listdir(folderPath)
    print(myList)
else:
    print("Klasör bulunamadı!")
# Resimleri Listeye Yükleme
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

mpHand = mp.solutions.hands  # mediapipe el modülü
hands = mpHand.Hands()  # El tespit modeli
mpDraw = mp.solutions.drawing_utils  # El çizim fonksiyonu

tipIds = [4, 8, 12, 16, 20]  # Baş parmak, işaret parmağı, orta parmak, yüzük parmağı, serçe parmak
pTime = 0

while True:
    success, img = cap.read()  # Kameradan görüntü al
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # MediaPipe RGB formatı ister

    results = hands.process(imgRGB)  # Elleri algıla
    # print(results.multi_hand_landmarks)
    lmLists = []

    # Eğer en az bir el tespit edilmişse
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)

            lmList = []
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            lmLists.append(lmList)

    for lmList in lmLists:
        if len(lmList) != 0:
            fingers = []

            # bas parmak
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # 4 parmak
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)
            print(totalFingers)

            # Görüntüye Parmak Sayısını Ekleyelim444444
            if 0 <= totalFingers < len(overlayList):
                h, w, c = overlayList[totalFingers - 1].shape
                img[0:h, 0:w] = overlayList[totalFingers - 1]

            cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(totalFingers), (50, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 8)

    # fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow('Original', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
