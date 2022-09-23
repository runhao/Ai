import cv2 as cv
import os
from math import *


def remote(img, angle):
    '''
        不切边旋转
    :param img: 原始图像
    :param angle: 旋转角度
    :return: 新的img
    '''
    h, w = img.shape[:2]
    h_new = int(w * fabs(sin(radians(angle))) + h * fabs(cos(radians(angle))))
    w_new = int(h * fabs(sin(radians(angle))) + w * fabs(cos(radians(angle))))

    matRotation = cv.getRotationMatrix2D((w / 2, h / 2), angle, 1)

    matRotation[0, 2] += (w_new - w) / 2
    matRotation[1, 2] += (h_new - h) / 2

    imgRotation = cv.warpAffine(img, matRotation, (w_new, h_new), borderValue=(255, 255, 255))

    return imgRotation


def do_rotate(im, angle, center=None, scale=1.0):
    """
        图像旋转变换
    :param im: 原始图像数据
    :param angle: 旋转角度
    :param center: 旋转中心，如果为None则以原图中心为旋转中心
    :param scale: 缩放比例，默认为1
    :return: 返回旋转后的图像
    """
    h, w = im.shape[:2]  # 获取图像高、宽

    # 旋转中心默认为图像中心
    if center is None:
        center = (w / 2, h / 2)

    # 计算旋转矩阵
    M = cv.getRotationMatrix2D(center, angle, scale)

    # 使用openCV仿射变换实现函数旋转
    rotated = cv.warpAffine(im, M, (w, h))

    return rotated  # 返回旋转后的矩阵


def img_path(dirs, data_root_path):
    '''
        获取图片路径
    :return: 所有子目录下的原始样本和子目录下的目录和子目录
    '''
    sub_dir_path = []
    for d in dirs:
        dir_path = os.path.join(data_root_path, d)  # 拼接路径
        if not os.path.isdir(dir_path):  # 不是目录
            continue
        sub_dir_path.append(os.path.join(dir_path))   # 子目录下的目录
    return ([os.listdir(sub_dir_path[0]), os.listdir(sub_dir_path[1])], sub_dir_path, dirs)  # 返回所有子目录下的原始样本


def scale(min_size):
    '''
        将图片缩放至固定的像素
    :param min_size: 设定图片最短边像素值
    :return: None
    '''

    data_root_path = os.path.join(os.getcwd(), "data")
    imgs, sub_dir_path, dirs = img_path(os.listdir(data_root_path), data_root_path)  # 列出所有子目录
    dd = os.path.abspath('..')  # 获取上级目录
    os.chdir(dd)
    try:
        os.mkdir("data")
    except Exception as e:
        print(e)
    os.chdir(os.path.join(dd, "data"))
    for x in range(len(dirs)):
        i = 1
        os.mkdir(dirs[x])
        os.chdir(os.path.join(dd, "data", dirs[x]))
        for img_file in imgs[x]:  # 遍历
            img_full_path = os.path.join(sub_dir_path[x], img_file)  # 拼接完整路径
            try:
                im = cv.imread(img_full_path)
                h, w = im.shape[:2]  # 获取图像尺寸
            except Exception as e:
                print(e)
                continue
            n = min(h, w) / min_size  # 缩放目标尺寸
            dst_size = (int(w / n), int(h / n))  # 缩放目标尺寸
            img_new = cv.resize(im, dst_size)  # 执行缩放
            pos = img_file.find(".")  # 返回.的位置
            name = dirs[x]
            suffix = img_file[pos:]  # 取出后缀名
            img_new_name = "%s_%d%s" % (name, i, suffix)
            print("scale ok:" + os.path.join(dd, "data") +img_new_name)
            cv.imwrite(img_new_name, img_new)  # 将缩放后的图片保存至新文件
            i += 1
        os.chdir(os.path.join(dd, "data"))  # 返回上级目录


def rotate_all():
    dd = os.path.abspath('..')  # 获取上级目录
    os.chdir(dd)
    data_root_path = os.path.join(os.getcwd(), "data")
    imgs, sub_dir_path, dirs = img_path(os.listdir(data_root_path), data_root_path)  # 列出所有子目录
    for x in range(len(dirs)):
        print(dirs[x])
        os.chdir(os.path.join(dd, "data", dirs[x]))
        for img_file in imgs[x]:  # 遍历
            img_full_path = os.path.join(sub_dir_path[x], img_file)  # 拼接完整路径
            im = cv.imread(img_full_path)  # img_full_path
            pos = img_file.find(".")  # 返回.的位置
            name = img_file[0:pos]  # 取出名称部分
            suffix = img_file[pos:]  # 取出后缀名

            # 旋转45/90/135/180/225/270/315度
            for i in range(1, 8):
                img_new = remote(im, 45 * i)
                # 拼一个新的文件名
                img_new_name = "%s_rotate_%d%s" % (name, i, suffix)

                cv.imwrite(os.path.join(sub_dir_path[x], img_new_name), img_new)  # 将裁剪后的图片保存至新文件
                print("rotate:", os.path.join(dd, "data", img_new_name))
        os.chdir(os.path.join(dd, "data"))  # 返回上级目录

if __name__ == "__main__":
    # 图像处理
    scale(400) # 最短边400px
    print("图像缩放结束")

    # 图像旋转
    rotate_all()
    print("图像旋转结束")
