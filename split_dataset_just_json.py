# 如果只是根据json划分数据集，也就是将instances_train2017.json中的东西划分为train和val，那就用这个脚本，又快又稳。
import json
import os
import random
from pycocotools.coco import COCO
import shutil

# coco.getCatIds() # 此函数用于获取加载对象所包含的所有类别的id（即category 的序号）
# coco.getAnnIds() # 获取加载对象所包含的所有标记信息（就是所有图片的Segmentation，即分割的坐标数据）
# coco.getImgIds() # 获取所有 标记所对应的原图id

root = os.getcwd()
workdir = os.path.join(root, 'annotations')

coco = COCO(os.path.join(workdir, 'instances_val2017.json'))
class_names = [coco.cats[catId]['name'] for catId in coco.getCatIds()]
categories = [dict(id=i + 1, name=name) for i, name in enumerate(class_names)]

annotaions_train = []
images_train = []
annotaions_val = []
images_val = []

# change imgid to 0~len()-1
train_imgid = 0
val_imgid = 0

for catId in coco.getCatIds():
    imgIds = coco.getImgIds(catIds=[catId])
    random.shuffle(imgIds)
    for imgId in imgIds[:int(len(imgIds) * 0.2)]:     # 验证集取0.2
    # for imgId in imgIds[:1]:
        img = coco.imgs[imgId]
        img['id'] = val_imgid
        images_val.append(img)
        anns = coco.imgToAnns[imgId]
        for ann in anns:
            ann['image_id'] = val_imgid
            # x1,y1,w,h --> x1,y1,x2,y2
            ann['bbox'][2] = ann['bbox'][0] + ann['bbox'][2]
            ann['bbox'][3] = ann['bbox'][1] + ann['bbox'][3]
            annotaions_val.append(ann)
        val_imgid += 1

    for imgId in imgIds[int(len(imgIds) * 0.2):]:     # 验证集取0.8
    # for imgId in imgIds[1:3]:
        img = coco.imgs[imgId]
        img['id'] = train_imgid
        images_train.append(img)
        anns = coco.imgToAnns[imgId]
        for ann in anns:
            ann['image_id'] = train_imgid
            # x1,y1,w,h --> x1,y1,x2,y2
            ann['bbox'][2] = ann['bbox'][0] + ann['bbox'][2]
            ann['bbox'][3] = ann['bbox'][1] + ann['bbox'][3]
            annotaions_train.append(ann)
        train_imgid += 1
new_train = {"images": images_train, "type": "instances", "annotations": annotaions_train, "categories": categories}
new_valid = {"images": images_val, "type": "instances", "annotations": annotaions_val, "categories": categories}

cnt = 0
imgids = []
for idx in range(len(new_train['annotations'])):
    if new_train['annotations'][idx]['image_id'] not in imgids:
        imgids.append(new_train['annotations'][idx]['image_id'])
        cnt += 1

if os.path.exists(os.path.join(root, 'coco', 'annotations')):
    shutil.rmtree(os.path.join(root, 'coco', 'annotations'))

os.makedirs(os.path.join(root, 'coco', 'annotations'))

with open(os.path.join(root, 'coco', 'annotations', 'instances_train2017.json'), "w") as jsonFile:
    json.dump(new_train, jsonFile)

with open(os.path.join(root, 'coco', 'annotations', 'instances_val2017.json'), "w") as jsonFile:
    json.dump(new_valid, jsonFile)

# copy img

imgs_train = new_train['images']
imgs_val = new_valid['images']
if os.path.exists(os.path.join(root, 'coco', 'train2017')):
    shutil.rmtree(os.path.join(root, 'coco', 'train2017'))
if os.path.exists(os.path.join(root, 'coco', 'val2017')):
    shutil.rmtree(os.path.join(root, 'coco', 'val2017'))

os.mkdir(os.path.join(root, 'coco', 'train2017'))
os.mkdir(os.path.join(root, 'coco', 'val2017'))
for img in imgs_train:
    shutil.copy(os.path.join(root, 'imgs', img['file_name']), os.path.join(root, 'coco', 'train2017'))
for img in imgs_val:
    shutil.copy(os.path.join(root, 'imgs', img['file_name']), os.path.join(root, 'coco', 'val2017'))
