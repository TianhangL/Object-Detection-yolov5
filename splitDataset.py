import os
import random
import argparse

def generate_voc_segmentation_splits(
    jpeg_dir="JPEGImages",
    anno_dir="Annotations",
    output_dir="ImageSets/Segmentation",
    ratios=(0.31, 0.29, 0.4),  # train, val, test
    seed=42
):
    """
    生成VOC格式的语义分割数据集划分文件
    :param jpeg_dir: JPEG图像目录路径
    :param anno_dir: 标注文件目录路径
    :param output_dir: 输出划分文件目录
    :param ratios: 划分比例 [train, val, test]，需总和为1
    :param seed: 随机种子
    """
    # 验证参数有效性
    assert abs(sum(ratios) - 1.0) < 1e-6, "划分比例总和必须为1"
    assert len(ratios) == 3, "需要提供train/val/test三个比例"

    # 收集有效图像ID（同时存在于JPEG和Annotations）
    jpeg_files = {f.split('.')[0] for f in os.listdir(jpeg_dir) if f.endswith('.jpg')}
    anno_files = {f.split('.')[0] for f in os.listdir(anno_dir) if f.endswith('.xml')}
    valid_ids = sorted(list(jpeg_files & anno_files))  # 取交集
    
    print(f"找到{len(valid_ids)}个有效样本")
    if not valid_ids:
        raise ValueError("未找到有效的图像和标注文件对")

    # 设置随机种子保证可复现
    random.seed(seed)
    random.shuffle(valid_ids)

    # 计算划分点
    total = len(valid_ids)
    train_end = int(ratios[0] * total)
    val_end = train_end + int(ratios[1] * total)

    # 分割数据集
    splits = {
        "train": valid_ids[:train_end],
        "val": valid_ids[train_end:val_end],
        "test": valid_ids[val_end:]
    }

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 写入文件
    for split_name, ids in splits.items():
        file_path = os.path.join(output_dir, f"{split_name}.txt")
        with open(file_path, 'w') as f:
            f.write("\n".join(ids))
        print(f"生成 {split_name} 划分: {len(ids)} 个样本 -> {file_path}")

    # 生成trainval.txt（训练+验证集合并）
    with open(os.path.join(output_dir, "trainval.txt"), 'w') as f:
        f.write("\n".join(splits["train"] + splits["val"]))
    print(f"生成 trainval 合并文件: {len(splits['train'])+len(splits['val'])} 个样本")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--jpeg", default="/home/chenchen/lth/yolov5-master/VOC2025/images", help="JPEG图像目录路径")
    parser.add_argument("--anno", default="/home/chenchen/lth/yolov5-master/VOC2025/Annotations", help="标注XML文件目录路径")
    parser.add_argument("--output", default="/home/chenchen/lth/yolov5-master/VOC2025/ImageSets/Segmentation", 
                       help="输出划分文件目录")
    parser.add_argument("--ratios", type=float, nargs=3, default=[0.31, 0.29, 0.4],
                       help="划分比例：train val test (需总和为1)")
    parser.add_argument("--seed", type=int, default=42, help="随机种子")
    args = parser.parse_args()

    generate_voc_segmentation_splits(
        jpeg_dir=args.jpeg,
        anno_dir=args.anno,
        output_dir=args.output,
        ratios=args.ratios,
        seed=args.seed
    )
