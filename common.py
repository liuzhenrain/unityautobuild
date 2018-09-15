# !/usr/bin/python
# -*- coding=utf8 -*-

import os


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
        else:
            get_all_files(os.path.join(dir_path, _file), file_array, exp)
