import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets = ['train', 'test', 'val']

Imgpath = '/home/chenchen/lth/yolov5-master/VOC2025/images' 
xmlfilepath = '/home/chenchen/lth/yolov5-master/VOC2025/Annotations/'  
ImageSets_path = '/home/chenchen/lth/yolov5-master/VOC2025/ImageSets/Segmentation/'
Label_path = '/home/chenchen/lth/yolov5-master/VOC2025/'
classes = ["aeroplane", "bicycle", "toothbrush", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
# Imgpath = '/home/chenchen/lth/yolov5-master/VOC/images' 
# xmlfilepath = '/home/chenchen/lth/yolov5-master/VOC/Annotations/'  
# ImageSets_path = '/home/chenchen/lth/yolov5-master/VOC/ImageSets/Main/'
# Label_path = '/home/chenchen/lth/yolov5-master/VOC/'
# classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]



def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id):
    in_file = open(xmlfilepath + '%s.xml' % (image_id))
    out_file = open(Label_path + 'labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        # if obj.find('difficult') == None:
        #     print(in_file)
        # difficult = obj.find('difficult').text
        cls = obj.find('name').text
        # if cls not in classes or int(difficult) == 1:
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


for image_set in sets:
    if not os.path.exists(Label_path + 'labels/'):
        os.makedirs(Label_path + 'labels/')
    image_ids = open(ImageSets_path + '%s.txt' % (image_set)).read().strip().split()
    list_file = open(Label_path + '%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write(Imgpath + '/%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    list_file.close()