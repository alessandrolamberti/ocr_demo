import easyocr 
import cv2 
import numpy as np

class OCR_Reader():
    """
    Initialize the reader with an image.
    
    Parameters:
     -image: numpy array
     -languages: list of languages to use for OCR, default is ['en', 'it']
    """

    def __init__(self, image, languages=['en', 'it']):
        self.reader = easyocr.Reader(languages)
        self.image = image

    def read_text(self):
        result = self.reader.readtext(self.image)
        text = []
        for detection in result:
            top_left = tuple(detection[0][0])
            bottom_right = tuple(detection[0][2])
            text.append(detection[1])
            img = cv2.rectangle(self.image,top_left,bottom_right,(0,255,0),2)
        return img, text

    

