'''
    train - VGG
    by:freefish
    version:2.1
'''
import logging
import os
import time
import paddle
from paddle import fluid
import matplotlib.pyplot as plt

import sys

dir_mytest = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_mytest)
from global_var import *
from multiprocessing import cpu_count

type_size = 2  # 种类
train_img_size = 400  # 训练图像大小
label_dict = {}  # 标签字典
BUF_SIZE = 10000
BATCH_SIZE = 32  # 批次大小
EPOCH_NUM = 20  # 迭代次数
learning_rate = 0.00000001  # 学习率


def init_log_config():  # 初始化日志相关配置
    '''
        参见logging模块的四大组件
    :return: None
    '''
    global logger

    logger = logging.getLogger()  # 创建日志对象
    logger.setLevel(logging.INFO)  # 设置日志级别
    log_path = os.path.join(os.getcwd(), 'logs')

    if not os.path.exists(log_path):  # 创建日志路径
        os.makedirs(log_path)

    log_name = os.path.join(log_path, 'train.log')  # 训练日志文件
    fh = logging.FileHandler(log_name, mode='w')  # 打开文件句柄
    fh.setLevel(logging.DEBUG)  # 设置级别

    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")  # 一般格式器中要定义好日志产生时间，日志级别，产生日志的模块全路径，模块的哪一行，具体的日志信息等
    fh.setFormatter(formatter)
    logger.addHandler(fh)


# 对自定义的数据集创建训练集train和reader
def train_r(train_list, buffered_size=BUF_SIZE):
    '''
        读取训练集
    :param train_list: 样本目录
    :param buffered_size: 缓冲大小，一次性读取数目
    :return: paddle读取数据时自带一个多线程读取数据的函数
    '''

    def reader():
        with open(train_list, "r") as f:  # 打开训练样本
            lines = [line.strip() for line in f]  # 一行一行的存入列表
            for line in lines:
                img_path, lab = line.strip().split("\t")
                if not os.path.exists(img_path):  # 图片可能空白太多被移走
                    continue
                # print(img_path, ":", int(lab))
                yield img_path, int(lab)

    return paddle.reader.xmap_readers(train_mapper, reader, cpu_count(), buffered_size)  # paddle读取数据时自带一个多线程读取数据的函数


# 定义训练的mapper
def train_mapper(sample):
    '''
        图片处理
    :param sample:
    :return: 图片及标签
    '''
    img, lable = sample
    if not os.path.exists(img):
        print(img, "文件不存在")
    # 进行图片读取，由于数据集的像素和维度不同，需要进一步对图像进行变换
    img = paddle.dataset.image.load_image(img)
    # 对图像进行简单变换，对图像进行crop修剪操作，输出img的维度(3, 400, 400)
    img = paddle.dataset.image.simple_transform(im=img,
                                                resize_size=train_img_size,  # 剪裁图片
                                                crop_size=train_img_size,
                                                is_color=True,  # 彩色图像
                                                is_train=True)
    # 将img数组进行归一化处理，得到0~1之间的数值
    img = img.flatten().astype("float32") / 255.0
    return img, lable


def test_r(test_list, buffered_size=BUF_SIZE):
    def reader():
        with open(test_list, "r") as f:
            # 将train.list里面的标签和图片放到一个list列表中，中间用\t隔开
            lines = [line.strip() for line in f]
            for line in lines:
                img_path, lab = line.strip().split("\t")
                if not os.path.exists(img_path):  # 图片可能空白太多被移走
                    print("图片不存在:", img_path)
                    continue
                yield img_path, int(lab)

    return paddle.reader.xmap_readers(test_mapper, reader, cpu_count(), buffered_size)


def test_mapper(sample):
    img, label = sample

    img = paddle.dataset.image.load_image(img)
    img = paddle.dataset.image.simple_transform(im=img,
                                                resize_size=train_img_size,
                                                crop_size=train_img_size,
                                                is_color=True,
                                                is_train=False)
    img = img.flatten().astype("float32") / 255.0
    return img, label


