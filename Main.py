# -*- coding=utf8 -*-
import platform
import os
import string
from pack_majia import PackMajia
import json
from flashtext import KeywordProcessor

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
    # sysname = platform.system()
    # if sysname == "Darwin":
    #     os.system("ls -al ~")
    # elif sysname == "Windows":
    #     os.system("dir ./")

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
        parse.parse_value(inputValue, sourcePath.strip())