irom django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from . models import *
from PIL import Image
import pytesseract
import cv2
import numpy as np
from pytesseract import Output
import os
import re
import urllib.request
from . contour_detection import further_editting



def initialize_editting(image):
    cropped_image = further_editting(image)
    cropped_image = cropped_image[0]
    raw_image = further_editting(image)
    raw_image = raw_image[1]

    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

    # extracting surname
    def extract_surname():
        surname_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        surname_crop = cv2.convertScaleAbs(surname_crop, alpha=1.4, beta=7)
        surname = surname_crop[18:65,10:400]
        custom_config = r'-l eng --oem 3 --psm 6'
        surname_text = pytesseract.image_to_string(surname,config=custom_config)
        surname_text = surname_text.split("\n")[1]
        surname_text = re.sub(r'[^\w\s]', '', surname_text)
        return surname_text

    # extracting firstname
    def extract_firstname():
        firstname_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        firstname_crop = cv2.convertScaleAbs(firstname_crop, alpha=1.6, beta=7)
        firstname = firstname_crop[51:105,10:400]
        custom_config = r'-l eng --oem 3 --psm 6'
        firstname_text = pytesseract.image_to_string(firstname,config=custom_config)
        firstname_text = firstname_text.split("\n")[1]
        firstname_text = re.sub(r'[^\w\s]', '', firstname_text)
        return firstname_text

    # extracting sex
    try:

        def extract_sex():
            sex_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
            sex_crop = cv2.convertScaleAbs(sex_crop, alpha=0.4, beta=7)
            sex = sex_crop[121:164,220:390]
            custom_config = r'-l eng --oem 3 --psm 6'
            sex_text = pytesseract.image_to_string(sex,config=custom_config)
            sex_text = sex_text.split("\n")[1][-1]
            sex_text = re.sub(r'[^\w\s]', '', sex_text)
            return sex_text
    except Exception as e:
        return "error ocuured"

    # extracting date of birth
    def extract_dob():
        dob_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        dob_brightness = np.average(dob_crop)

        # checking if brightness is too high
        if dob_brightness >= 160:
            dob_crop = cv2.convertScaleAbs(dob_crop, alpha=0.6, beta=5)
        else:

            dob_crop = cv2.convertScaleAbs(dob_crop, alpha=1.6, beta=5)

        dob = dob_crop[156:210,10:330]
        custom_config = r'-l eng --oem 3 --psm 6'
        dob_text = pytesseract.image_to_string(dob,config=custom_config)
        dob_text = re.search('\d{2}/\d{2}/\d{4}', dob_text)
        dob_text = dob_text.group(0)
        return dob_text

    # extracting ID number
    def extract_idnumber():
        idnumber_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        idnumber_brightness = np.average(idnumber_crop)

        # checking if brightness is too high
        if idnumber_brightness > 168 and idnumber_brightness < 177:
        
            idnumber_crop = cv2.convertScaleAbs(idnumber_crop, alpha=0.9, beta=10)
        else:
            idnumber_crop = cv2.convertScaleAbs(idnumber_crop, alpha=1.9, beta=10)

        idnumber = idnumber_crop[200:250,10:330]
        custom_config = r'-l eng --oem 3 --psm 6'
        idnumber_text = pytesseract.image_to_string(idnumber,config=custom_config)
        idnumber_text = idnumber_text.split("\n")[1]
        idnumber_text = re.sub('[ ]', "",idnumber_text)
        idnumber_text = idnumber_text[:15]
        idnumber_text = idnumber_text.replace("|", "")
        return idnumber_text

    # extracting height
    def extract_height():
        height_crop = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
        height_crop = cv2.convertScaleAbs(height_crop, alpha=1.6, beta=7)
        height_crop = height_crop[300:350,390:550]
        custom_config = r'-l eng --oem 3 --psm 6'
        height_crop = pytesseract.image_to_string(height_crop,config=custom_config)
        height_text = height_crop.split("\n")[1]
        height_text = height_text[-4:]
        return height_text

    # extracting document number
    def extract_documentnumber():
        documentnumber_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        documentnumber_crop = cv2.convertScaleAbs(documentnumber_crop, alpha=1.9, beta=10)
        documentnumber = documentnumber_crop[235:290,10:330]
        custom_config = r'-l eng --oem 3 --psm 6'
        document_number_text = pytesseract.image_to_string(documentnumber,config=custom_config)
        document_number_text = document_number_text.split("\n")[1]
        document_number_text = re.sub('[ ]', "",document_number_text)
        return document_number_text


    # extracting place of birth
    def extract_place_of_birth():
        place_of_birth_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        place_of_birth_crop = cv2.convertScaleAbs(place_of_birth_crop, alpha=1.4, beta=7)
        place_of_birth = place_of_birth_crop[270:330,10:330]
        custom_config = r'-l eng --oem 3 --psm 6'
        place_of_birth_text = pytesseract.image_to_string(place_of_birth,config=custom_config)
        place_of_birth_text = place_of_birth_text.split("\n")[1]
        return place_of_birth_text


    # extracting date of issuance
    def extract_date_of_issuance():
        date_of_issuance_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        date_of_issuance_crop = cv2.convertScaleAbs(date_of_issuance_crop, alpha=1.2, beta=7)
        date_of_issuance = date_of_issuance_crop[312:360,10:330]
        custom_config = r'-l eng --oem 3 --psm 6'
        date_of_issuance_text = pytesseract.image_to_string(date_of_issuance,config=custom_config)
        date_of_issuance_text = re.search('\d{2}/\d{2}/\d{4}', date_of_issuance_text)
        date_of_issuance_text = date_of_issuance_text.group(0)
        return date_of_issuance_text

    # extracting date of expiry
    def extract_date_of_expiry():
        date_of_expiry_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        date_of_expiry_crop = cv2.convertScaleAbs(date_of_expiry_crop, alpha=1.5, beta=10)
        date_of_expiry = date_of_expiry_crop[345:415,1:330]
        custom_config = r'-l eng --oem 3 --psm 6' 
        date_of_expiry_text = pytesseract.image_to_string(date_of_expiry,config=custom_config)
        date_of_expiry_text = re.search('\d{2}/\d{2}/\d{4}', date_of_expiry_text)
        date_of_expiry_text = date_of_expiry_text.group(0)
        return date_of_expiry_text



    ghana_card_data = {
        "surname": str(extract_surname()),
        "firstname": str(extract_firstname()),
        "sex": str(extract_sex()),
        "nationality": "Ghanaian",
        "date_of_birth": str(extract_dob()),
        "height": str(extract_height()),
        "id_number": str(extract_idnumber()),
        "document_number": str(extract_documentnumber()),
        "place_of_birth": str(extract_place_of_birth()),
        "date_of_issuance": str(extract_date_of_issuance()),
        "date_of_expiry": str(extract_date_of_expiry())
    }
    print(ghana_card_data)
    return ghana_card_data
