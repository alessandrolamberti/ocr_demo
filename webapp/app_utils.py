import streamlit as st 
import cv2
from ocr.text_reader import OCR_Reader

def demo(gpu):
    img = cv2.imread("/home/alessandro/ai/ocr_demo/tests/test_1.png")
    image = img.copy()

    modified, text, boxes = OCR_Reader(gpu=gpu).read_text(img)

    return image, modified, text, boxes


