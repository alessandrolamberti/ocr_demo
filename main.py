import numpy as np
import cv2 
import argparse
from PIL import Image

from ocr.text_reader import OCR_Reader

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--img_path", help="path of the image",
        required=True, type=str)
    parser.add_argument(
        "--gpu", help="enable or not gpu usage", default=False, type=bool)

    return parser.parse_args()


def main(args):
    image = np.asarray(Image.open(args.img_path))
    reader = OCR_Reader(image)

    image, text = reader.read_text()

    print('*'*80)
    print('Text detected:\n\n')

    for line in text:
        print(line)
    print('*'*80)

    cv2.imshow("image", image)
    cv2.waitKey(0)


if __name__ == "__main__":
    args = parse_args()

    main(args)