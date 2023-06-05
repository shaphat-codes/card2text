irom PIL import Image
import pytesseract
import cv2
import numpy as np
from pytesseract import Output
import os
import re
from views import UploadCard


# Create your views here.
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'



x =180
y = 100
h = 400
w= 320
image_final = cv2.resize(image_final, (751, 490))
cv2.imwrite("first_crop.jpg", image_final)

            
idname_crop = cv2.cvtColor(image_final, cv2.COLOR_BGR2GRAY)
idname_crop = cv2.convertScaleAbs(idname_crop, alpha=0.4, beta=7)
idname = idname_crop[15:59,125:325]
cv2.imwrite("ecowas.jpg", idname)
custom_config = r'-l eng --oem 3 --psm 6'
idname_text = pytesseract.image_to_string(idname,config=custom_config)
print(idname_text)
