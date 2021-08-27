import easyocr 
import cv2 

class OCR_Reader():
    """
    Initialize the reader with an image.
    
    Parameters:
     -image/frame: numpy array
     -languages: list of languages to use for OCR, default is ['en', 'it']
    """

    def __init__(self, gpu=True, languages=['en', 'it']):
        self.reader = easyocr.Reader(languages, gpu=gpu)

    def read_text(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        result = self.reader.readtext(gray)
        text = []
        boxes = []
        for detection in result:
            top_left = tuple(detection[0][0])
            bottom_right = tuple(detection[0][2])
            text.append(detection[1])
            boxes.append(f"Box: {top_left + bottom_right}")
            try:
                image = cv2.rectangle(image,top_left,bottom_right,(0,255,0),2)
            except:
                continue
        return image, text, boxes

    def read_video(self, frame):
        return self.reader.readtext(frame)