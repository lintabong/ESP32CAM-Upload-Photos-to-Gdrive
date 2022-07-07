from serial             import Serial
from time               import sleep
from pydrive.drive      import GoogleDrive
from pydrive.auth       import GoogleAuth
import requests
import datetime
import cv2
import urllib.request
import numpy

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
folder = "1KcqDaI8nsAIvkBdoou3QF3ATwBSyAC8v"

ser = Serial('COM3', 115200, timeout=0.05)

url = 'http://192.168.1.15/saved-photo'

def datepicker():
    timenow = datetime.datetime.now()
    ye   = str(timenow.year)
    mo   = str(timenow.month)
    da   = str(timenow.day)

    ho   = str(timenow.hour)
    mi   = str(timenow.minute)
    se   = str(timenow.second)

    return ye, mo, da, ho, mi, se

while True:
    img_resp = urllib.request.urlopen(url)
    imgnp = numpy.array(bytearray(img_resp.read()), dtype = numpy.uint8)
    frame = cv2.imdecode(imgnp, -1)

    b = str(ser.readline()).replace('b', '').replace('\\r\\n', '').replace('\'', '')
    if len(b) != 0:
        print('response 200', b)
        n = datepicker()
        nall = ''
        for i in range(len(n)):
            nall = nall + n[i] + '_'

        response = requests.get(url)
        if response.status_code == 200:
            with open('resultcam\im' + nall + '.jpeg', 'wb') as f:
                f.write(response.content)

            f.close()

            f = drive.CreateFile({'parents': [{'id': folder}], 'title': 'im' + nall + '.jpeg'})
            f.SetContentFile('resultcam\im' + nall + '.jpeg')
            f.Upload()
        else:
            print(response.status_code)

    key = cv2.waitKey(5)
    if key == ord('q'):
        break

    sleep(0.5)

cv2.destroyAllWindows()
