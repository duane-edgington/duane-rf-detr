# duane-rf-detr
duane rf-detr code

## Set-up
on spark-ae0e

```
cd /home/duane/rf-detr
```

```
build_clean_pytorch.sh
```

```
venv source/bin/activate
```

*or* 

```
cd /home/duane/rf-detr/duane-rf-detr
```

```
build_venv.sh  # this script builds a local venv and does the pip install from requirements.txt
```



## get and setup the directories

```
stage_data.sh     # stage the yolo datasets (generated elsewhere)
```

useful to move files around:

instead of cp, use rsync -a /some/path/to/src/ /other/path/to/dest/ --progress

```
python3 yolo_to_coco.py   # set up coco dataset from yolo dataset
```

example

```
python3 yolo_to_coco.py --images_path "datasets/train/train" --labels_path "datasets/savedir/labels/train" --output_path "datasets/train/_annotations.coco.json" --class_names "object"
```


## train ##

```
python3 duane-rfdetr.py
```     
duane-rfdetr.py    # train the model
