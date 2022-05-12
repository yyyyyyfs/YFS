from base64 import encode
import json
import os
from PIL import Image
import random

file_path = os.path.join('data','Analyse_data','1号阀室平台')
data_names = os.listdir(file_path)
json_save_path = os.path.join("/home/guest/data/Analyse_data/1号_coco/training",'data2coco_all.json')
json_train_path = os.path.join("/home/guest/data/Analyse_data/1号_coco/training",'data2coco_train.json')
json_val_path = os.path.join("/home/guest/data/Analyse_data/1号_coco/training",'data2coco_val.json')

categories = ['person','head','helmet','clothes','uniform','helmet_unknown','uniform_unknown']
categories_dict = dict()
for i,c in enumerate(categories):
    categories_dict[c] = i+1
num = len(data_names)//2
train_list = random.sample(range(num),int(0.8*num))#按照0.8划分训练集
# print(len(train_list))

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
def base_images(file_name,height,weight,id):
    return dict(file_name = file_name,
                height = height,
                weight =weight,
                id = id)
def base_annotations(area,image_id,bbox,category_id,instance_id):
    return dict(segmentation = list(),
                area = area,
                iscrowd = 0,
                image_id = image_id,
                bbox = bbox,
                category_id = category_id,
                instance_id = instance_id)
def base_categories(category_id, name):
    return dict(supercategory = name,
                id = category_id,
                name = name)
json_path = []
image_path = []
image_id = 0
instance_id = 0
cate_gory = []
annotations = []
for i,name in enumerate(data_names):#得到所有的json、图片文件地址
    if os.path.splitext(name)[1] == '.json':
        json_path.append(os.path.join(file_path,name))
    else:
        image_path.append(os.path.join(file_path,name))
  
for i,img_file in enumerate(image_path):
    #写入coco的['images']
    image_name = os.path.basename(img_file)
    img = Image.open(img_file)
    w = img.width
    h = img.height
    image_id += 1
    images = base_images(image_name,h,w,image_id)
    
    base_coco['images'].append(images)
    if i in train_list:
        train_coco['images'].append(images)
    else:
        val_coco['images'].append(images)
    #写入coco的['annotations']
    anno_file = img_file[:-3] + 'json'
    with open(anno_file,'r') as f:
        data = json.load(f)
    for dic in data['shapes']:
        x1 = dic['points'][0][0]
        y1 = dic['points'][0][1]
        x2 = dic['points'][1][0]
        y2 = dic['points'][1][1]
        w = x2 - x1
        h = y2 - y1
        instance_id +=1
        area = round((x2 - x1)*(y2 - y1),4)
        bbox = [round(x1,4),round(y1,4),round(w,4),round(h,4)]       
        category = dic['label']
        category_id = categories_dict[category]
        annotations = base_annotations(area,image_id,bbox,category_id,instance_id)
        base_coco['annotations'].append(annotations)
    if  i in train_list:
        train_coco['annotations'].append(annotations)                  
    else:
        val_coco['annotations'].append(annotations)
    
    #写入coco的['category']
for i,c in enumerate(categories):
    cate_gory.append(base_categories(i+1,c))
base_coco['categories'].append(cate_gory)
train_coco['categories'].append(cate_gory)
val_coco['categories'].append(cate_gory)
#生成更新后的json
json.dump(base_coco,open(json_save_path,'w'),indent=4,)
json.dump(train_coco,open(json_train_path,'w'),indent=4)
json.dump(val_coco,open(json_val_path,'w'),indent=4)
print(f"train set:{len(train_coco['images'])}\nval set:{len(val_coco['images'])}\ntotal:{len(base_coco['images'])}")
