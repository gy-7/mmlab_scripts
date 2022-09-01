# 在mmdetection的根目录下运行，报错多那个参数，就把create_mm_config中那个参数赋值给注释掉。
import os
from mmcv import Config

########################### 下面是一些超参数，自行修改  #############################
root_path = os.getcwd()
model_name = 'faster_rcnn_r50_fpn_1x_coco'  # 改成自己要使用的模型名字
work_dir = os.path.join(root_path, "work_dirs", "faster_rcnn_r50_fpn_1x_coco_job1")  # 训练过程中，保存文件的路径，不用动。
baseline_cfg_path = os.path.join('configs', 'faster_rcnn', 'faster_rcnn_r50_fpn_1x_coco.py')  # 改成自己要使用的模型的路径
save_cfg_path = os.path.join(work_dir, 'config.py')  # 生成的配置文件保存的路径

train_data_images = os.path.join(root_path, 'data', 'coco_small', 'train')  # 改成自己训练集图片的目录。
val_data_images = os.path.join(root_path, 'data', 'coco_small', 'val')  # 改成自己验证集图片的目录。
test_data_images = os.path.join(root_path, 'data', 'coco_small', 'test')  # 改成自己测试集图片的目

train_ann_file = os.path.join(root_path, 'data', 'coco_small', 'annotations', 'train.json')  # 修改为自己的数据集的训练集json
val_ann_file = os.path.join(root_path, 'data', 'coco_small', 'annotations', 'val.json')  # 修改为自己的数据集的验证集json
test_ann_file = os.path.join(root_path, 'data', 'coco_small', 'annotations', 'test.json')  # 修改为自己的数据集的验证集json录。

# 去找个网址里找你对应的模型的网址: https://github.com/open-mmlab/mmdetection/blob/master/README_zh-CN.md
load_from = os.path.join(work_dir, 'checkpoint.pth')

# File config
num_classes = 1  # 改成自己的类别数。
classes = ('pedestrian',)  # 改成自己的类别


########################### 上边是一些超参数，自行修改  #############################

def main():
    cfg = Config.fromfile(baseline_cfg_path)

    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    cfg.work_dir = work_dir

    cfg.data.train.img_prefix = train_data_images
    cfg.data.train.classes = classes
    cfg.data.train.ann_file = train_ann_file

    cfg.data.val.img_prefix = val_data_images
    cfg.data.val.classes = classes
    cfg.data.val.ann_file = val_ann_file

    cfg.data.test.img_prefix = test_data_images
    cfg.data.test.classes = classes
    cfg.data.test.ann_file = test_ann_file

    # 加载预训练
    cfg.load_from = load_from

    cfg.dump(save_cfg_path)

    print("—" * 80)
    print(f'CONFIG:\n{cfg.pretty_text}')
    print("—" * 80)
    print("| Save config path:", save_cfg_path)
    print("—" * 80)
    print("| Load pretrain model path:", load_from)
    print("—" * 80)
    print('Please download the model pre-training weights, rename the "checkpoint.pth" '
          'and put it in the following directory:', save_cfg_path[:-9])
    print("—" * 80)


if __name__ == '__main__':
    main()
