#! /usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import shutil
reload(sys) 
sys.setdefaultencoding("utf-8")


def moveOut(needMovePath,moveOutPath):
    list = os.listdir(needMovePath)
    for path in list:
        filePath = os.path.join(needMovePath,path)
        if os.path.isfile(filePath):
            if path.endswith('.png') or path.endswith('.jpg'):  
                dstfilePath = os.path.join(moveOutPath,path)
                shutil.copyfile(filePath,dstfilePath)
        else:
            moveOut(filePath,moveOutPath)

def moveIn(needMovePath,moveInPath):
    list = os.listdir(needMovePath)
    for path in list:
        filePath = os.path.join(needMovePath,path)
        if os.path.isfile(filePath):
            if path.endswith('.png') or path.endswith('.jpg'):  
                dstfilePath = findFilePath(moveInPath,path)
                if dstfilePath not in "not find":
                    os.remove(dstfilePath)
                    shutil.copyfile(filePath,dstfilePath)
        else:
            moveOut(filePath,moveInPath)


def findFilePath(moveInPath,fileName):
    arr = []
    batchAllFile(moveInPath,arr)
    for path in arr:
        if fileName in path:
            return path
    return "not find"

def batchAllFile(moveInPath,arr):
    list = os.listdir(moveInPath)
    for path in list:
        filePath = os.path.join(moveInPath,path)
        if os.path.isfile(filePath):
            if path.endswith('.png') or path.endswith('.jpg'):  
                arr.append(filePath)
        else:
            batchAllFile(filePath,arr)


def main():
    argtype = sys.argv[1]
    if argtype == '-moveOut':
        needMovePath = sys.argv[2]
        moveOutPath = sys.argv[3]
        moveOut(needMovePath,moveOutPath)
    elif argtype == '-moveIn':
        needMovePath = sys.argv[2]
        moveInPath = sys.argv[3]
        moveIn(needMovePath,moveInPath)


if __name__ == "__main__":
    main()