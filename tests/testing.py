import easyocr
import cv2


reader = easyocr.Reader(lang_list=['en'])


result = reader.readtext("/home/alessandro/ai/ocr_demo/tests/test_1.png")
img = cv2.imread("/home/alessandro/ai/ocr_demo/tests/test_1.png")

for detection in result: 
    top_left = tuple(detection[0][0])
    bottom_right = tuple(detection[0][2])
    text = detection[1]
    img = cv2.rectangle(img,top_left,bottom_right,(0,255,0),3)
    print(text)
    
cv2.imshow("image",img)
cv2.waitKey(0)