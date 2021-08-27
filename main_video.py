import cv2 
import argparse
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
    if not os.path.exists(output_dir + experiment_id):
            os.makedirs(output_dir + experiment_id)
    
    if not os.path.exists(output_dir + experiment_id + "/frames"):
            os.makedirs(output_dir + experiment_id + "/frames")
        
    video = cv2.VideoCapture(args.video_path)
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height =int(video.get( cv2.CAP_PROP_FRAME_HEIGHT))

    reader = OCR_Reader(gpu=args.gpu)
    output = cv2.VideoWriter(output_dir + f'{experiment_id}/frames/' + 'output.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width,frame_height))
    success, image = video.read()
    boxes = []
    text = []

    while True:
        success, image = video.read()
        if not success:
            break

        result = reader.read_video(image)
        
        if result is not None:
            for detection in result:
                top_left = tuple(detection[0][0])
                bottom_right = tuple(detection[0][2])
                text.append(detection[1])
                boxes.append(detection[0])
                try:
                    image = cv2.rectangle(image,top_left,bottom_right,(0,255,0),3)
                    image = cv2.putText(image, detection[1], top_left, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                    output.write(image)
                except:
                    continue
        
        with open(output_dir + experiment_id + '/boxes' + '.txt', 'w') as f: 
            f.write(f"Detected boxes - experiment id: {experiment_id}\n")
            for box in boxes:
                f.write(f"\n{box}")

        cv2.imshow('image', image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video.release()
    output.release()

if __name__ == "__main__":
    args = parse_args()

    main(args)