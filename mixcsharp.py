# !/usr/bin/python
# -*- coding=utf8 -*-

import common
import os
import random
import string
import re

ignore_array = ["ToLua"]
"""
:type:list[str]
"""
valueTypeArray = ["int", "string", "float", "bool"]
""":type:list[str]"""
gyreArray = ["private", "public", "protect"]


def __addFunc():
    print "添加方法"
    gyrestr = random.choice(["public", "private"])


def _createCodeName(firstUp=False):
    count = random.randint(3, 10)
    codeName = random.sample(string.ascii_lowercase, count)
    resStr = ""
    if firstUp:
        firstChar = "".join(random.sample(string.ascii_uppercase, 1))
        resStr = firstChar + "" + "".join(codeName)
    else:
        resStr = "".join(codeName)
    return resStr


def _createValue(gy=True, count=1):
    gyreStr = ""
    resStr = ""
    for i in range(0, count):
        if gy:
            gyreStr = random.choice(gyreArray)
        codeName = _createCodeName(True)
        vtype = random.choice(valueTypeArray)
        if vtype == "int":
            resStr += "\t%s %s %s = %d;\n" % (gyreStr, vtype, codeName, random.randint(100, 1000000))
        if vtype == "float":
            resStr += "\t%s %s %s = %df;\n" % (gyreStr, vtype, codeName, random.randint(100, 1000000))
        if vtype == "string":
            resStr += "\t%s %s %s = \"%s\";\n" % (gyreStr, vtype, codeName, "".join(random.sample(string.ascii_lowercase, random.randint(8, 20))))
        if vtype == "bool":
            resStr += "\t%s %s %s = %s;\n" % (gyreStr, vtype, codeName, random.choice(["true", "false"]))
    return resStr


print _createValue(True, 10)


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
            with open(filePath, "r+") as fi:
                content = fi.read()
                se = re.search(".*public.*class.*%s.*{" % (os.path.basename(filePath).split('.')[0]), content).group()
                getPos = content.find(se)
                if getPos != -1:
                    content = content[:getPos + len(se)] + '\n' + addcodestr + content[getPos + len(se):]
                    fi.write(content)
                    tips = '代码：添加成功,%s.cs' % (filePath)
                    print(tips)
