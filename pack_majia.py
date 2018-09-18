# !/usr/bin/python
# -*- coding=utf8 -*-

import os
import md5
from flashtext import KeywordProcessor
import mixcsharp,mixluascripts


class PackMajia:
    _sourcePath = ""
    _allLuaFiles = []
    _ignoreFiles = ["MVCRegister",
                    "MessageNames",
                    "Dialog",
                    "MVCFramework",
                    "Global.lua",
                    "Main.lua",
                    "Tools",
                    "ViewConfig",
                    "Define.lua",
                    "ScreenMask.lua",
                    "GameMgrLua"]
    _exp = ".lua"

    def __init__(self, path):
        self._sourcePath = path

    def pack(self):
        path_array = self._sourcePath.split(os.sep)
        path_array.append("Assets")
        path_array.append("Lua")
        path_array.append("LuaScript")
        lua_path = self._sourcePath+os.sep+os.sep.join(["Assets","Lua","LuaScript"])
        mixluascripts.mix_lua(lua_path)
        csharpPath = self._sourcePath+os.sep+os.sep.join(["Assets","CScripts"])
        mixcsharp.mix_csharp(csharpPath)
        self._allLuaFiles = []
        if os.path.exists(lua_path):
            self.get_all_files(lua_path, self._allLuaFiles, ".lua")

            self.change_res_name(".prefab")
            self.change_ogg_name()
            self.replace_file_name()
        else:
            print("路径配置错误，应该是 Unity 项目的根目录，错误路径", self._sourcePath)

    def get_all_files(self, dir_path, file_array, exp):
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
                self.get_all_files(os.path.join(dir_path, _file), file_array, exp)

    def replace_file_name(self):
        replace_array = []

        for fi in self._allLuaFiles:
            will_continue = False
            for v in self._ignoreFiles:
                if fi.__contains__(v):
                    will_continue = True
            if will_continue:
                continue
            fileName = os.path.basename(fi)
            os.chdir(os.path.dirname(fi))
            file_name_array = fileName.split(".")
            if len(file_name_array) > 2:
                print "这个文件有问题" + fileName
            else:
                m1 = md5.new()
                itemMes = []
                itemMes.append(fi)
                temp = file_name_array[0] + os.times()[4].__str__()
                m1.update(temp.encode(encoding="utf8"))
                new_name = "x" + m1.hexdigest() + self._exp
                itemMes.append(new_name)
                replace_array.append(itemMes)
                self.change_file_str(file_name_array[0], "x" + m1.hexdigest())

        for item in replace_array:
            origin = item[0]
            new_name = item[1]
            os.chdir(os.path.dirname(origin))
            os.rename(os.path.basename(origin), new_name)
            print os.path.basename(origin), "replace name", new_name

    def change_file_str(self, currentStr, newStr):
        keyword = KeywordProcessor(True)
        keyword.add_keyword(currentStr, newStr)
        for fi in self._allLuaFiles:
            if os.path.exists(fi):
                with open(fi, "r+") as f:
                    file_str = f.read()
                    keywords_found = keyword.extract_keywords(file_str)
                    if len(keywords_found) > 0:
                        print "will replace file:", fi
                        newfileStr = keyword.replace_keywords(file_str)
                        f.seek(0, 0)
                        f.write(newfileStr)
            else:
                print "不包含文件", fi

    def change_res_name(self, exp):
        path_array = self._sourcePath.split(os.sep)
        path_array.append("Assets")
        path_array.append("Res")
        path = os.sep.join(path_array)
        res_array = []
        self.get_all_files(path, res_array, exp)
        m1 = md5.new()
        for name in res_array:
            time = os.times()[4]
            print "Change res:", name
            baseName = os.path.basename(name)
            if baseName.lower() == "UIVersionUpdate.prefab".lower():
                continue
            dirName = os.path.dirname(name)
            os.chdir(dirName)
            if exp == ".ogg":
                md5Str = baseName.split('.')[0]
            else:
                md5Str = baseName.split('.')[0] + time.__str__()
            m1.update(md5Str.encode(encoding="utf8"))
            newName = "y" + m1.hexdigest() + exp
            os.rename(name, newName)
            self.change_file_str(baseName, newName)

    def change_ogg_name(self):
        path_array = self._sourcePath.split(os.sep)
        path_array.append("Assets")
        path_array.append("Res")
        path = os.sep.join(path_array)
        res_array = []
        self.get_all_files(path, res_array, ".ogg")
        m1 = md5.new()
        ogg_table = []
        for name in res_array:
            time = os.times()[4]
            print "Change ogg:", name
            baseName = os.path.basename(name)
            dirName = os.path.dirname(name)
            os.chdir(dirName)
            newName = ""
            hasName = False
            for v in ogg_table:
                if baseName == v[0]:
                    print "已有同名文件",baseName,v[1]
                    hasName = True
                    newName = v[1]
            if not hasName:
                md5Str = baseName.split('.')[0]+time.__str__()
                m1.update(md5Str.encode(encoding="utf8"))
                newName = "y" + m1.hexdigest()+".ogg"
                item=[]
                item.append(baseName)
                item.append(newName)
                ogg_table.append(item)
                self.change_file_str(baseName, newName)
            os.rename(name, newName)
