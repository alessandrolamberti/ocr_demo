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
        "--video_path", help="path of the image",
        required=True, type=str)
    parser.add_argument(
        "--gpu", help="enable or not gpu usage", default=False, type=bool)

    return parser.parse_args()


def main(args):
    output_dir = "output/"
    experiment_id = str(time.strftime("%Y-%m-%d_%H-%M-%S"))

    video = cv2.VideoCapture(args.video_path)
    reader = OCR_Reader(gpu=args.gpu)

    #read video
    success, image = video.read()
    frame_width, frame_height = image.shape[:2]
    out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

    while success:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)

        result = reader.read_text(img)
        boxes = []
        text = []
        for detection in result:
            if detection[1] not in text:
                text.append(detection[1])
                top_left = tuple(detection[0][0])
                bottom_right = tuple(detection[0][2])
                boxes.append(f"Box: {top_left + bottom_right}")
                img = cv2.rectangle(frame,top_left,bottom_right,(0,255,0),2)

    # write output video
        out.write(img)



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