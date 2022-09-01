# 裁剪图片创建分类数据集
import os
import cv2
from pycocotools.coco import COCO

root_dir = os.getcwd()
img_dir = os.path.join(root_dir, 'all_data', 'train')
anns_fp = os.path.join(root_dir, 'all_data', 'annotations', 'train.json')
save_dir = os.path.join(root_dir, 'cls_dataset')

# create class directory
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    os.mkdir(os.path.join(save_dir, 'shoot'))
    os.mkdir(os.path.join(save_dir, 'noshoot'))

coco = COCO(anns_fp)
img_ids = coco.getImgIds()

cnt = 0
for img_id in img_ids:
    img_info = coco.loadImgs(img_id)[0]
    img_fp = os.path.join(img_dir, img_info['file_name'])
    ann_ids = coco.getAnnIds(imgIds=img_id)
    ann_info = coco.loadAnns(ann_ids)
    if len(ann_info) == 0:
        continue
    for i in range(len(ann_info)):
        if ann_info[i]['category_id'] == 1:
            img = cv2.imread(img_fp)
            x1 = int(ann_info[i]['bbox'][0])
            y1 = int(ann_info[i]['bbox'][1])
            x2 = x1 + int(ann_info[i]['bbox'][2])
            y2 = y1 + int(ann_info[i]['bbox'][3])
            img = img[y1:y2, x1:x2]
            cv2.imwrite(os.path.join(save_dir, 'shoot', str(cnt) + '.jpg'), img)
            cnt += 1
