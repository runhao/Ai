'''
    preprocessing
    by:freefish
'''
import sys
import os
dir_mytest = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_mytest)

from global_var import * #导包

name_data_list = {}  # 记录每个人多少张训练图片、多少张测试图片

def save_train_test_list(path, name):
    '''
        形成文件列表
    :param path: 数据地址
    :param name: 类别名
    :return:None
    '''
    if name not in name_data_list:  # 未在字典中
        img_list = []
        img_list.append(path)  # 将图片添加到列表
        name_data_list[name] = img_list  # 存入字典
    else:  # 已经在字典中
        name_data_list[name].append(path)  # 加入

def save_train_test_file():
    '''
        划分测试集和训练集
    :return: None
    '''
    for name, img_list in name_data_list.items():
        i = 0
        num = len(img_list)
        print("%s: %d张" % (name, num))

        for img in img_list:
            if i % 10 == 0:  # 每10笔取一笔测试数据
                with open(test_file_path, "a") as f:
                    line = "%s\t%d\n" % (img, name_dict[name]) # 存放图片路径及类别编号
                    # print(line)
                    f.write(line)
            else:  # 其它作为训练数据
                with open(train_file_path, "a") as f:
                    line = "%s\t%d\n" % (img, name_dict[name])
                    # print(line)
                    f.write(line)
            i += 1
    print('生成数据列表完成！')

if __name__ == '__main__':
    dirs = os.listdir(data_root_path)
    for d in dirs:
        full_path = os.path.join(data_root_path, d)  # 完整路径
        if os.path.isdir(full_path):  # 目录
            imgs = os.listdir(full_path)
            for img in imgs:
                # print(img + "," + d)
                save_train_test_list(os.path.join(full_path, img), d)
        else:  # 文件
            pass

    # 若无创建，反之清空数据文件
    with open(test_file_path, "w") as f:
        pass
    with open(train_file_path, "w") as f:
        pass

    save_train_test_file()