def vgg_bn_drop(image, type_size):
    '''
        搭建VGG网络
    输入层 --> 卷积*2 --> 卷积*2 --> 卷积*3 --> 卷积*3 --> 卷积*3 --> 池化 --> dropout --> 池化 --> dropout --> 全连接 --> 输出层                                                        <--
    :param image: 样本图像
    :param type_size: 类别数量
    :return:
    '''

    def conv_block(ipt, num_filter, groups, dropouts):
        return fluid.nets.img_conv_group(input=ipt,  # 具有[N，C，H，W]格式的输入图像
                                         pool_size=2,
                                         pool_stride=2,
                                         conv_num_filter=[num_filter] * groups,  # 过滤器个数
                                         conv_filter_size=3,  # 过滤器大小
                                         conv_act='relu',
                                         conv_with_batchnorm=True,  # 表示在 Conv2d Layer 之后是否使用 BatchNorm
                                         conv_batchnorm_drop_rate=dropouts,  # 表示 BatchNorm 之后的 Dropout Layer 的丢弃概率
                                         pool_type='max')  # 最大池化

    conv1 = conv_block(image, 64, 2, [0.0, 0])
    conv2 = conv_block(conv1, 128, 2, [0.0, 0])
    conv3 = conv_block(conv2, 256, 3, [0.0, 0.0, 0])
    conv4 = conv_block(conv3, 512, 3, [0.0, 0.0, 0])
    conv5 = conv_block(conv4, 512, 3, [0.0, 0.0, 0])

    drop = fluid.layers.dropout(x=conv5, dropout_prob=0.5)
    fc1 = fluid.layers.fc(input=drop, size=512, act=None)

    bn = fluid.layers.batch_norm(input=fc1, act='relu')
    drop2 = fluid.layers.dropout(x=bn, dropout_prob=0.0)
    fc2 = fluid.layers.fc(input=drop2, size=512, act=None)
    predict = fluid.layers.fc(input=fc2, size=type_size, act='softmax')

    return predict


############################ 程序开始 ################################
def plt_train():
    plt.figure("training", facecolor="lightgray")
    plt.title("training", fontsize=24)
    plt.xlabel("iter", fontsize=20)
    plt.ylabel("cost/acc", fontsize=20)
    plt.plot(batches, costs, color='red', label="Training Cost")
    plt.plot(batches, accs, color='green', label="Training Acc")
    plt.legend()
    plt.grid()
    plt.savefig("train.png")
    plt.show()


def plt_test():
    plt.figure("testing", facecolor="lightgray")
    plt.title("testing", fontsize=24)
    plt.xlabel("iter", fontsize=20)
    plt.ylabel("cost/acc", fontsize=20)
    plt.plot(test_batches, test_costs_p, color='red', label="Testing Cost")
    plt.plot(test_batches, test_accs_p, color='green', label="Testing Acc")
    plt.legend()
    plt.grid()
    plt.savefig("test.png")
    plt.show()


