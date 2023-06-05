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
from .non_standard_image_extraction import initialize_editting
from . image_rotation import rotate_image


# Create your views here.
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

@api_view(['POST'])
def UploadCard(request):
            
            if request.method == "POST":
                    serializer = CardSerializer(data=request.data)

            if serializer.is_valid():
                    image_url = serializer.validated_data["url"]

                    def url_to_image(image_url):
                        resp = urllib.request.urlopen(image_url)
                        image = np.asarray(bytearray(resp.read()), dtype="uint8")
                        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                        return image
            accepted_image = url_to_image(image_url)
            

            response = rotate_image(accepted_image)
            if response == False:
                response_i = initialize_editting(accepted_image)
                return Response(response_i)
            
            else:
                try:
                       
                    return Response(response)
                except Exception as e:
                      return Response({"message": "fail", "code":500})
                   


