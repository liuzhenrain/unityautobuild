# !/usr/bin/python
# -*- coding=utf8 -*-

import common
import os

ignore_array = ["ToLua"]
"""
:type:list[str]
"""

def mix_csharp(path):
    print "开始对CSharp添加垃圾代码和注释"
    csharp_files = []
    """
    :type:list[str]
    """
    common.get_all_files(path, csharp_files, ".cs")
    for filePath in csharp_files:
        willcontinue = False
        for ignore in ignore_array:
            if filePath.lower().__contains__(ignore):
                willcontinue = True
        if willcontinue:
            continue
        else:
            with open(filePath) as fi:
                all_lines = fi.readlines()