if __name__ == '__main__':
    init_log_config()  # 初始化日期工具
    print("开始执行:", time.strftime('%Y-%m-%d %H-%M-%S'))
    image = fluid.layers.data(name="image", shape=[3, train_img_size, train_img_size],
                              dtype="float32")  # [3, 400, 400]表示三通道RGB图像
    label = fluid.layers.data(name="label", shape=[1], dtype="int64")
    # 获取分类器，用VGG网络进行分类,type_size要和训练时的类别一致
    predict = vgg_bn_drop(image=image, type_size=type_size)
    cost = fluid.layers.cross_entropy(input=predict, label=label)  # 获取损失函数和准确率
    avg_cost = fluid.layers.mean(cost)  # 计算cost中所有元素的平均值
    accuracy = fluid.layers.accuracy(input=predict, label=label)  # 计算准确率
    # paddle框架采取类似于流程图的形式。program会记录用户定义的操作。这里将用户操作进行赋值，用于之后测试。
    test_program = fluid.default_main_program().clone(for_test=True)
    # 定义优化器Adam,一种万金油式的优化器,使用起来非常方便,梯度下降速度快,但是容易在最优值附近震荡,竞赛中性能会略逊于SGD
    optimizer = fluid.optimizer.Adam(learning_rate)
    opt = optimizer.minimize(avg_cost)
    # place = fluid.CPUPlace() # CPU执行训练
    place = fluid.CUDAPlace(0)  # GPU执行训练
    exe = fluid.Executor(place)
    exe.run(fluid.default_startup_program())
    # 定义输入数据的维度, DataFeeder负责将reader返回的数据转成一种特殊结构，输入到Executor
    feeder = fluid.DataFeeder(feed_list=[image, label], place=place)
    model_save_dir = "model/Nail/"  # 模型保存路径
    if os.path.exists(model_save_dir):  # 先加载模型执行增量训练
        fluid.io.load_persistables(exe, model_save_dir, fluid.default_main_program())
        print("加载增量模型成功.")
    costs = []  # 损失值,可视化使用
    accs = []  # 准确率,可视化使用
    test_accs_p = []
    test_costs_p = []
    batches = []
    test_batches = []
    trainer_reader = train_r(train_list=train_file_path)
    train_batch_reader = paddle.batch(paddle.reader.shuffle(reader=trainer_reader, buf_size=BUF_SIZE),
                                      batch_size=BATCH_SIZE)
    # 训练5个Pass, 每个Pass训练结束后，使用验证集进行验证，并求出相应的损失值cost和准确度acc
    times = 0
    test_times = 0
    for pass_id in range(EPOCH_NUM):
        train_cost = 0
        for batch_id, data in enumerate(train_batch_reader()):
            times += 1
            train_cost, train_acc = exe.run(program=fluid.default_main_program(),  # 运行主程序
                                            feed=feeder.feed(data),  # 喂入一个batch的数据
                                            fetch_list=[avg_cost, accuracy])  # fetch均方误差和准确率

            if batch_id % 50 == 0:
                tmp_str = "Pass:%d, Step:%d, Cost:%.6f, Acc:%.6f" % (pass_id, batch_id, train_cost[0], train_acc[0])
                # logger.info(tmp_str) # 写入日志，次数过多爆内存
                print(tmp_str)
                accs.append(train_acc[0])
                costs.append(train_cost[0])
                batches.append(times)

        # 开始测试
        test_accs = []
        test_costs = []
        tester_reader = test_r(test_list=test_file_path)
        test_batch_reader = paddle.batch(tester_reader, batch_size=BATCH_SIZE)

        for batch_id, data in enumerate(test_batch_reader()):
            test_cost, test_acc = exe.run(program=test_program,
                                          feed=feeder.feed(data),
                                          fetch_list=[avg_cost, accuracy])
            test_accs.append(test_acc[0])
            test_costs.append(test_cost[0])
        test_times += 1
        test_batches.append(test_times)

        test_cost = (sum(test_costs) / len(test_costs))
        test_acc = (sum(test_accs) / len(test_accs))
        test_costs_p.append(test_cost)
        test_accs_p.append(test_acc)
        tmp_str = "Test:%d, Cost:%.6f, ACC:%.6f" % (pass_id, test_cost, test_acc)
        # logger.info(tmp_str)
        print(tmp_str)

    if not os.path.exists(model_save_dir):  # 如果存储模型的目录不存在，则创建
        os.makedirs(model_save_dir)
    fluid.io.save_persistables(exe, model_save_dir, fluid.default_main_program())
    print("保存增量模型成功!")

    # 保存固化模型
    model_freeze_dir = "model_freeze/"
    if not os.path.exists(model_freeze_dir):
        os.makedirs(model_freeze_dir)
    fluid.io.save_inference_model(dirname=model_freeze_dir,
                                  feeded_var_names=["image"],
                                  target_vars=[predict],
                                  executor=exe)
    print("保存固化模型成功!")

    # 训练过程可视化
    plt_train()
    plt_test()