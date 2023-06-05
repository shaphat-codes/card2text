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
from .standard_image_extraction import standard_image
from .identify_Idname import rotation_check
from . non_standard_image_extraction import initialize_editting


def rotate_image(image):

    idname_text = rotation_check(image)

    #### checking if image is already of a good orientation
    print(idname_text[0])
    if idname_text[0] == True:
        response = standard_image(image)

        return response
    
    if idname_text[0] == False:
        print("it is false")
        new_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        idname_text[0] = rotation_check(new_image)[0]
        idname_text[1] = new_image
        idname_text[1] = cv2.resize(idname_text[1], (751, 490))

    if idname_text[0] == False:
        another_new_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        idname_text[0] = rotation_check(another_new_image)[0]
        idname_text[1] = another_new_image
        idname_text[1] = cv2.resize(idname_text[1], (751, 490))

    if idname_text[0] == False:
        last_image = cv2.rotate(image, cv2.ROTATE_180)
        idname_text[0] = rotation_check(last_image)[0]
        idname_text[1] = last_image
        idname_text[1] = cv2.resize(idname_text[1], (751, 490))

    print(idname_text[0])
    if idname_text[0] == True:
        print("it is now true")
        response = standard_image(idname_text[1])

        return response
    else:
        response = initialize_editting(image)
        return response
