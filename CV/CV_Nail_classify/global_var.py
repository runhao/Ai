# linux下环境变量
import os
dd = os.path.abspath('..')
os.chdir(dd)
now = os.getcwd()
data_root_path = os.path.join(now, "data")  # 数据路径
test_file_path = os.path.join(now, "data/test.txt")  # 测试文件路径
train_file_path = os.path.join(now, "data/train.txt")  # 训练文件路径

name_dict = {"Nail_Normal": 0, "Nail_Art": 1}  # 字典