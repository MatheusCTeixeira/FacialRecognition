

import os       #create path 
import face_recognition     #recognize face
import cv2      #process video and save pictures
import sys

PATH = "./People/"
name = ""
count = 0


i = sys.argv.index("-f", 0)

name = sys.argv[i + 1]

if os.path.exists(PATH + name) == False:
    os.makedirs(PATH + name)

video = cv2.VideoCapture(0) #Captura a partir da camera

cv2.namedWindow("Cadastro")

while True:
    #Obtém um frame
    val, frame = video.read()

    #Localiza faces nas imagens
    locations = face_recognition.face_locations(frame)

    for location in locations:
        top, right, bottom, left = location

        color = (255, 0, 0)

        # Salva a image se 's' for pressionado
        if cv2.waitKey(33) == ord('s'):
            face_ROI = frame[top - 20 : bottom + 20, left - 20 : right + 20]

            cv2.imwrite(PATH + name + "/" + str(count) + ".jpg", face_ROI)

            color = (0, 0, 255)

            count += 1

        #Desenha um retângulo para destacar a face reconhecida
        cv2.rectangle(frame, (left - 10, top - 10), (right + 10, bottom + 10), color, 2)



    cv2.imshow("Cadastro", frame)
    
    if cv2.waitKey(33) == ord('q'):
        cv2.destroyWindow("Cadastro")
        break

exit()


