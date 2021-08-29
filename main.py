import numpy as np
import cv2 
import argparse
from PIL import Image
import time
import os

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
    output_dir = "output/"
    experiment_id = str(time.strftime("%Y-%m-%d_%H-%M-%S"))

    image = cv2.imread(args.img_path)
    reader = OCR_Reader(gpu=args.gpu)

    image, text, boxes = reader.read_text(image)

    if not os.path.exists(output_dir + experiment_id):
        os.makedirs(output_dir + experiment_id)
        
    with open(output_dir + experiment_id + '/text' + '.txt', 'w') as f:
        f.write(f"Detected text - experiment id: {experiment_id}\n")
        for line in text:
            f.write(f"\n{line}")

    with open(output_dir + experiment_id + '/boxes' + '.txt', 'w') as f: 
        f.write(f"Detected boxes - experiment id: {experiment_id}\n")
        for box in boxes:
            f.write(f"\n{box}")

    cv2.imwrite(output_dir + experiment_id + '/output.png', image)


    print("Experiment finished!")
    cv2.imshow("image", image)
    cv2.waitKey(0)


if __name__ == "__main__":
    args = parse_args()

    main(args)