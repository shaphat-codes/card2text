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




def further_editting(accepted_image):

    def apply_thresholding_on_image(accepted_image):
                        # convert the image to grayscale and blur it slightly
                        image_final = accepted_image
                        gray = cv2.cvtColor(image_final, cv2.COLOR_BGR2GRAY)
                        blurred = cv2.GaussianBlur(gray, (7, 7), 0)


                        # apply simple thresholding with a hardcoded threshold value
                        (T, threshInv) = cv2.threshold(blurred, 190, 200,
                            cv2.THRESH_BINARY_INV)
                        
                        thresh = cv2.threshold(threshInv,120,20,cv2.THRESH_BINARY_INV)[1]
                        # get contours
                        thresh_result = threshInv.copy()
                        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        contours = contours[0] if len(contours) == 2 else contours[1]
                        return [contours, thresh_result]
        

    contours = apply_thresholding_on_image(accepted_image)
    contours = contours[0]

    thresh_result = apply_thresholding_on_image(accepted_image)
    thresh_result = thresh_result[1]

    
    def find_desired_part_of_image(contours, thresh_result):

                            i = 0

                            # store the perimeter of each rectangle
                            perimeter_list = []

                            # store the individual rectangles
                            cropped_images = []

                            # store the dimension of each rectangle
                            dimensions = []
                            for cntr in contours:
                                x,y,w,h = cv2.boundingRect(cntr)
                                dimensions.append(cv2.boundingRect(cntr))
                                cv2.rectangle(thresh_result, (x, y), (x+w, y+h), (0, 0, 255), 2)
                                cropped_images.append(thresh_result[y:y+h, x:x+w])
                                cntr_per = cv2.arcLength(cntr, True)
                                perimeter_list.append(cntr_per)
                                
                                i += 1

                            # find the largest rectangle and store its dimensions
                            index_of_largest = perimeter_list.index(max(perimeter_list))
                            fore_dimension = dimensions[index_of_largest]
                            x_value = fore_dimension[0]
                            y_value = fore_dimension[1]
                            w_value = fore_dimension[2]
                            h_value = fore_dimension[3]

                            # map the dimensions stored unto the original image
                            editted_image = accepted_image[y_value:y_value+h_value, x_value:x_value+w_value]

                            # resize the new image
                            resize_editted = cv2.resize(editted_image, (751, 490))
                            raw_image = resize_editted
                            cropped_image = resize_editted[100:100+400,120:120+380]
                            return cropped_image, raw_image
    return find_desired_part_of_image(contours, thresh_result)
