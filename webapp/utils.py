import streamlit as st 
import numpy as np
import cv2
from ocr.text_reader import OCR_Reader

def demo():
    img = cv2.imread("/home/alessandro/ai/ocr_demo/tests/test_1.png")
    image = img.copy()

    modified, text = OCR_Reader().read_text(img)

    return image, modified, text


