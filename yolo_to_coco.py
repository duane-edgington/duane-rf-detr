import os
import json
from PIL import Image

def convert_yolo_to_coco(yolo_images_path, yolo_labels_path, output_coco_path, class_names):
    coco_data = {
        "info": {
            "year": "2025",
            "version": "0",
            "description": "UAVS",
            "contributor": "",
            "url": "https://public.roboflow.com/object-detection/undefined",
            "date_created": "2025-07-24T06:49:14+00:00"
        },
        "licenses": [
            {
                "id": 1,
                "url": "https://creativecommons.org/licenses/by/4.0/",
                "name": "CC BY 4.0"
            }
        ],
        "images": [],
        "annotations": [],
        "categories": []
    }

    # Populate categories
    for i, name in enumerate(class_names):
        coco_data["categories"].append({"id": i, "name": name, "supercategory": "none"})

    image_id = 0
    annotation_id = 0

    for img_filename in os.listdir(yolo_images_path):
        if not img_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        img_path = os.path.join(yolo_images_path, img_filename)
        label_filename = os.path.splitext(img_filename)[0] + '.txt'
        label_path = os.path.join(yolo_labels_path, label_filename)

        with Image.open(img_path) as img:
            width, height = img.size

        coco_data["images"].append({
            "id": image_id,
            "file_name": img_filename,
            "width": width,
            "height": height
        })

        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    class_id, x_center, y_center, bbox_width, bbox_height = map(float, parts)

                    # Convert normalized YOLO to absolute COCO
                    abs_x_center = x_center * width
                    abs_y_center = y_center * height
                    abs_bbox_width = bbox_width * width
                    abs_bbox_height = bbox_height * height

                    x_min = abs_x_center - (abs_bbox_width / 2)
                    y_min = abs_y_center - (abs_bbox_height / 2)

                    coco_data["annotations"].append({
                        "id": annotation_id,
                        "image_id": image_id,
                        "category_id": int(class_id),
                        "bbox": [x_min, y_min, abs_bbox_width, abs_bbox_height],
                        "area": abs_bbox_width * abs_bbox_height,
                        "iscrowd": 0
                    })
                    annotation_id += 1
        image_id += 1

    with open(output_coco_path, 'w') as f:
        json.dump(coco_data, f, indent=4)
