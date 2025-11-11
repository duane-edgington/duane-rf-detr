# duane-rf-detr
duane rf-detr code

## Set-up
on spark-ae0e

cd /home/duane/rf-detr

build_clean_pytorch.sh

venv source/bin/activate

cd duane-rf-detr

## get and setup the directories

stage_data.sh     # stage the yolo datasets (generated elsewhere)

yolo_to_coco.py   # set up coco dataset from yolo dataset

duane-rfdetr.py    # train the model
