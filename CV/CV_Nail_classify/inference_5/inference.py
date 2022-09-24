'''
    inference
    by:freefish
    version:1.0
'''
import paddle
import paddle.fluid as fluid
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os
import sys
dir_mytest = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_mytest)
from global_var import *


place = fluid.CPUPlace()
infer_exe = fluid.Executor(place)
inference_scope = fluid.core.Scope()
model_freeze_dir = os.path.join(os.getcwd(), "model_freeze")

# 加载数据
def load_image(path):
    img = paddle.dataset.image.load_and_transform(path, 400, 400, False).astype("float32")
    img = img / 255.0
    return img

infer_imgs = []
# 类别0
test_img = os.path.join(os.getcwd(), "data/Nail_Art/Nail_Art_5.jpg")
# test_img = "../data/Nail_Art/Nail_art_5.jpg"

# 类别1
# test_img = "../data/Nail_Normal/Nail_normal_5.jpg"

infer_imgs.append(load_image(test_img))
infer_imgs = np.array(infer_imgs)

with fluid.scope_guard(inference_scope):
    [inference_program, feed_target_names, fetch_targets] = \
        fluid.io.load_inference_model(model_freeze_dir, infer_exe)

    # 开始预测
    results = infer_exe.run(inference_program,
                            feed={feed_target_names[0]: infer_imgs},
                            fetch_list=fetch_targets)
    print("results:", results)

    result = results[0]
    print(result.shape)
    max_index = np.argmax(result)
    for k, v in name_dict.items():
        if max_index == v:
            print("预测结果: 类别编号[%d], 名称[%s], 概率[%.4f]" % (max_index, k, result[0][max_index] * 100))

    # 显示原图
    img = Image.open(test_img)
    plt.imshow(img)
    plt.show()