import streamlit as st 
import numpy as np
from PIL import Image
import tempfile
import cv2

from ocr.text_reader import OCR_Reader
from webapp.app_utils import demo
from webapp.pages import Page, Pages_View

st.set_page_config(page_title="OCR Demo WebApp - Alessandro Lamberti", layout="wide")

class OCR_App_Page(Page):
    def __init__(self):
        Page.__init__(self, "OCR App")
        st.sidebar.subheader("Parameters:")
        gpu = st.sidebar.checkbox("Enable GPU usage")
        batch_size = st.sidebar.slider("Batch size", 1, 10, 1)
        st.sidebar.write("batch_size>1 will make EasyOCR faster but use more memory")
        text_threshold = st.sidebar.slider("Text threshold", 0.1, 1.0, 0.7)
        st.sidebar.write("Text confidence threshold")
        self.reader = OCR_Reader(gpu=gpu)
    
    def dispatch(self):
        st.header("OCR App")
        option = st.sidebar.radio('What do you prefer?', options = ['Custom images', 'Demo', 'Custom video'])

        if option == 'Custom images':
            content = st.sidebar.file_uploader("Choose a content image", type=['png', 'jpg', 'jpeg'])
            if content:
                image = np.asarray(Image.open(content).convert('RGB'))
                try:
                    image, text = self.reader.read_text(image)
                    st.image(image)
                    st.subheader("Extracted text")
                    for line in text:
                        st.text(line)    
                except:
                    st.error("I'm sorry, something went wrong. Maybe no text was detected, try another image.")        
            else:
                st.warning("Please choose a valid image file")
        
        elif option == 'Demo':
            image, modified, text = demo()
            st.image([image, modified], caption=['Original image', "Extracted text"])
            st.subheader("Extracted text")
            for line in text:
                st.text(line)        

        elif option == 'Custom video':
            content = st.sidebar.file_uploader("Choose a video", type=['mp4', 'mkv', 'avi'])
            if content:
                tfile = tempfile.NamedTemporaryFile(delete=True) 
                tfile.write(content.read())
                vf = cv2.VideoCapture(tfile.name)
                st.subheader("Extracted text")

                stframe = st.empty()
                index = 0

                while vf.isOpened():
                    ret, frame = vf.read()
                    if not ret:
                        st.warning("Can't receive frame (stream end?). Exiting ...")
                        break
                    if index % 100 == 0:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        # normalize
                        gray = gray.astype(np.float32) / 255.0                    
                        try:
                            image, text = self.reader.read_video(gray)
                            stframe.image(image)
                            st.write(text)
                        except:
                            continue
                    index += 1



pages_view = Pages_View()
pages_view.add_page(OCR_App_Page())


def main(page_name):
    pages_view.get_page_by_name(page_name).dispatch()


if __name__ == "__main__":
    
    page_name = st.sidebar.selectbox("Select page:", options=pages_view.get_pages_name())
    main(page_name)