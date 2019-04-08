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

#脚本路径
script_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
#过滤文本保存地址
filterMethodPath = script_path + "/filterMethod.json"

#获取文件里面已经包含的数组
with open(os.path.join(script_path, "./filterMethod.json"), "r") as fileObj:
    filterMethodArr = json.load(fileObj)

def frameworkPathList(foldPath):
    list = os.listdir(foldPath)
    frameworkList = []
    for i in range(0,len(list)):
        path = os.path.join(foldPath,list[i])
        if os.path.isdir(path) and path.strip().endswith(".framework"):
               #你想对文件的操作
                frameworkList.append(path)
        elif os.path.isdir(path):
            tempList = frameworkPathList(path)
            for pathName in tempList:
                frameworkList.append(pathName)
    return frameworkList

def frameworkHeaderList(frameworkList):
    headerPathList = []
    for frameName in frameworkList:
        headerFoldPath = frameName + "/Headers"
        if os.path.isdir(headerFoldPath):
            headerList = os.listdir(headerFoldPath)
            for headerPath in headerList:
                 if headerPath.endswith('.h'):
                    headerPath = frameName + "/Headers/" +headerPath
                    headerPathList.append(headerPath)
    return headerPathList

def foldHeaderList(foldPath):
    headerPathList = []
    list = os.listdir(foldPath)
    for i in range(0,len(list)):
        path = os.path.join(foldPath,list[i])
        if os.path.isdir(path):
            tempList = foldHeaderList(path)
            for headerPath in tempList:
                headerPathList.append(headerPath)
        elif path.endswith('.h'):
            headerPathList.append(path)
    return headerPathList



def readHeaderFindFilter(headerList):
    global filterMethodArr
    for headerPath in headerList:
        isprotocol = False
        fo = open(headerPath,'r')
        try:
            for line in fo:
                line = "".join(line.split()) #去掉空制符号
                if isprotocol: #如果处于读取代理函数中
                    if line.startswith('+(') or line.startswith('-('):
                         line = line.split(';')[0]
                         line = line.split(':')[0]
                         line = line.split(')')[-1]
                         if line not in filterMethodArr:
                            filterMethodArr.append(line)
                    if line.startswith('@end'):
                        isprotocol = False
                else: #如果不处于读取代理函数中
                    if line.startswith("@protocol"):
                        isprotocol = True
                        
        finally:
            fo.close()
        fo.close()
    return filterMethodArr


def main():
    global filterMethodPath
    foldPath = sys.argv[1]
    frameworkList = frameworkPathList(foldPath)
    headerList = frameworkHeaderList(frameworkList)
    tempList = foldHeaderList(foldPath)
    for path in tempList:
        headerList.append(path)
    filterArr = readHeaderFindFilter(headerList)
    fo = open(filterMethodPath,'wr')
    json.dump(filterArr,fo)
    fo.close()

if __name__ == "__main__":
    main()

