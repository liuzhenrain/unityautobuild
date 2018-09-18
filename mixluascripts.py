# !/usr/bin/python
# -*- coding=utf8 -*-

import common
import os
import random
import string
import re
import copy

ignore_array = []
"""
:type:list[str]
"""

value_type_array = ["int", "string", "bool"]


def _createValue(isLocal=False, count=1):
    resStr = ""
    for i in range(0, count):
        lStr = "local" if isLocal else ""
        codename = "mix_" + common.createCodeName(False)
        vtype = random.choice(value_type_array)
        if vtype == "int":
            resStr += "%s %s = %d\n" % (lStr, codename, random.randint(10, 10000))
            if isLocal:
                resStr += "\t" + _addif(codename)
        elif vtype == "string":
            resStr += '%s %s = \"%s\"\n' % (lStr, codename, "".join(random.sample(string.ascii_lowercase, random.randint(5, 25))))
        elif vtype == "bool":
            resStr += '%s %s = %s\n' % (lStr, codename, random.choice(["false", "true"]))
    return resStr


def _addif(valName):
    resstr = """if %s == %d then\n\t%s\nend\n""" % (valName, random.randint(100, 10000), _createValue(False, random.randint(1, 10)))
    return resstr


def _addfor(count):
    resstr = ""
    for i in range(0, count):
        forcont = _createValue(True, random.randint(1, 5))
        forstr = """for i=1,i < %d do\n\t%s\nend\n""" % (random.randint(1, 100), forcont)
        resstr += forstr
    return resstr


def _createFunc(count=1):
    resstr = ""
    for i in range(0, count):
        codename = "Mix_" + common.createCodeName(True)
        hasparam = random.choice([False, True])
        param_array = []
        if hasparam:
            param_array.append(common.createCodeName(False))
        param_str = ",".join(param_array)
        localstr = "local " if random.choice([True, False]) else ""
        funcon = _createValue(True, random.randint(1, 5)) + "\n" + _addfor(random.randint(1, 5))
        resstr += """%sfunction %s(%s)\n\t%s\nend\n""" % (localstr, codename, param_str, funcon)
    return resstr


def mix_lua(path):
    allluafiles = []
    """
    :type:list[str]
    """
    common.get_all_files(path, allluafiles, ".lua")
    for filePath in allluafiles:
        willcontinue = False
        os.chdir(os.path.dirname(filePath))
        for ignore in ignore_array:
            if filePath.lower().__contains__(ignore.lower()):
                willcontinue = True
        if willcontinue:
            continue
        else:
            print u"正在处理文件", filePath
            with open(filePath, "r+") as fi:
                lines = fi.readlines()
                fi.seek(0, 0)
                fi.truncate()
                addcontent = _createFunc(random.randint(1, 3))
                str = addcontent + "\n" + "".join(lines)
                fi.write(str)
                print u"混淆已完成", filePath
