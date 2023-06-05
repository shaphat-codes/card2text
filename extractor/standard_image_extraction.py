from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from PIL import Image
import pytesseract
import cv2
import numpy as np
from pytesseract import Output
import os
import re
import urllib.request



def standard_image(image):
                    x =180
                    y = 100
                    h = 400
                    w= 320

                    # storing the original image in a new variable
                    raw_image = image

                    #cropping the original image for extraction
                    cropped_image = image[y:y+h,x:x+w]
                    #### extracting the surname
                    def extract_surname():
                        surname_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                        surname_crop = cv2.convertScaleAbs(surname_crop, alpha=1.4, beta=7)
                        surname = surname_crop[18:65,10:400]
                        cv2.waitKey(0)
                        custom_config = r'-l eng --oem 3 --psm 6'
                        surname_text = pytesseract.image_to_string(surname,config=custom_config)
                        surname_text = surname_text.split("\n")[1]
                        surname_text = re.sub(r'[^\w\s]', '', surname_text)
                        return surname_text
                    
                    ### extracting the firstname
                    def extract_firstname():
                        firstname_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                        firstname_crop = cv2.convertScaleAbs(firstname_crop, alpha=1.6, beta=7)
                        firstname = firstname_crop[51:105,10:400]
                        custom_config = r'-l eng --oem 3 --psm 6'
                        firstname_text = pytesseract.image_to_string(firstname,config=custom_config)
                        firstname_text = firstname_text.split("\n")[1]
                        firstname_text = re.sub(r'[^\w\s]', '', firstname_text)
                        return firstname_text

                    ### extract sex
                    def extract_sex():
                        sex_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                        sex_crop = cv2.convertScaleAbs(sex_crop, alpha=0.4, beta=7)
                        sex = sex_crop[121:164,220:390]
                        #cv2.imshow("sex", sex)
                        #cv2.imwrite("sex_final.jpg", sex)
                        cv2.waitKey(0)
                        custom_config = r'-l eng --oem 3 --psm 6'
                        sex_text = pytesseract.image_to_string(sex,config=custom_config)
                        sex_text = sex_text.split("\n")[1][-1]
                        sex_text = re.sub(r'[^\w\s]', '', sex_text)
                        return sex_text
                    
                    ### extract Date of Birth
                    try:
                         
                        def extract_dob():

                            dob_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                            dob_brightness = np.average(dob_crop)

                            # checking if there is extra brightness
                            if dob_brightness >= 160:
                                dob_crop = cv2.convertScaleAbs(dob_crop, alpha=0.6, beta=5)
                            else:
                                dob_crop = cv2.convertScaleAbs(dob_crop, alpha=1.6, beta=5)
                            dob = dob_crop[156:210,10:330]
                            custom_config = r'-l eng --oem 3 --psm 6'
                            dob_text = pytesseract.image_to_string(dob,config=custom_config)
                            dob_text = re.search('\d{2}/\d{2}/\d{4}', dob_text)
                            if dob_text == None:
                                dob_text = "Null"
                                return dob_text
                            else:
                                
                                dob_text = dob_text.group(0)
                                return dob_text
                            
                            return dob_text
                    except Exception as e:
                         return "there was an error"
                    ### extracting ID number
                    def extract_idnumber():
                        idnumber_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                        idnumber_brightness = np.average(idnumber_crop)

                        # checking if theres is extra brightness
                        if idnumber_brightness > 168 and idnumber_brightness < 177:


                            idnumber_crop = cv2.convertScaleAbs(idnumber_crop, alpha=0.9, beta=10)
                        else:
                            idnumber_crop = cv2.convertScaleAbs(idnumber_crop, alpha=1.9, beta=10)

                        idnumber = idnumber_crop[200:250,10:330]
                        custom_config = r'-l eng --oem 3 --psm 6'
                        idnumber_text = pytesseract.image_to_string(idnumber,config=custom_config)
                        idnumber_text = idnumber_text.split("\n")[1]
                        idnumber_text = f"{idnumber_text[:16]}"
                        idnumber_text = idnumber_text.replace("|", "")
                        #idnumber_text = re.sub(r'[^\w\s]', '', idnumber_text)
                        
                        return idnumber_text

                    ### extracting height
                    def extract_height():
                        #using original cropped image since position of height can vary
                        height_crop = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
                        height_crop = cv2.convertScaleAbs(height_crop, alpha=1.6, beta=7)
                        height_crop = height_crop[300:350,390:550]
                        custom_config = r'-l eng --oem 3 --psm 6'
                        height_crop = pytesseract.image_to_string(height_crop,config=custom_config)
                        height_text = height_crop.split("\n")[1]
                        height_text = height_text[-4:]
                        return height_text
                    
                    # extracting the document number
                    def extract_documentnumber():
                        documentnumber_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                        documentnumber_crop = cv2.convertScaleAbs(documentnumber_crop, alpha=2.1, beta=10)
                        documentnumber = documentnumber_crop[235:290,10:330]
                        custom_config = r'-l eng --oem 3 --psm 6'
                        document_number_text = pytesseract.image_to_string(documentnumber,config=custom_config)
                        document_number_text = document_number_text.split("\n")[1]
                        return document_number_text

                    # extracting place of birth
                    def extract_place_of_birth():
                        place_of_birth_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                        place_of_birth_crop = cv2.convertScaleAbs(place_of_birth_crop, alpha=1.5, beta=7)
                        place_of_birth = place_of_birth_crop[270:330,10:330]
                        custom_config = r'-l eng --oem 3 --psm 6'
                        place_of_birth_text = pytesseract.image_to_string(place_of_birth,config=custom_config)
                        place_of_birth_text = place_of_birth_text.split("\n")[1]
                        return place_of_birth_text

                    # extracting date of issunace
                    try:
                        def extract_date_of_issuance():
                            date_of_issuance_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                            date_of_issuance_crop = cv2.convertScaleAbs(date_of_issuance_crop, alpha=1.5, beta=7)
                            date_of_issuance = date_of_issuance_crop[312:360,10:330]
                            custom_config = r'-l eng --oem 3 --psm 6'
                            date_of_issuance_text = pytesseract.image_to_string(date_of_issuance,config=custom_config)
                            date_of_issuance_text = re.search('\d{2}/\d{2}/\d{4}', date_of_issuance_text)
                            
                            if date_of_issuance_text == None:
                                    date_of_issuance_text = "Null"
                                    return date_of_issuance_text
                            else:
                                    
                                    date_of_issuance_text = date_of_issuance_text.group(0)
                                    return date_of_issuance_text
                    except Exception as e:
                         return "error here"

                    # extracting the date of expiry
                    try:
                         
                        def extract_date_of_expiry():
                            date_of_expiry_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                            date_of_expiry_crop = cv2.convertScaleAbs(date_of_expiry_crop, alpha=1.5, beta=10)
                            date_of_expiry = date_of_expiry_crop[345:415,1:330]
                            custom_config = r'-l eng --oem 3 --psm 6' 
                            date_of_expiry_text = pytesseract.image_to_string(date_of_expiry,config=custom_config)
                            date_of_expiry_text = re.search('\d{2}/\d{2}/\d{4}', date_of_expiry_text)
                            if date_of_expiry_text == None:
                                    date_of_expiry_text = "Null"
                                    return date_of_expiry_text
                            else:
                                    
                                    date_of_expiry_text = date_of_expiry_text.group(0)
                                    return date_of_expiry_text
                            
                    except Exception as e:
                         return "error here"
                

                    ghana_card_data = {
                            "surname": str(extract_surname()),
                            "firstname": str(extract_firstname()),
                            "sex": str(extract_sex()),
                            "nationality": "Ghanaian",
                            "date_of_birth": str(extract_dob()),
                            "height": str(extract_height()),
                            "id_number": extract_idnumber(),
                            "document_number": str(extract_documentnumber()),
                            "place_of_birth": str(extract_place_of_birth()),
                            "date_of_issuance": str(extract_date_of_issuance()),
                            "date_of_expiry": str(extract_date_of_expiry())
                        }
                    values = []
                    for value in ghana_card_data.values():
                             values.append(value) 
                    try:
                        if values.count("Null") > 1:
                            return {"message": "extraction unsuccessful"}
                        else:
                             
                            return ghana_card_data

                    except Exception as e:
                        return {"error": "couldn't get response"}
