
import face_recognition
import cv2
import os

DIR_IMAGE = "./People/"
UnknowPeople = "unknow people"

# Contém todas as faces a serem reconhecidas
all_people = []

for people_path in os.listdir(DIR_IMAGE):

    # Se não pasta não há necessidade de realizar verificação
    if os.path.isdir(DIR_IMAGE + people_path) == False:
        continue

    # O nome da pasta é o nome da pessoa a ser identificada
    new_people = [people_path,[]]
    print(people_path)

    for file_image in os.listdir(DIR_IMAGE + people_path):
        image = DIR_IMAGE + people_path + "/" + file_image
        
        # Se não for uma imagem não há necessidade de considerar o arquivo
        if os.path.isfile(image) == False:
            continue

        # Adiciona a imagem no dic da pessoa
        img = face_recognition.load_image_file(image)
        enc_img = face_recognition.face_encodings(img)
        if (len(enc_img) > 0 ):
            new_people[1].append(enc_img[0])
    
    # Acressenta ao dic geral
    all_people.append(new_people)

# Captura a partir da camera
video = cv2.VideoCapture(0)
cv2.namedWindow("frame")

# Faces reconhecidas no frame
Recognized_people = []

while True:

    # Obtém um frame de vídeo
    ret, frame = video.read()

    # Ajusta a imagem para acelerar o processamento e muda o formato de BGR para RGB
    frame_rsz = cv2.resize(frame, (0, 0), fx = 0.25, fy = 0.25)
    frame_bgr_rgb = frame_rsz[:,:,::-1]

    # Localiza as faces nos vídeos e codifica elas
    faces_location = face_recognition.face_locations(frame_bgr_rgb)
    faces_encoding = face_recognition.face_encodings(frame_bgr_rgb, faces_location)

    # Verifica se as faces localizadas nos vídeos são iguais as conhecidas
    for face_encoding in faces_encoding:
        name = UnknowPeople
        for people in all_people:
            #imagens de uma pessoa
            image_of_this_people = people[1]
            
            # Verifica se há match's com as imagens da pessoa usada como template
            match = (face_recognition.compare_faces(image_of_this_people, face_encoding, 0.4))
            
            #Se houver match o name da pessoa é atribuido
            if True in match:
                name = people[0]

        #Adiciona o nome da lista de nomes associado com cada face
        Recognized_people.append(name)
                
    #   Associa o nome a pessoa na imagem
    for name, (top, right, bottom, left) in zip(Recognized_people, faces_location):
        top, right, bottom, left = top*4, right*4, bottom*4, left*4

        #Verde se reconhece, Vermelho se não reconhece
        if name is UnknowPeople:
            color = (0, 0, 255)
        else:
            color = (0, 255, 0)

        # Desenha um retângulo ao entorno da face rotulado com o nome do indivíduo
        cv2.rectangle(frame, (left - 2, top), (right, bottom), color)
        cv2.rectangle(frame, (left - 2, bottom - 12), (right, bottom+6), color, cv2.FILLED)
        cv2.putText(frame, name, (left, bottom), cv2.FONT_HERSHEY_PLAIN , 1.0, (0, 0, 0), 1 )
        

    cv2.imshow("frame", frame)
    Recognized_people.clear()
    # cv2.waitKey(33)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyWindow("frame")

  





