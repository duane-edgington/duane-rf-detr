#!/bin/bash
# scipt to set up directories
#

mkdir $PWD/datasets/
mkdir $PWD/datasets/savedir/

cp /mnt/PAM_Analysis/duane_scratch/images.tar.gz $PWD/datasets/savedir/
cp /mnt/PAM_Analysis/duane_scratch/labels.tar.gz $PWD/datasets/savedir/
cp /mnt/PAM_Analysis/duane_scratch/data.yaml $PWD/datasets/savedir/

tar xf $PWD/datasets/savedir/images.tar.gz --directory $PWD/datasets/savedir/
tar xf $PWD/datasets/savedir/labels.tar.gz --directory $PWD/datasets/savedir/

## make the directories that yolov11 expects
mkdir $PWD/datasets/train/
mkdir $PWD/datasets/train/images/
mkdir $PWD/datasets/train/labels/
mkdir $PWD/datasets/test/
mkdir $PWD/datasets/test/images/
mkdir $PWD/datasets/test/labels/
mkdir $PWD/datasets/val/
mkdir $PWD/datasets/val/images/
mkdir $PWD/datasets/val/labels/





#move the data to the expected directories
rsync -a "$PWD/datasets/savedir/images/train/" "$PWD/datasets/train/"
#cp -r "$PWD/datasets/savedir/labels/train/" "$PWD/datasets/train/labels/"

rsync -a "$PWD/datasets/savedir/images/test/" "$PWD/datasets/test/"
#cp -r "$PWD/datasets/savedir/labels/test/" "$PWD/datasets/test/labels/"

rsync -a "$PWD/datasets/savedir/images/val/" "$PWD/datasets/valid/"
#cp -r "$PWD/datasets/savedir/labels/val/" "$PWD/datasets/valid/labels"

ls $PMD/datasets/






