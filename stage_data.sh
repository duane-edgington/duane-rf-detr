#!/bin/bash
# scipt to set up directories
#

## get test images for smoke test

wget -q https://media.roboflow.com/notebooks/examples/dog-2.jpeg
wget -q https://media.roboflow.com/notebooks/examples/dog-3.jpeg

## get datasets

mkdir -p $PWD/datasets/
mkdir -p $PWD/datasets/savedir/

cp /mnt/PAM_Analysis/duane_scratch/rfdetr/images.tar.gz $PWD/datasets/savedir/
cp /mnt/PAM_Analysis/duane_scratch/rfdetr/labels.tar.gz $PWD/datasets/savedir/
cp /mnt/PAM_Analysis/duane_scratch/rfdetr/data.yaml $PWD/datasets/savedir/

tar xf $PWD/datasets/savedir/images.tar.gz --directory $PWD/datasets/savedir/
tar xf $PWD/datasets/savedir/labels.tar.gz --directory $PWD/datasets/savedir/

## make the directories that yolov11 expects
mkdir -p $PWD/datasets/train/
mkdir -p $PWD/datasets/train/images/
mkdir -p $PWD/datasets/train/labels/
mkdir -p $PWD/datasets/test/
mkdir -p $PWD/datasets/test/images/
mkdir -p $PWD/datasets/test/labels/
mkdir -p $PWD/datasets/val/
mkdir -p $PWD/datasets/val/images/
mkdir -p $PWD/datasets/val/labels/

#move the data to the expected directories
rsync -a "$PWD/datasets/savedir/images/train/" "$PWD/datasets/train/"
#cp -r "$PWD/datasets/savedir/labels/train/" "$PWD/datasets/train/labels/"

rsync -a "$PWD/datasets/savedir/images/test/" "$PWD/datasets/test/"
#cp -r "$PWD/datasets/savedir/labels/test/" "$PWD/datasets/test/labels/"

rsync -a "$PWD/datasets/savedir/images/val/" "$PWD/datasets/valid/"
#cp -r "$PWD/datasets/savedir/labels/val/" "$PWD/datasets/valid/labels"

ls "$PWD/datasets"






