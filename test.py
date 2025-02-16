import json
from pycocotools.coco import COCO
# 在文件开头添加导入
import xml.etree.ElementTree as ET
import os
import shutil
from tqdm import tqdm  # 如果要用到进度条


# 替换配置
VOC_TO_REMOVE = "bird"        # 被替换的VOC类别
COCO_NEW_CLASS = "toothbrush" # COCO新类别（ID=90）
COCO_CLASS_ID = 90            # 对应COCO标注中的category_id

# COCO与VOC共有类别映射（基于之前分析）
COCO_VOC_MAP = {
    1: "person",  2: "bicycle",  3: "car",       5: "aeroplane",
    6: "bus",     7: "train",    9: "boat",      44: "bottle",
    62: "chair",  21: "cow",     19: "horse",    18: "dog",
    64: "pottedplant", 67: "diningtable", 72: "tvmonitor"
}


# 加载COCO标注
coco = COCO("/home/chenchen/lth/yolov5-master/coco2014/annotations/instances_train2014.json")

# 获取所有包含toothbrush的图像ID
img_ids = coco.getImgIds(catIds=[COCO_CLASS_ID])

# 收集完整标注数据
coco_data = []
for img_id in img_ids:
    img_info = coco.loadImgs(img_id)[0]
    ann_ids = coco.getAnnIds(imgIds=img_id)
    anns = coco.loadAnns(ann_ids)
    coco_data.append((img_info, anns))

def convert_coco_to_voc(img_info, anns, output_dir):
    # 创建VOC标注结构
    root = ET.Element("annotation")
    ET.SubElement(root, "filename").text = f"coco_{img_info['file_name']}"
    
    # 添加图像尺寸
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(img_info['width'])
    ET.SubElement(size, "height").text = str(img_info['height'])
    ET.SubElement(size, "depth").text = "3"
    
    # 处理所有标注
    for ann in anns:
        
        # 判断类别类型
        if ann["category_id"] == COCO_CLASS_ID:
            obj = ET.SubElement(root, "object")
            ET.SubElement(obj, "name").text = COCO_NEW_CLASS
        elif ann["category_id"] in COCO_VOC_MAP:
            obj = ET.SubElement(root, "object")
            ET.SubElement(obj, "name").text = COCO_VOC_MAP[ann["category_id"]]
        else:
            continue  # 忽略其他无关类别
        
        # 转换bbox格式 [x,y,w,h] → [xmin,ymin,xmax,ymax]
        bbox = ann["bbox"]
        bndbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(int(bbox[0]))
        ET.SubElement(bndbox, "ymin").text = str(int(bbox[1]))
        ET.SubElement(bndbox, "xmax").text = str(int(bbox[0] + bbox[2]))
        ET.SubElement(bndbox, "ymax").text = str(int(bbox[1] + bbox[3]))
    
    # 保存XML文件
    xml_path = f"{output_dir}/Annotations/coco_{img_info['file_name'].replace('.jpg', '.xml')}"
    ET.ElementTree(root).write(xml_path)
    
    # 复制图像文件并重命名
    shutil.copy(
        f"coco2014/train2014/{img_info['file_name']}",
        f"{output_dir}/images/coco_{img_info['file_name']}"
    )

# 批量转换
for img_info, anns in coco_data:
    convert_coco_to_voc(img_info, anns, "VOC2025")
