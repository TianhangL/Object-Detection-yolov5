# 删除所有包含被替换类别的数据
import os
import xml.etree.ElementTree as ET
import os
import shutil
from tqdm import tqdm  # 如果要用到进度条

VOC_TO_REMOVE = "bird"        # 被替换的VOC类别

def delete_voc_class(class_name):
    # 删除标注文件
    for xml_file in os.listdir("VOC2025/Annotations"):
        tree = ET.parse(f"VOC2025/Annotations/{xml_file}")
        root = tree.getroot()
        
        if any(obj.find('name').text == class_name for obj in root.findall('object')):
            os.remove(f"VOC2025/Annotations/{xml_file}")
            # 同步删除图像文件
            img_name = root.find('filename').text
            os.remove(f"VOC2025/images/{img_name}")

# delete_voc_class(VOC_TO_REMOVE)

num = 0 
for xml_file in os.listdir("VOC2025/Annotations"):
        tree = ET.parse(f"VOC2025/Annotations/{xml_file}")
        root = tree.getroot()
        for obj in root.findall('object'):
            if obj.find('name') == None:
                print(xml_file)
            if obj.find('name').text == "toothbrush" :
                num = num + 1
                print(obj.find('name').text)
print(num)
            