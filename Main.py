# !/usr/bin/python
# -*- coding=utf8 -*-
import platform
import os
from pack_majia import PackMajia
import json
import time
from exportproject import ExportProj
import shutil


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


def deleteUnExsitFolder(path):
    print path
    files = os.listdir(path)
    for _file in files:
        realPath = os.path.join(path, _file)
        dontremove = False
        for pack_name in json_obj["pack_game"]:
            if realPath.__contains__(pack_name.split('/')[-1]):
                dontremove = True
        if not dontremove:
            print "Deleting files/folders", realPath
            if os.path.isfile(realPath):
                os.remove(realPath)
            else:
                shutil.rmtree(realPath, False)


if __name__ == "__main__":
    isMac = False
    sysname = platform.system()
    if sysname == "Darwin":
        isMac = True
    elif sysname == "Windows":
        isMac = False

    with open("config.json", "r") as fi:
        json_obj = json.load(fi, encoding="utf8")

    inputValue = "1"
    sourcePath = json_obj["project_path"]
    if len(sourcePath) > 0:
        os.chdir(sourcePath)
        os.chdir(os.path.pardir)
        baseName = os.path.basename(sourcePath)
        targetPath = os.getcwd() + os.sep + baseName + "_Mix_" + time.strftime("%m-%d_%H-%M", time.localtime())
        print "Copy new project folder:", targetPath
        if isMac:
            os.system("cp -R {0} {1}".format(sourcePath, targetPath))
        else:
            os.system("")

        print "target path:",targetPath
        subRes = os.path.join(targetPath, "Assets/Res/SubGames")
        deleteUnExsitFolder(subRes)
        subRes = os.path.join(targetPath, "Assets/Lua/LuaScript/SubGames")
        deleteUnExsitFolder(subRes)
        if not json_obj["skip_confuse"]:
            majia_build = PackMajia(targetPath)
            majia_build.pack()
        else:
            print "Skip confusion, package directly"
        if json_obj["auto_pack"]:
            print "Package Starting"
            print targetPath, os.path.abspath(targetPath)
            export = ExportProj(targetPath, json_obj)
            export.genProject()


    else:
        print "Don`t configuration Project Path"
        exit()
