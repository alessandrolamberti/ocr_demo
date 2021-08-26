import streamlit as st 
import numpy as np
import easyocr
from PIL import Image

from ocr.text_reader import OCR_Reader
from webapp.utils import demo
from webapp.pages import Page, Pages_View

st.set_page_config(page_title="OCR Demo WebApp - Alessandro Lamberti", layout="wide")

class Welcome_Page(Page):
    def __init__(self):
        Page.__init__(self, "Welcome")
    
    def dispatch(self):
        st.title("OCR Demo Webapp")
        st.header("Welcome to the Fire Detection demo app!")
        st.markdown('By <a href="https://www.linkedin.com/in/alessandro-lamberti/" target="_blank">Alessandro Lamberti</a>' , unsafe_allow_html=True)
        st.markdown("### Please select the page you want to navigate to.")
        st.markdown("""
        - App: try the app, you can choose your own images, or try the pre-loaded demo.
                    """)


class OCR_App_Page(Page):
    def __init__(self):
        Page.__init__(self, "OCR App")
    
    def dispatch(self):
        st.header("OCR App")
        option = st.sidebar.radio('What do you prefer?', options = ['Custom images', 'Demo'])

        if option == 'Custom images':
            content = st.sidebar.file_uploader("Choose a content image", type=['png', 'jpg', 'jpeg'])
            if content:
                image = np.asarray(Image.open(content).convert('RGB'))
                image, text = OCR_Reader(image).read_text()
                st.image(image)
                st.subheader("Extracted text")
                for line in text:
                    st.text(line)            
            else:
                st.warning("Please choose a valid image file")
        
        elif option == 'Demo':
            image, modified, text = demo()
            st.image([image, modified], caption=['Original image', "Extracted text"])
            st.subheader("Extracted text")
            for line in text:
                st.text(line)            


pages_view = Pages_View()
pages_view.add_page(Welcome_Page())
pages_view.add_page(OCR_App_Page())


def main(page_name):
    pages_view.get_page_by_name(page_name).dispatch()


if __name__ == "__main__":
    
    page_name = st.sidebar.selectbox("Select page:", options=pages_view.get_pages_name())
    main(page_name)