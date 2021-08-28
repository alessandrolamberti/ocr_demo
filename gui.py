from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2
from ocr.text_reader import OCR_Reader
import time
import os

def select_image():
	global panelA, panelB
	path = filedialog.askopenfilename()
	output_dir = "output/"
	experiment_id = str(time.strftime("%Y-%m-%d_%H-%M-%S"))


	if len(path) > 0:
		image = cv2.imread(path)
		detected, text, boxes = reader.read_text(image)
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

		image = cv2.cvtColor(detected, cv2.COLOR_BGR2RGB)
		image = Image.fromarray(image)
		image = ImageTk.PhotoImage(image)

		if panelA is None or panelB is None:
			panelA = Label(image=image)
			panelA.image = image
			panelA.pack(side="left", padx=10, pady=10)
			panelB = Label(text= [f"{line}\n" for line in text])
			panelB.place = text
			panelB.pack(side="right", padx=10, pady=10)
		# otherwise, update the image panels
		else:
			# update the pannels
			panelA.configure(image=image)
			panelB.configure(text= [f"{line}\n" for line in text])
			panelA.image = image
			panelB.place = text

root = Tk()
panelA = None
panelB = None
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

reader = OCR_Reader(gpu = False)
root.mainloop()