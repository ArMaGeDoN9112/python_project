"""

Face recognition module

"""

import cv2
import numpy as np

from keras.models import load_model
from keras.preprocessing.image import img_to_array

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
classifier = load_model('model.h5')

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy','Neutral', 'Sad', 'Surprise']


class VideoCamera:
    def __init__(self, file_name):
        self.cap = cv2.VideoCapture(file_name)

    def get_video(self):
        ret, frame = self.cap.read()

        if not ret:
            return None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            roi_gray = gray[y:y+h,x:x+w]
            roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray])!=0:
                roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi,axis=0)

                prediction = classifier.predict(roi)[0]
                label=emotion_labels[prediction.argmax()]
                label_position = (x,y)
                cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            else:
                cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        frame = cv2.resize(frame, (500, 300))
        _, img = cv2.imencode(".jpg", frame)

        return img.tobytes()
