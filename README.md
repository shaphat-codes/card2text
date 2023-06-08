# PROJECT

**Name**: card2text

**Author**: Jehoshaphat Tatiglo 


# DESCRIPTION

An API service that allows you to get details from ID cards in json format. With card2text, you can upload single or multiple images to an API and get a json response of the card details.


# PURPOSE

Many businesses/companies require their users to submit ID cards as part of their KYC requirements. This is done in order to compare and confirm the details from the card with the details entered during registration. Sometimes  you would want to keep a text based copy of the card details rather than images.

Having to manually cross check each and every card with the user's data can be very stressful and unproductive. Card2text aims at taking that workload.


# TECHNOLOGIES AND DEPENDENCIES USED

**Programming languages**

1. Python 
2. Javascript

**Optical Character Recognition** 

_Tesseract OCR_: I tested three different OCRs when building the project - keras_ocr, easyocr and tesseract ocr. After careful analysis, I decided to go with tesseract because it was relatively faster compared with the other two.

**Frameworks and others**

1. Django(for API development)
2. Opencv(for computer vision)
3. Reactjs(frontend development)
4. Docker(containerization)
5. Render(for hosting)


# PROCESSES


## Stage 1

An image is accepted through the API


## Stage 2

**Rotation check**

The orientation of the image is checked to see if it is in the right rotation. The image is corrected accordingly

_Approach:_

A lateral and landscape image is what the algorithm expects. In situations where this is not the case, the images are rotated through a series of angles(90 clockwise, 90 anticlockwise and 180) until the preferred rotation is achieved.

**Background noise and orientation**

Users sometimes submit images with background noise that can affect text extraction. In this case, the image goes through a series of thresholding in order to crop out the region of interest.

_Approach:_

- Thresholding is applied on the image to bring out its foreground.
- Rectangular boxes are drawn around the image from the above step.
- The rectangle with the greatest perimeter becomes the area of interest.
- The dimension of the area of interest is taken and mapped unto the original image to obtain a suitable image for text extraction. 

**Dimension check**

Images must have specific dimensions. At this stage, the dimensions of images are corrected.


# Stage 3 

- Crop out the text based part of image(this is done to reduce background noise)
- Demarcate image into smaller sections(this is done to improve accuracy of extraction)
- Pass the various demarcations through tesseract OCR
- Clean the text received(results from the OCR often contain unwanted characters)
- Return json response of the result
