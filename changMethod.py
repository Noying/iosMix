#! /usr/bin/python
# -*- coding: UTF-8 -*-
# 添加OC垃圾代码
import os,sys
import random
import string
import re
import md5
import time
import json
import shutil
import hashlib 
import time
import argparse

import sys 
reload(sys) 
sys.setdefaultencoding("utf-8")

script_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
#备份目录
backup_ios_folder = os.path.join(script_path, "./backup_ios")

#新建的头文件文件夹名
header_Path = script_path

with open(os.path.join(script_path, "./run.json"), "r") as fileObj:
    run_list = json.load(fileObj)

with open(os.path.join(script_path, "./nerb.json"), "r") as nerbObj:
    nerb_list = json.load(nerbObj)

with open(os.path.join(script_path, "./fiter.json"), "r") as fileObj1:
    sysFilter_list = json.load(fileObj1)

with open(os.path.join(script_path, "./filterMethod.json"), "r") as fileObj2:
    filterMethod_list = json.load(fileObj2)


with open(os.path.join(script_path, "./fileName.json"), "r") as filterFoldObj:
    fileNameFilterList = json.load(filterFoldObj)

def randomMethodName():
    global run_list
    global nerb_list
    return random.choice(run_list) + random.choice(nerb_list).capitalize()

def createHeaderFile(fileName):
     headerPath = "Ry" + fileName + ".h"
     return headerPath

def createHeaderFoldPath(foldPath):
    global header_Path
    headerFoldPath = os.path.join(foldPath,"ryHeaderFold")
    if(os.path.exists(headerFoldPath)):
        pass
    else:
        os.mkdir(headerFoldPath)
    header_Path = headerFoldPath

def searchMethodAndWriteToPath(filePath):
    global header_Path
    global filterMethod_list
    global sysFilter_list
    global fileNameFilterList
    arr = []
    fo = open(filePath,'r')
    fileName = filePath.split('/')[-1]
    fileName = fileName.split('.')[0]
    #看看是否需要过滤该文件
    for filterName in fileNameFilterList:
        if filterName in fileName:
            return

    fw = open(header_Path+"/"+createHeaderFile(fileName),"w") #创建头文件
    try:
        for line in fo:
         # 去除空格,换行符,制表符
            line = "".join(line.split())
            if line.startswith('+(') or line.startswith('-('):
                line = line.split('{')[0]
                line = line.split(':')[0]
                line = line.split(')')[-1]
                # 过滤
                if line in sysFilter_list:
                    continue
                if line in filterMethod_list:
                    continue
                if line in arr:
                    continue
                randomMethod = randomMethodName()
                arr.append(line)
                fw.write("#define " + line + " " + randomMethod + "\n")
        fo.close()
        fw.close()
    finally:
        fo.close()
        fw.close()
     #在.h文件头加入目前的.h文件
    headerPath =  filePath.replace('.m','.h')
    if os.path.exists(headerPath):
        fh = open(headerPath,"r+")
        content = fh.read()
        fh.seek(0,0)
        fh.write("#ifdef AIV3\n#include\""+createHeaderFile(fileName)+"\"\n#endif\n"+content)
        fh.close()

def findOCFileFromFold(filePath):
    list = os.listdir(filePath)
    fileArr = []
    for path in list:
        path = os.path.join(filePath,path)
        
        if os.path.isdir(path):
            tempList = findOCFileFromFold(path)
            for tempPath in tempList:
                fileArr.append(tempPath)
        elif path.endswith('.m'):
            fileArr.append(path)
    return fileArr

def main():
    foldPath =  sys.argv[1]
    createHeaderFoldPath(foldPath)
    file_list = findOCFileFromFold(foldPath)
    for path in file_list:
        searchMethodAndWriteToPath(path)

if __name__ == "__main__":
    main()
    