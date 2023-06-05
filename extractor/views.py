from django.shortcuts import render
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

# Create your views here.
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


@api_view(['POST'])
def UploadCard(request):
 

        if request.method == "POST":

            
            #print(text.split("\n")[1])

            serializer = CardSerializer(data=request.data)
        
            
        if serializer.is_valid():
            image_url = serializer.validated_data["url"]

            def url_to_image(image_url):
                resp = urllib.request.urlopen(image_url)
                image = np.asarray(bytearray(resp.read()), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                return image
            
            image_final = url_to_image(image_url)



            
            #img = cv2.imread(image_url)
            x =180
            y = 100
            h = 400
            w= 320
            image_final = cv2.resize(image_final, (751, 490))
            #cv2.imwrite("first_crop.jpg", image_final)

            
            idname_crop = cv2.cvtColor(image_final, cv2.COLOR_BGR2GRAY)
            idname_crop = cv2.convertScaleAbs(idname_crop, alpha=0.4, beta=7)
            idname = idname_crop[15:59,125:325]
            #cv2.imwrite("ecowas.jpg", idname)
            custom_config = r'-l eng --oem 3 --psm 6'
            idname_text = pytesseract.image_to_string(idname,config=custom_config)
            print(idname_text)
            
            if any(item in idname_text for item in ['ECO', 'WAS', 'COW']):


                cropped_image = image_final[y:y+h,x:x+w]
                #cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                #cropped_image = cv2.convertScaleAbs(cropped_image, alpha=2.5, beta=7)
                #cv2.imshow("Cropped Image",cropped_image)
                #cv2.imshow("OriginalImage",img)
                #cv2.imwrite("Cropped Image.jpg", cropped_image)
                #cv2.waitKey(0)
                
                
                pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'



                # Simply extracting text from image
                #image = Image.open("Cropped Image.jpg")

                
                surname_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                surname_crop = cv2.convertScaleAbs(surname_crop, alpha=1.4, beta=7)
                surname = surname_crop[18:65,10:400]
                #cv2.imshow("surname", surname)
                #cv2.imwrite("surname_final.jpg", surname)
                
                custom_config = r'-l eng --oem 3 --psm 6'
                surname_text = pytesseract.image_to_string(surname,config=custom_config)
                surname_text = surname_text.split("\n")[1]

                
                surname_text = re.sub('[«]', "",surname_text)
                surname_text = re.sub('[|]', "",surname_text)






                
                firstname_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                firstname_crop = cv2.convertScaleAbs(firstname_crop, alpha=1.6, beta=7)
                firstname = firstname_crop[51:105,10:400]
                #cv2.imshow("firstname", firstname)
                #cv2.imwrite("firstname_final.jpg", firstname)
                
                custom_config = r'-l eng --oem 3 --psm 6'
                firstname_text = pytesseract.image_to_string(firstname,config=custom_config)
                firstname_text = firstname_text.split("\n")[1]

                
                firstname_text = re.sub('[|]', "",firstname_text)



                sex_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                sex_crop = cv2.convertScaleAbs(sex_crop, alpha=0.4, beta=7)
                sex = sex_crop[121:164,220:390]
                #cv2.imshow("sex", sex)
                #cv2.imwrite("sex_final.jpg", sex)
                
                custom_config = r'-l eng --oem 3 --psm 6'
                sex_text = pytesseract.image_to_string(sex,config=custom_config)
                sex_text = sex_text.split("\n")[1][-1]

            



                
                dob_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
   
                dob_brightness = np.average(dob_crop)
                if dob_brightness >= 160:
                    dob_crop = cv2.convertScaleAbs(dob_crop, alpha=0.6, beta=5)
                else:

                    dob_crop = cv2.convertScaleAbs(dob_crop, alpha=1.6, beta=5)
                dob = dob_crop[156:210,10:330]
                #cv2.imshow("dob", dob)
                #cv2.imwrite("dob_final.jpg", dob)
                
                custom_config = r'-l eng --oem 3 --psm 6'
                dob_text_raw = pytesseract.image_to_string(dob,config=custom_config)
                dob_text = dob_text_raw.split("\n")[1]
                dob_text = re.search('\d{2}/\d{2}/\d{4}', dob_text)
                if dob_text is None:
                    dob_text = dob_text_raw.split("\n")[2]
                    
                    dob_text = re.search('\d{2}/\d{2}/\d{4}', dob_text)
                    dob_text = dob_text.group(0)
                else:

                    dob_text = dob_text.group(0)




                
                idnumber_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                idnumber_brightness = np.average(idnumber_crop)
                if idnumber_brightness > 168 and idnumber_brightness < 177:


                    idnumber_crop = cv2.convertScaleAbs(idnumber_crop, alpha=0.9, beta=10)
                else:
                    idnumber_crop = cv2.convertScaleAbs(idnumber_crop, alpha=1.9, beta=10)

                idnumber = idnumber_crop[200:250,10:330]
                #cv2.imshow("idnumber", idnumber)
                #cv2.imwrite("idnumber_final.jpg", idnumber)
                
                custom_config = r'-l eng --oem 3 --psm 6'
                idnumber_text = pytesseract.image_to_string(idnumber,config=custom_config)
                idnumber_text = re.findall(r'\d+', idnumber_text)
                idnumber_text = f"GHA-{idnumber_text[0]}-{idnumber_text[1]}"
                


                
                documentnumber_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

                documentnumber_crop = cv2.convertScaleAbs(documentnumber_crop, alpha=1.9, beta=10)
                documentnumber = documentnumber_crop[235:290,10:330]
                #cv2.imshow("documentnumber", documentnumber)
                #cv2.imwrite("documentnumber_final.jpg", documentnumber)
                
                custom_config = r'-l eng --oem 3 --psm 6'
                document_number_text = pytesseract.image_to_string(documentnumber,config=custom_config)
                print(document_number_text)
                document_number_text = document_number_text.split("\n")[1]

                



                
                place_of_birth_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

                place_of_birth_crop = cv2.convertScaleAbs(place_of_birth_crop, alpha=1.4, beta=7)
                place_of_birth = place_of_birth_crop[270:330,10:330]
                #cv2.imshow("documentnumber", place_of_birth)
                #cv2.imwrite("place_of_birth_final.jpg", place_of_birth)
                

                custom_config = r'-l eng --oem 3 --psm 6'
                place_of_birth_text = pytesseract.image_to_string(place_of_birth,config=custom_config)
                place_of_birth_text = place_of_birth_text.split("\n")[1]



                
                date_of_issuance_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

                date_of_issuance_crop = cv2.convertScaleAbs(date_of_issuance_crop, alpha=1.5, beta=7)
                date_of_issuance = date_of_issuance_crop[312:360,10:330]
                #cv2.imshow("documentnumber", date_of_issuance)
                #cv2.imwrite("date_of_issuance_final.jpg", date_of_issuance)
                

                custom_config = r'-l eng --oem 3 --psm 6'
                date_of_issuance_text = pytesseract.image_to_string(date_of_issuance,config=custom_config)
                
                
                date_of_issuance_text = re.search('\d{2}/\d{2}/\d{4}', date_of_issuance_text)
                date_of_issuance_text = date_of_issuance_text.group(0)




                
                date_of_expiry_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

                date_of_expiry_crop = cv2.convertScaleAbs(date_of_expiry_crop, alpha=1.5, beta=10)
                date_of_expiry = date_of_expiry_crop[345:415,1:330]
                #cv2.imshow("expiry date", date_of_expiry)
                #cv2.imwrite("date_of_expiry_final.jpg", date_of_expiry)
                

                custom_config = r'-l eng --oem 3 --psm 6' 
                date_of_expiry_text = pytesseract.image_to_string(date_of_expiry,config=custom_config)
                date_of_expiry_text = re.search('\d{2}/\d{2}/\d{4}', date_of_expiry_text)
                date_of_expiry_text = date_of_expiry_text.group(0)



                ghana_card_data = {
                        "surname": surname_text,
                        "firstname": firstname_text,
                        "sex": sex_text,
                        "nationality": "Ghanaian",
                        "date_of_birth": dob_text,
                        "id_number": idnumber_text,
                        "document_number": document_number_text,
                        "place_of_birth": place_of_birth_text,
                        "date_of_issuance": date_of_issuance_text,
                        "date_of_expiry": date_of_expiry_text
                    }
                
            else:
                image_final = url_to_image(image_url)
                # load the image and display it
                # convert the image to grayscale and blur it slightly
                gray = cv2.cvtColor(image_final, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (7, 7), 0)


                # apply simple thresholding with a hardcoded threshold value
                (T, threshInv) = cv2.threshold(blurred, 190, 200,
                    cv2.THRESH_BINARY_INV)
                
                
                img = threshInv

                #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

                # threshold
                thresh = cv2.threshold(img,120,20,cv2.THRESH_BINARY_INV)[1]


                # get contours
                result = img.copy()
                contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours = contours[0] if len(contours) == 2 else contours[1]


                i = 0
                perimeter_list = []
                cropped_images = []
                dimensions = []
                for cntr in contours:
                    x,y,w,h = cv2.boundingRect(cntr)
                    dimensions.append(cv2.boundingRect(cntr))
                    cv2.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cropped_images.append(result[y:y+h, x:x+w])
                    cntr_per = cv2.arcLength(cntr, True)
                    perimeter_list.append(cntr_per)
                    
                    i += 1




                index_of_largest = perimeter_list.index(max(perimeter_list))
                fore_dimension = dimensions[index_of_largest]
                x_value = fore_dimension[0]
                y_value = fore_dimension[1]
                w_value = fore_dimension[2]
                h_value = fore_dimension[3]



                editted_image = image_final[y_value:y_value+h_value, x_value:x_value+w_value]

                resize_editted = cv2.resize(editted_image, (751, 490))

                #cv2.imwrite("final image.jpg", resize_editted)
                


                

                cropped_image = resize_editted[100:100+400,120:120+380]
                #cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                #cropped_image = cv2.convertScaleAbs(cropped_image, alpha=2.5, beta=7)
                #cv2.imshow("Cropped Image",cropped_image)
                #cv2.imshow("OriginalImage",img)
                #cv2.imwrite("Cropped Image.jpg", cropped_image)
                #cv2.waitKey(0)
                
                
                pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'



                # Simply extracting text from image
                #image = Image.open("Cropped Image.jpg")

                
                surname_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                surname_crop = cv2.convertScaleAbs(surname_crop, alpha=1.4, beta=7)
                surname = surname_crop[18:65,10:400]
                #cv2.imshow("surname", surname)
                #cv2.imwrite("surname_final.jpg", surname)
                
                custom_config = r'-l eng --oem 3 --psm 6'
                surname_text = pytesseract.image_to_string(surname,config=custom_config)
                surname_text = surname_text.split("\n")[1]

                
                surname_text = re.sub('[«]', "",surname_text)
                surname_text = re.sub('[|]', "",surname_text)






                
                firstname_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                firstname_crop = cv2.convertScaleAbs(firstname_crop, alpha=1.6, beta=7)
                firstname = firstname_crop[51:105,10:400]
                #cv2.imshow("firstname", firstname)
                #cv2.imwrite("firstname_final.jpg", firstname)
                
                custom_config = r'-l eng --oem 3 --psm 6'
                firstname_text = pytesseract.image_to_string(firstname,config=custom_config)
                firstname_text = firstname_text.split("\n")[1]

                
                firstname_text = re.sub('[|]', "",firstname_text)



                sex_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                sex_crop = cv2.convertScaleAbs(sex_crop, alpha=0.4, beta=7)
                sex = sex_crop[121:164,220:390]
                #cv2.imshow("sex", sex)
                #cv2.imwrite("sex_final.jpg", sex)
                
                custom_config = r'-l eng --oem 3 --psm 6'
                sex_text = pytesseract.image_to_string(sex,config=custom_config)
                sex_text = sex_text.split("\n")[1][-1]

            



                
                dob_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
   
                dob_brightness = np.average(dob_crop)
                if dob_brightness >= 160:
                    dob_crop = cv2.convertScaleAbs(dob_crop, alpha=0.6, beta=5)
                else:

                    dob_crop = cv2.convertScaleAbs(dob_crop, alpha=1.6, beta=5)
                dob = dob_crop[156:210,10:330]
                #cv2.imshow("dob", dob)
                #cv2.imwrite("dob_final.jpg", dob)
                
                custom_config = r'-l eng --oem 3 --psm 6'
                dob_text = pytesseract.image_to_string(dob,config=custom_config)
                
                dob_text = re.search('\d{2}/\d{2}/\d{4}', dob_text)
                dob_text = dob_text.group(0)

                
                idnumber_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                idnumber_brightness = np.average(idnumber_crop)
                print(f"brightness is {idnumber_brightness}")
                if idnumber_brightness > 168 and idnumber_brightness < 177:
                
                    idnumber_crop = cv2.convertScaleAbs(idnumber_crop, alpha=0.7, beta=10)
                else:
                    idnumber_crop = cv2.convertScaleAbs(idnumber_crop, alpha=1.9, beta=10)

                idnumber = idnumber_crop[200:250,10:330]
                #cv2.imshow("idnumber", idnumber)
                #cv2.imwrite("idnumber_final.jpg", idnumber)
                
                custom_config = r'-l eng --oem 3 --psm 6'
                idnumber_text = pytesseract.image_to_string(idnumber,config=custom_config)
                print(idnumber_text)
                idnumber_text = re.findall(r'\d+', idnumber_text)
                extra_text = ""
                if len(idnumber_text) > 2:
                    extra_text = idnumber_text[-3]
                
                idnumber_text = f"GHA-{extra_text}{idnumber_text[0]}-{idnumber_text[1]}"
                


                
                documentnumber_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

                documentnumber_crop = cv2.convertScaleAbs(documentnumber_crop, alpha=1.9, beta=10)
                documentnumber = documentnumber_crop[235:290,10:330]
                #cv2.imshow("documentnumber", documentnumber)
                #cv2.imwrite("documentnumber_final.jpg", documentnumber)
                
                custom_config = r'-l eng --oem 3 --psm 6'
                document_number_text = pytesseract.image_to_string(documentnumber,config=custom_config)
                print(document_number_text)
                document_number_text = document_number_text.split("\n")[1]

                



                
                place_of_birth_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

                place_of_birth_crop = cv2.convertScaleAbs(place_of_birth_crop, alpha=1.4, beta=7)
                place_of_birth = place_of_birth_crop[270:330,10:330]
                #cv2.imshow("documentnumber", place_of_birth)
                #cv2.imwrite("place_of_birth_final.jpg", place_of_birth)
                

                custom_config = r'-l eng --oem 3 --psm 6'
                place_of_birth_text = pytesseract.image_to_string(place_of_birth,config=custom_config)
                place_of_birth_text = place_of_birth_text.split("\n")[1]



                
                date_of_issuance_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

                date_of_issuance_crop = cv2.convertScaleAbs(date_of_issuance_crop, alpha=1.5, beta=7)
                date_of_issuance = date_of_issuance_crop[312:360,10:330]
                #cv2.imshow("documentnumber", date_of_issuance)
                #cv2.imwrite("date_of_issuance_final.jpg", date_of_issuance)
                

                custom_config = r'-l eng --oem 3 --psm 6'
                date_of_issuance_text = pytesseract.image_to_string(date_of_issuance,config=custom_config)
                
                
                date_of_issuance_text = re.search('\d{2}/\d{2}/\d{4}', date_of_issuance_text)
                date_of_issuance_text = date_of_issuance_text.group(0)




                
                date_of_expiry_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

                date_of_expiry_crop = cv2.convertScaleAbs(date_of_expiry_crop, alpha=1.5, beta=10)
                date_of_expiry = date_of_expiry_crop[345:415,1:330]
                #cv2.imshow("expiry date", date_of_expiry)
                #cv2.imwrite("date_of_expiry_final.jpg", date_of_expiry)
                

                custom_config = r'-l eng --oem 3 --psm 6' 
                date_of_expiry_text = pytesseract.image_to_string(date_of_expiry,config=custom_config)
                date_of_expiry_text = re.search('\d{2}/\d{2}/\d{4}', date_of_expiry_text)
                date_of_expiry_text = date_of_expiry_text.group(0)



                ghana_card_data = {
                        "surname": surname_text,
                        "firstname": firstname_text,
                        "sex": sex_text,
                        "nationality": "Ghanaian",
                        "date_of_birth": dob_text,
                        "id_number": idnumber_text,
                        "document_number": document_number_text,
                        "place_of_birth": place_of_birth_text,
                        "date_of_issuance": date_of_issuance_text,
                        "date_of_expiry": date_of_expiry_text
                    }
                
                
                print(ghana_card_data)
            


        
                
            serializer.save()
            

        return Response(ghana_card_data)
