# !/usr/bin/python
# -*- coding=utf8 -*-
# Adongblog
# V1.0
# 2018.05.06

import os
from time import strftime
import time
import random,string
import re
# title=
datestr=strftime("%Y-%m-%d")
def codeNameOnly():   #只生成随机名称
    namenum=random.randint(3,8)
    typestr=random.choice(['int','bool','string'])
    return typestr+' '+''.join(random.sample(string.ascii_lowercase,namenum))
def codeName():
    namenum=random.randint(3,8)
    funname1=''.join(random.sample(string.ascii_uppercase,1))
    funname2=''.join(random.sample(string.ascii_lowercase,namenum))
    return funname1+funname2

def valueName(gy=True,outnum=1):
    valueType=random.choice(['int','string','bool'])
    gyrestr=''
    restr=''
    for num in range(0,outnum):
        if(gy):
            gyrestr=random.choice(['public','private'])

        if(valueType=='int'):
            vaname=codeName()
            restr+='%s int %s=%d;\n'%(gyrestr,vaname,random.randint(1,1000))
            if(gy==False):  #方法内才生成
                restr+='\n'+funif(vaname,True)
        elif(valueType=='string'):
            restr+='%s string %s="%s";\n'%(gyrestr,codeName(),codeName())
        elif(valueType=='bool'):
            restr+='%s bool %s=%s;\n'%(gyrestr,codeName(),random.choice(['true','false']))
    return restr

def funif(vlm,ifcon):
    ifconstr=''
    if(ifcon==True):
        ifconstr=valueName(False)
    restr="""
    if(%s==%d){
        %s
    }"""%(vlm,random.randint(1,100),ifconstr)
    return restr

def funfor():
    forstr="""
    for(int i=1;i<%d;i++){
        %s
    }"""%(random.randint(4,10),valueName(False))
    return forstr

def funget():
    pass
# 方法构造
def funCreat():
    gyrestr=random.choice(['public','private'])
    valstr='%s'%(codeNameOnly())
    autofun=random.choice(['if','for'])
    autofunstr=''
    if(autofun=='for'):
        autofunstr=funfor()

    crstr="""
        %s void %s(%s){
            %s
        }"""%(gyrestr,codeName(),valstr,autofunstr)
    return crstr

## 添加注释
def addzhushistr():
    addstr="""
    //Copyright(C) 2018 by Adongblog
    //文件名：
    //作者：Adongblog
    //创建时间：%s
    //版本：V1.0
    //修改历史：
    //描述：
    //================================
    """%(datestr)
    return addstr
def AddZhushi(fixurl):

    with open('%s'%(fixurl),'r+') as f:
        content = f.read()
        #添加注释
        if addzhushistr() in content:
            print('注释：已添加过了')
        else:
            f.seek(0, 0)
            f.write('%s\n'%(addzhushistr())+content)
            tips=u'注释：添加成功,%s'%(fixurl)
            FixLog(tips)
            print(tips)
def FindDir(url):
    try:
        os.chdir(url)
    except:
        return
    for new_dir in os.listdir(os.curdir):
        # print("文件名："+new_dir+'  路径：'+os.getcwd()+os.sep+new_dir)
        filepath=os.getcwd()+os.sep+new_dir
        filepath=filepath.replace('\\','/').rstrip()
        fty=filepath[-3:]
        if '.cs' in fty:
            AddZhushi(filepath)


# 添加代码
def AddGaurdCode(fixurl,filename):
    scrfun="%s\n"%(valueName(True,random.randint(6,12)))
    scrstr="private void %s(){\n    %s\n    %s\n    %s\n    %s\n}"%(codeName(),valueName(False),valueName(False),valueName(False),funfor())
    funcre=funCreat()
    addcodestr='\n%s\n    %s\n  %s\n//Adongblog\n\n'%(scrfun,scrstr,funcre)
    try:
        fileget=open('%s'%(fixurl),'r')
        content=fileget.read()
        se=re.search(r'.*public.*class.*%s.*\s{'%(filename),content).group()
        getpos=content.find(se)
        # print('添加位置：%s 位置内容:%s'%(getpos,se))
        if getpos !=-1:
            content=content[:getpos+len(se)]+'\n'+addcodestr+content[getpos+len(se):]
            fileget=open('%s'%(fixurl),'w')
            fileget.write(content)
            tips=u'代码：添加成功,%s.cs'%(fixurl)
            FixLog(tips)
            print(tips)
        fileget.close()
    except:
        print('添加代码错误：',fixurl)

def FindDirCode(url):
    try:
        os.chdir(url)
    except:
        return
    for new_dir in os.listdir(os.curdir):
        # print("文件名："+new_dir+'  路径：'+os.getcwd()+os.sep+new_dir)
        filepath=os.getcwd()+os.sep+new_dir
        filepath=filepath.replace('\\','/').rstrip()
        fty=filepath[-3:]
        if '.cs' in fty:
            filenamestr=new_dir.replace('.cs','')
            AddGaurdCode(filepath,filenamestr)
    exit()
def FixLog(textadd):
    path='d:/python/Log'
    logfile=os.path.exists(path)
    timeget=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    filepath=path+'/LogScrpt.txt'
    addcon='\n%s,%s'%(timeget,textadd)
    if not logfile:
        os.makedirs(path)
        tips=u'%s,日志：创建日志文件,%s'%(timeget,filepath)
        filecr=open(filepath,'w')
        filecr.write(tips+addcon)
        print(tips)
    else:
        filecr=open(filepath,'r')
        try:
            con=filecr.read()
            con=con+addcon
            filecr=open(filepath,'w')
            filecr.write(con)
            print('日志：写入日志成功')
        finally:
            filecr.close()


seturl=raw_input('请输入路径：')
print seturl
fixurl=str(seturl)
fixurl=fixurl.replace('\\','/').rstrip()
FindDir(fixurl) #添加注释
FindDirCode(fixurl) #添加代码