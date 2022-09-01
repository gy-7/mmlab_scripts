使用OpenMMLab系列的开源库时，常用的脚本合集。

### 脚本解释：

> anchor_visiual.py  生成的锚框可视化 
>
> aug_test.py   自动数据增强，单文件可视化效果。
>
> create_cls_dataset.py   创建分类数据集的脚本。
>
> create_config_mmcls.py    创建mmclassification模型的配置文件，在文件里修改好自己的模型名字，以及数据集路径就可以用了。非常方便，谁用谁说好。
>
> create_config_mmdet.py    同上，创建mmdetection模型的配置文件。
>
> dataset_category_sove.py
>
> old_benchmark.py   旧版本的测试模型推理速度
>
> split_coco_val.py   将coco数据集的val数据集，划分为train,val,test数据集。可以作为简单的模型测试。
>
> split_dataset_just_json.py    划分数据集的json文件，之划分json文件。
>
> sub_solve.py    打比赛时，对最后bbox置信度的处理。
>
> thin_pth.py   mm系列的模型瘦身脚本，只保存模型的权重文件，不保存环境配置，以及优化器参数。
>
> visiual_dataset.py   可视化数据集脚本
>
> visiual_sub.py    打比赛时，可视化推理结果的脚本
