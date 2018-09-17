# !/usr/bin/python
# -*- coding=utf8 -*-
import platform
import os
from pack_majia import PackMajia
import json
import time


class parse_input_value:
    """
    处理传入的内容,根据内容确定要执行的逻辑
    """
    _actionType = 0
    _sourcePath = ""

    def parse_value(self, cusType, path):
        self._actionType = cusType
        self._sourcePath = path
        print (self._actionType, self._sourcePath)
        pack = PackMajia(path)
        pack.pack()


if __name__ == "__main__":
    isMac = False
    sysname = platform.system()
    if sysname == "Darwin":
        isMac = True
    elif sysname == "Windows":
        isMac = False

    # inputValue = raw_input("1. ios马甲包打包,2. 安卓完整打包 3. 安卓补丁包 4. IOS 补丁包: ")
    # sourcePath = raw_input("项目的根目录地址,需要完整地址:")
    # json_obj=[]
    with open("config.json", "r") as fi:
        # print fi.read()
        json_obj = json.load(fi, encoding="utf8")

    parse = parse_input_value()
    inputValue = "1"
    sourcePath = json_obj["project_path"]
    if len(sourcePath) > 0:
        os.chdir(sourcePath)
        os.chdir(os.path.pardir)
        baseName = os.path.basename(sourcePath)
        targetPath = baseName+"_Mix_" + time.strftime("%m-%d_%H-%M", time.localtime())
        print "拷贝新目录",targetPath
        if isMac:
            os.system("cp -R {0} {1}".format(sourcePath, targetPath))
        else:
            os.system("")
        parse.parse_value(inputValue, os.path.abspath(targetPath))
    else:
        print "没有配置项目地址"
        exit()
