import cv2
import os

cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

# Replace "account_number" with the actual account number of the user
Name = input("Enter your name: ")

# Create a folder with the name of the account number if it doesn't already exist
if not os.path.exists("pictures/" + Name):
    os.makedirs("pictures/" + Name)

count = 0
while count < 200:
    # Capture frame-by-frame
    ret, frames = video_capture.read()
    #print(ret)

    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces and save them as images
    for (x, y, w, h) in faces:
        cv2.rectangle(frames, (x, y), (x+w, y+h), (0, 255, 0), 2)
        count += 1
        cv2.imwrite("pictures/" + Name + "/face" + str(count) + ".jpg", frames[y:y+h, x:x+w])

    # Display the resulting frame
    cv2.imshow('Video', frames)
    k=cv2.waitKey(1) & 0xFF

    if k == ord('q') :#ord('q')
        break

video_capture.release()
cv2.destroyAllWindows()
