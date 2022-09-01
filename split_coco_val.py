# 划分coco数据集
# 将coco数据集分为train和val两个子集
import json
import os
import random
import shutil

from pycocotools.coco import COCO
from tqdm import trange

train_percentage = 0.7
val_percentage = 0.2
root_dir = os.getcwd()
json_fp = os.path.join(root_dir, 'coco', 'annotations', 'instances_val2017.json')
img_dir = os.path.join(root_dir, 'coco', 'val2017')
save_dir = os.path.join(root_dir, 'coco_small')


def split_coco(json_fp, img_dir, save_dir):
    json_data = json.load(open(json_fp, 'r'))
    coco = COCO(json_fp)

    train_dir = os.path.join(save_dir, 'train')
    val_dir = os.path.join(save_dir, 'val')
    test_dir = os.path.join(save_dir, 'test')
    train_json = {'info': json_data['info'], 'licenses': json_data['licenses'], 'images': [], 'annotations': [],
                  'categories': json_data['categories']}
    val_json = {'info': json_data['info'], 'licenses': json_data['licenses'], 'images': [], 'annotations': [],
                'categories': json_data['categories']}
    test_json = {'info': json_data['info'], 'licenses': json_data['licenses'], 'images': [], 'annotations': [],
                 'categories': json_data['categories']}
    # 创建coco目录结构
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
    os.makedirs(save_dir)
    os.mkdir(train_dir)
    os.mkdir(val_dir)
    os.mkdir(test_dir)
    os.mkdir(os.path.join(save_dir, 'annotations'))

    imgs = coco.imgs
    img_ids = coco.getImgIds()
    train_ids = random.sample(img_ids, int(len(img_ids) * train_percentage))
    val_ids = random.sample(list(set(img_ids) - set(train_ids)), int(len(img_ids) * val_percentage))

    m = len(img_ids)
    for i in trange(m):
        ann_ids = coco.getAnnIds(imgIds=img_ids[i])
        if img_ids[i] in train_ids:
            train_json['images'].append(imgs[img_ids[i]])
            shutil.copy(os.path.join(img_dir, imgs[img_ids[i]]['file_name']),
                        os.path.join(train_dir, imgs[img_ids[i]]['file_name']))
            for ann_id in ann_ids:
                train_json['annotations'].append(coco.anns[ann_id])
        elif img_ids[i] in val_ids:
            val_json['images'].append(imgs[img_ids[i]])
            shutil.copy(os.path.join(img_dir, imgs[img_ids[i]]['file_name']),
                        os.path.join(val_dir, imgs[img_ids[i]]['file_name']))
            for ann_id in ann_ids:
                val_json['annotations'].append(coco.anns[ann_id])
        else:
            test_json['images'].append(imgs[img_ids[i]])
            shutil.copy(os.path.join(img_dir, imgs[img_ids[i]]['file_name']),
                        os.path.join(test_dir, imgs[img_ids[i]]['file_name']))
            for ann_id in ann_ids:
                test_json['annotations'].append(coco.anns[ann_id])

    with open(os.path.join(save_dir, 'annotations', 'train.json'), 'x') as f:
        json.dump(train_json, f)
    with open(os.path.join(save_dir, 'annotations', 'val.json'), 'x') as f:
        json.dump(val_json, f)
    with open(os.path.join(save_dir, 'annotations', 'test.json'), 'x') as f:
        json.dump(test_json, f)


if __name__ == '__main__':
    split_coco(json_fp, img_dir, save_dir)
    print('done')
