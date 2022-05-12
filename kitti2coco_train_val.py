import json
import os
from PIL import Image
import random

image_path = os.path.join('/data','kitti2d',"training",'image_2')
label_path = os.path.join('/data','kitti2d',"training","label_2")
json_train_path = os.path.join('/data','kitti2d',"training", 'kitti2d_train.json')
json_val_path = os.path.join('/data','kitti2d',"training", 'kitti2d_val.json')
json_save_path = os.path.join('/data','kitti2d',"training", 'kitti2d_trainval.json')
kitti_files = os.listdir(label_path)

categories = ['Car', 'Van', 'Truck', 'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram', 'Misc', 'DontCare']
categories_dict = dict()
for i,c in enumerate(categories):
    categories_dict[c] = i+1


trainval_percent = 1.0
train_percent = 0.8
num = len(kitti_files)
list_index = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
train_list = random.sample(list_index, tr)

base_coco = dict(info = dict(),
                 licenses = list(),
                 images = list(),
                 annotations = list(),
                 categories = list())

train_coco = dict(info = dict(),
                  licenses = list(),
                  images = list(),
                  annotations = list(),
                  categories = list())

val_coco = dict(info = dict(),
                licenses = list(),
                images = list(),
                annotations = list(),
                categories = list())

def base_images(file_name, height, width, image_id):
    return dict(file_name = file_name,
                height = height,
                width = width,
                id = image_id)

def base_annotations(area, image_id, bbox, category_id, instance_id):
    return dict(segmentation = list(),
                area = area,
                iscrowd = 0,
                image_id = image_id,
                bbox = bbox,
                category_id = category_id,
                id = instance_id)    #instance id

def base_categories(category_id, name):
    return dict(supercategory = name,
                id = category_id,
                name = name)
image_id = 0
instance_id = 0
train_annos = []
train_val_annos = []
val_annos = []
for i,anno_file in enumerate(kitti_files):
    image_name = anno_file[:-3] + 'png'
    file_path = os.path.join(image_path, image_name)
    img = Image.open(file_path)
    w = img.width
    h = img.height
    images = base_images(image_name, h, w, image_id)
    base_coco['images'].append(images)
    if i in train_list:
        train_coco['images'].append(images)
    else:
        val_coco['images'].append(images)

    anno_path = os.path.join(label_path, anno_file)
    with open(anno_path,'r') as f:
        annos = f.readlines()
    for anno in annos:
        anno = anno.split()[:8]
        category,truncated,occluded,alpha,l,t,r,b = anno
        fl,ft,fr,fb = float(l), float(t), float(r), float(b)
        w = fr-fl
        h = fb-ft
        area = round(w*h,4)
        bbox = [round(fl,2),round(ft),round(w,2),round(h,2)]
        category_id = categories_dict[category]
        annotations = base_annotations(area, image_id, bbox, category_id, instance_id)
        train_val_annos.append(annotations)
        if image_id==2:
            print(train_val_annos)
        if i in train_list:
            train_annos.append(annotations)
        else:
            val_annos.append(annotations)
        instance_id += 1
    image_id += 1
base_coco.update(annotations=train_val_annos)
train_coco.update(annotations=train_annos)
val_coco.update(annotations=val_annos)
# categories
cate = []
for i,c in enumerate(categories):
    cate.append(base_categories(i+1,c))
base_coco.update(categories=cate)
train_coco.update(categories=cate)
val_coco.update(categories=cate)

json.dump(base_coco,open(json_save_path, 'w'))
json.dump(train_coco,open(json_train_path, 'w'))
json.dump(val_coco,open(json_val_path, 'w'))
print(f"train set:{len(train_coco['images'])}\nval set:{len(val_coco['images'])}\ntotal:{len(base_coco['images'])}")