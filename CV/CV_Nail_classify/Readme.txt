使用说明：
    1. 按照后缀序号依次操作，子目录中有版本迭代说明。
    2. 爬虫下载的图片存放在子目录下data中,中文目录需要更改为英文名。
    3. arrange好后的图片存放在主目录下data中。
    4. preprocessing划分训练集和测试集。
    5. 对数据集进行训练，当前目录下生成文件（增量模型，固化模型，cost/acc图片）。
    6. 使用固化模型参数对指定图片进行预测，打印结果。
    7. 手动将多轮次训练cost/acc图片存放于cost&acc文件夹中，作为实验对比。
    8. 重新训练模型时，需手动删除model(增量模型)及model_freeze(固化模型)文件夹。
