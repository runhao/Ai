'''
    解压数据
'''

import os

cd = ("cd data/ &&")
os.system(cd + "unzip -qo lslm.zip && unzip -qo lslm-test.zip")
os.system(cd + "mv lslm/*.txt .")
os.system(cd + "mv lslm-test/*.txt .")
os.system(cd + "sed -i 's/^/lslm\//' train.txt")
os.system(cd + "sed -i 's/^/lslm-test\//' eval.txt")
os.system(cd + "awk '{print $2}' label_list.txt > label_list")
print("解压完成.")