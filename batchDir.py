#! /usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
reload(sys) 
sys.setdefaultencoding("utf-8")

def removeSuffix(filePath):
    list = os.listdir(filePath)
    for path in list:
        path = os.path.join(filePath,path)
        if os.path.isdir(path):
            if path.endswith('.imageset'):
                newPath = path.replace('.imageset','')
                os.rename(path,newPath)
            else:
                removeSuffix(path)

def addSuffix(filePath):
    list = os.listdir(filePath)
    for path in list:
        path = os.path.join(filePath,path)
        if os.path.isdir(path):
            if not path.endswith('.imageset'):
                newPath = path+'.imageset'
                os.rename(path,newPath)
            addSuffix(path)


def main():
    argtype = sys.argv[1]
    filePath = sys.argv[2]
    if argtype == '-remove':
        removeSuffix(filePath)
    elif argtype == '-add':
        addSuffix(filePath)


if __name__ == "__main__":
    main()