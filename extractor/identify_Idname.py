import argparse
import cv2
from PIL import Image
import pytesseract
import numpy as np
from pytesseract import Output


def rotation_check(image_final):
                pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
                image_final = cv2.resize(image_final, (751, 490))
                idname_crop = cv2.cvtColor(image_final, cv2.COLOR_BGR2GRAY)
                idname_crop = cv2.convertScaleAbs(idname_crop, alpha=0.4, beta=7)
                idname = idname_crop[15:59,125:325]
                custom_config = r'-l eng --oem 3 --psm 6'
                idname_text = pytesseract.image_to_string(idname,config=custom_config)
                if any(item in idname_text for item in ['ECO', 'WAS', 'COW']):
    
                    return [True, idname]
                else:
                    return [False, idname]
                

