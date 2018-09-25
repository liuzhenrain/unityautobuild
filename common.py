# !/usr/bin/python
# -*- coding=utf8 -*-

import os
import random
import string


def get_all_files(dir_path, file_array, exp):
    """
    递归查找指定文件夹下所有的指定后缀文件
    :param dir_path: 根目录
    :param file_array: 保存的数组
    :param exp: 后缀
    :return:
    """
    files = os.listdir(dir_path)
    for _file in files:
        if os.path.isfile(os.path.join(dir_path, _file)):
            if _file.endswith(exp):
                file_array.append(os.path.join(dir_path, _file))
            elif exp == "*":
                file_array.append(os.path.join(dir_path,_file))
        else:
            if _file == ".git":
                continue
            get_all_files(os.path.join(dir_path, _file), file_array, exp)


def createCodeName(firstUp=False, focusIgnoreArray=[]):
    """
    创建一个属性的名字或者方法的名字
    :param firstUp: 是否首字母大写
    :return: 返回自动生成的字符
    """
    count = random.randint(3, 10)
    codeName = random.sample(string.ascii_lowercase, count)
    resStr = ""
    if firstUp:
        firstChar = "".join(random.sample(string.ascii_uppercase, 1))
        resStr = firstChar + "b" + "".join(codeName)
    else:
        resStr = "a" + "".join(codeName)
    return resStr
