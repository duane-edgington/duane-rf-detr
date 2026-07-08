import numpy as np
import supervision as sv

from PIL import Image

#from rfdetr import RFDETRMedium
from rfdetr import RFDETRLarge
from rfdetr.util.coco_classes import COCO_CLASSES

from roboflow import Roboflow

# inference an image that is in the local directory
image = Image.open("dog-2.jpeg")

#model = RFDETRMedium(resolution=576)
model = RFDETRLarge(resolution=704)  #This is the resolution of RFDETRLarge. Must be divisible by 32
#model.optimize_for_inference() # this threw an error in my python 3.13, pytorch environment

detections = model.predict(image, threshold=0.2)

color = sv.ColorPalette.from_hex([
    "#ffff00", "#ff9b00", "#ff8080", "#ff66b2", "#ff66ff", "#b266ff",
    "#9999ff", "#3399ff", "#66ffff", "#33ff99", "#66ff66", "#99ff00"
])
text_scale = sv.calculate_optimal_text_scale(resolution_wh=image.size)
thickness = sv.calculate_optimal_line_thickness(resolution_wh=image.size)

bbox_annotator = sv.BoxAnnotator(color=color, thickness=thickness)
label_annotator = sv.LabelAnnotator(
    color=color,
    text_color=sv.Color.BLACK,
    text_scale=text_scale,
    smart_position=True
)

labels = [
    f"{COCO_CLASSES[class_id]} {confidence:.2f}"
    for class_id, confidence
    in zip(detections.class_id, detections.confidence)
]

annotated_image = image.copy()
annotated_image = bbox_annotator.annotate(annotated_image, detections)
annotated_image = label_annotator.annotate(annotated_image, detections, labels)
annotated_image.thumbnail((800, 800))

#annotated_image

# Save the annotated image
annotated_image.save("annotated_dog-2.jpeg")
print("Annotated image saved as 'annotated_dog-2.jpeg'")


## get api key for roboflow

import os
import sys

def get_api_key():
    api_key = os.environ.get('ROBOFLOW_API_KEY')

    if not api_key:
        print("Error: API_KEY environment variable is not set")
        print("Please set it with: export API_KEY='your_key_here'")
        sys.exit(1)

    return api_key

# Usage
myapi_key = get_api_key()
print("API Key loaded successfully")

## train a model

from roboflow import download_dataset

rf = Roboflow(api_key=myapi_key)
#project = rf.workspace().project("basketball-players-fy4c2")
#dataset = download_dataset("https://universe.roboflow.com/roboflow-jvuqo/basketball-player-detection-2/13", "coco")

dataset = "/home/duane/rf-detr/duane-rf-detr/datasets"


model = RFDETRLarge()



#model.train(dataset_dir=dataset, epochs=20, batch_size=16, grad_accum_steps=1)  # full train takes about 3 days
model.train(dataset_dir=dataset, epochs=2, batch_size=16, grad_accum_steps=1)  # test train

print("Training results saved in directory 'output'")
