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
gyreArray = ["private", "public", "protected"]


def _createValue(gy=True, count=1):
    """
    自动生成属性定义，自定义前面是否带有访问修饰符，如果不带有访问修饰符，int 类型会自动生成一个 if 判定函数
    :param gy: 是否带有访问修饰符
    :param count: 数量
    :return:
    """
    gyreStr = ""
    resStr = ""
    for i in range(0, count):
        if gy:
            gyreStr = random.choice(gyreArray)
        codeName = common.createCodeName(True)
        vtype = random.choice(valueTypeArray)
        if vtype == "int":
            resStr += "\t%s %s %s = %d;\n" % (gyreStr, vtype, codeName, random.randint(100, 1000000))
            if not gy:
                resStr += _funcIf(codeName, True)
        if vtype == "float":
            resStr += "\t%s %s %s = %df;\n" % (gyreStr, vtype, codeName, random.randint(100, 1000000))
        if vtype == "string":
            resStr += "\t%s %s %s = \"%s\";\n" % (gyreStr, vtype, codeName, "".join(random.sample(string.ascii_lowercase, random.randint(8, 20))))
        if vtype == "bool":
            resStr += "\t%s %s %s = %s;\n" % (gyreStr, vtype, codeName, random.choice(["true", "false"]))
    return resStr


def _createParam(count=1):
    resStr = []
    for i in range(0, count):
        codeName = common.createCodeName(False)
        vtype = random.choice(valueTypeArray)
        resStr.append("%s %s" % (vtype, codeName))
    return ",".join(resStr)


def _funcIf(value, ifCon=False):
    fconStr = ""
    if ifCon:
        fconStr = _createValue(False)
    resStr = """
    if(%s == %d){
    %s
    }
    """ % (value, random.randint(20, 1000), fconStr)
    return resStr


def funcFor():
    valueStr = common.createCodeName(False)
    resStr = """
    for(int %s = 0; %s < %d; %s++){
        %s
    }
    """ % (valueStr, valueStr, random.randint(10, 100), valueStr, _createValue(False, 5))
    return resStr


def _createFunc(count=1):
    resStr = ""
    for i in range(0, count):
        gyreStr = random.choice(gyreArray)
        funcName = common.createCodeName(True)
        valueStr = _createValue(False, 5)
        forStr = funcFor()

        funcStr = """
        %s void %s (%s){
            %s
        }
        """ % (gyreStr, funcName, _createParam(random.randint(0, 5)), valueStr + "\n" + forStr)
        resStr += (funcStr + "\n")
    return resStr


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
            if filePath.lower().__contains__(ignore.lower()):
                willcontinue = True
        if willcontinue:
            continue
        else:
            os.chdir(os.path.dirname(filePath))
            filename = os.path.basename(filePath).replace(".cs", "")
            value_str = _createValue(True, random.randint(3, 15))
            funcStrs = _createFunc(random.randint(1, 3))
            addcodestr = value_str + "\n" + funcStrs
            print u"打开的cs脚本名称", filePath
            with open(filePath, "r+") as fi:
                content = fi.read()
                se = re.search(".*public.*class.*%s.*{" % (filename), content)
                if not se:
                    se = re.search(".*public.*class.*%s.*\n.*{" % (filename), content)
                if se:
                    segroup = se.group()
                    if segroup.lstrip().startswith("//") or segroup.lstrip().startswith("/*") or segroup.strip().__contains__("static"):
                        continue
                    getPos = content.find(segroup)
                    if getPos != -1:
                        content = content[:getPos + len(segroup)] + '\n' + addcodestr + content[getPos + len(segroup):]
                        fi.seek(0, 0)
                        fi.write(content)
                        print u'代码添加成功', filePath
                else:
                    print u"脚本很奇怪", filePath
