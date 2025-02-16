## 数据集构建过程

首先下载VOC2007的数据集和COCO2014的数据集

运行test.py，加载coco数据集并收集所有toothbrush的数据，转换为VOC标注格式

运行delVoc.py，删除VOC被替换的数据类别

运行splitDataset.py对新构建的VOC2025数据集进行分割



## 项目构建

首先运行pip install -r requirements.txt配置环境

本实验训练出的模型结果保存在了`runs/train/exp4`下

推理可直接运行detect.py，推理结果保存在`runs/detect`下