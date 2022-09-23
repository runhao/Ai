'''
    基于opencv的图像缩放
'''

import os
import cv2 as cv
import math


class cv_scale:
    def __init__(self, path, resize_path, file_size):
        '''
            初始化
        :param path: 表示原始文件路径
        :param resize_path: 表示压缩后存放路径
        :param file_size: 表示压缩目标值
        '''
        self.path = path
        self.resize_path = resize_path
        self.file_size = file_size * 2

    def get_doc_size(self):
        '''
        :return: 返回图片的文档大小，单位为 MB
        '''
        try:
            size = os.path.getsize(self.path)
            return self.get_mb_size(size)
        except Exception as e:
            print("error:", e)

    def get_mb_size(self, bytes):
        bytes = float(bytes)
        mb = bytes / 1024 / 1024
        return mb

    def delete_file(self):
        '''
            删除压缩过程中产生的中间文件
        :return: None
        '''
        if self.file_exist():
            os.remove(self.path)
        else:
            print('no such file:%s' % self.path)

    def file_exist(self):
        return os.path.exists(self.path)

    def resize_rate(self, fx, fy):
        im_resize = cv.resize(self.image, None, fx=fx, fy=fy)
        self.delete_file()
        self.save_image(im_resize)

    def save_image(self, image):
        cv.imwrite(self.path, image)

    def read_image(self):
        return cv.imread(self.path)

    def run(self):
        size = self.get_doc_size()
        self.image = self.read_image()
        self.delete_file()
        while size > self.file_size:
            rate = math.ceil((size / self.file_size) * 10) / 10
            rate = math.sqrt(rate)
            rate = 1.0 / rate
            if self.file_exist():
                self.resize_rate(rate, rate)
            else:
                self.path ,self.resize_path = self.resize_path, self.path
                self.resize_rate(rate, rate)
                size = self.get_doc_size()


if __name__ == '__main__':
    op = cv_scale("./data/1.jpg", "data/1.jpg", 1) # 输入路径，输出路径，压缩至?MB
    print(op.run())