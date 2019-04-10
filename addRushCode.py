#! /usr/bin/python
# -*- coding: UTF-8 -*-

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
import sqlite3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

import sys 
reload(sys) 
sys.setdefaultencoding("utf-8")

script_path = os.path.split(os.path.realpath(sys.argv[0]))[0]

#单词列表，用以随机名称
with open(os.path.join(script_path, "./word_list.json"), "r") as fileObj:
    word_name_list = json.load(fileObj)

with open(os.path.join(script_path, "./run.json"), "r") as runObj:
    run_list = json.load(runObj)

with open(os.path.join(script_path, "./nerb.json"), "r") as nObj:
    nerb_list = json.load(nObj)

with open(os.path.join(script_path, "./fileName.json"), "r") as filterFoldObj:
    fileNameFilterList = json.load(filterFoldObj)

inputTypeList = ["int","NSString","UIView","float","NSArray","NSDictionary"]

#初始化类
def initDataBase():
    conn = sqlite3.connect("class.db")
    #创建一个cursor：
    cursor = conn.cursor()
    #执行一条SQL语句：创建user表
    cursor.execute('create table classTable(className varchar(30),fatherClassName varchar(20))')
    cursor.execute('create table classProtery(className varchar(30),properName varchar(30),properType varchar(20))')
    cursor.execute('create table classMethod(className varchar(30),methodName varchar(30),methodReturnType varchar(20),methodInputType varchar(20),methodInputTypeIndex number,methodInputCount number,inputName varchar(20))')
    cursor.execute('create table classNeedImportClass (className varchar(30),classNeedName varchar(30))')
    cursor.close()
    conn.commit()
    conn.close()

#随机类名和基础属性
def randomClassNameAndProper():
    global inputTypeList
    #类名后缀
    classNameArr = ["Model","Tool","UIView","UIViewController"] 
    classFatherName = ["NSObject","NSObject","UIView","UIViewController"]
    #此处规定随机几个类文件
    count = 6
    #此处规定几个随机基础类型
    typeCount = 4
    #连接数据库
    conn = sqlite3.connect("class.db")
    cursor = conn.cursor()

    for i in range(0,count):
        for texIndex in range(0,len(classNameArr)):
                className = random.choice(nerb_list)+classNameArr[texIndex]
                cursor.execute('insert into classTable(className,fatherClassName) values(\"'+ className +"\",\""+classFatherName[texIndex]+"\")")
                for typeI in range(0,typeCount):
                    cursor.execute("insert into classProtery(className,properName,properType) values('"+ className + "','" + random.choice(word_name_list) +"','"+random.choice(inputTypeList)+"')")
    
    cursor.close()
    conn.commit()
    conn.close()

#随机含有类名的属性，以增加互通率
def randomClassProper():
    #此处规定随机几个互通类属性
    count = 2
     #连接数据库
    conn = sqlite3.connect("class.db")
    cursor = conn.cursor()
    cursor.execute('select className from classTable')
    #搜索到的所有随机类的名字
    classNameArr = cursor.fetchall()
    for className in classNameArr:
        sql = "insert into classProtery(className,properName,properType) values('"+ className[0] + "','" + random.choice(word_name_list) +"','"+random.choice(classNameArr)[0]+"')"
        cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()

#此处随机类的几个函数名
def randomMethod():
    global run_list
    global inputTypeList
    global word_name_list
    #此处规定一个类随机几个函数
    count = 5
    conn = sqlite3.connect("class.db")
    cursor = conn.cursor()
    cursor.execute('select className from classTable')
    classNameArr = cursor.fetchall()
    
    for className in classNameArr:
        for i in range(0,count):
            #随机函数需要几个参数

            methodName = random.choice(run_list)+random.choice(word_name_list).capitalize() + ":with" +random.choice(word_name_list).capitalize() +":with"+random.choice(word_name_list).capitalize()
            methodType = random.choice(classNameArr)[0] +":"+random.choice(classNameArr)[0]+":"+random.choice(classNameArr)[0]
            returnType = random.choice(inputTypeList)
            sql = "insert into classMethod(className,methodName,methodReturnType,methodInputType) values('" + className[0] + "','" +methodName+"','"+ returnType +"','"+methodType+"')"
            
            cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()

#随机函数内容字符串
def randomMethodStr(className):
    global inputTypeList
    #需要引入哪些类
    classNeedArr = [] 
    
    conn = sqlite3.connect("class.db")
    cursor = conn.cursor()
    #初始化函数
    cursor.execute("select properName,properType from classProtery where className = '"+className +"'")
    proNameArr = cursor.fetchall()
    initStr = "-(id)init{\n\tself = [super init];\n\tif(self){\n"
    for proName in proNameArr:
        initStr += "\t\tself." + proName[0] +" = "+ propertyInit(proName[1]) + ";\n"
        if proName[1] not in inputTypeList and proName[1] not in classNeedArr:
            classNeedArr.append(proName[1])
    initStr += "\t}\n\treturn self;\n}\n"
    cursor.execute("select methodName,methodReturnType,methodInputType from classMethod where className = '" + className +"'")
    classNameArr = cursor.fetchall()
    #制作基础函数
    methodStr  = "\n"
    for className in classNameArr:
        methodName = className[0].split(":")
        methodReturnType = className[1]
        methodInputType = className[2].split(":")
        inputName1 =  random.choice(word_name_list)
        inputName2 =  random.choice(word_name_list)
        inputName3 =  random.choice(word_name_list)
        #组成函数名字字符串
        methodStr += "-(" + returnTypeInit(methodReturnType) +")"+methodName[0]+":("+methodInputType[0]+"*) "+ inputName1 + " " +methodName[1] + ":(" +methodInputType[1]+"*) "+inputName2 + " "+methodName[2] + ":(" +methodInputType[2]+"*) "+inputName3+ "{\n"
        for kkk in methodInputType:
            if kkk not in classNeedArr:
                    classNeedArr.append(kkk)
        #给函数本体赋值
        #先随机一个属性直接赋值
        prop = random.choice(proNameArr)
        methodStr += "\tself."+prop[0]+" = " + propertyInit(prop[1]) +";\n"
        #然后随机一个基础类型交付给与
        nextPro = random.choice(proNameArr)
        cursor.execute("select methodName,methodInputType,className from classMethod where methodReturnType = '"+nextPro[1]+"'")
        nextPro_MethodNameArr = cursor.fetchall()

        if len(nextPro_MethodNameArr) >0:
            nextPro_method = random.choice(nextPro_MethodNameArr)
       
            next_PromethodName = nextPro_method[0].split(":")
            next_PromethodInputType = nextPro_method[1].split(":")
            next_PromethodClass = nextPro_method[2]
            next_proInputNmae = [random.choice(word_name_list),random.choice(word_name_list),random.choice(word_name_list)]
            for i in range(0,len(next_PromethodInputType)):
                methodStr += "\t"+next_PromethodInputType[i]+"* "+ next_proInputNmae[i] + " = " + propertyInit(next_PromethodInputType[i]) +";\n"
                if next_PromethodInputType[i] not in classNeedArr:
                    classNeedArr.append(next_PromethodInputType[i])
            classRname  = random.choice(word_name_list)
            methodStr += "\t" + next_PromethodClass + "* "+ classRname + " = " + propertyInit(next_PromethodClass) + ";\n"
            if next_PromethodClass not in classNeedArr:
                    classNeedArr.append(next_PromethodClass)
            methodStr += "\t[" +classRname+ " " + next_PromethodName[0]+ ":" + next_proInputNmae[0] + " " + next_PromethodName[1]+ ":" + next_proInputNmae[1] + " " + next_PromethodName[2]+ ":" + next_proInputNmae[2] + "];\n"
            
        else:#不是基础类型只能初始化了
            methodStr += "\tself."+nextPro[0]+" = " + propertyInit(nextPro[1]) +";\n"
            if nextPro[1] not in classNeedArr:
                classNeedArr.append(proName[1])
        methodStr += "\treturn " + propertyInit(methodReturnType) +";\n"
        methodStr += "}\n\n"
    cursor.close()
    conn.commit()
    conn.close()
    return [classNeedArr,initStr+methodStr]

def headerStrInit(className,classNeedArr):
    headerStr = "#import <Foundation/Foundation.h>\n"
    headerStr += "#import <UIKit/UIKit.h>\n"
    for classNeedName in classNeedArr:
        headerStr += "@class "+classNeedName+";\n"
    headerStr +="\n\n\n"
    conn = sqlite3.connect("class.db")
    cursor = conn.cursor()
    cursor.execute("select fatherClassName from classTable where className =='"+className+"'")
    fatherClassName = cursor.fetchall()
    headerStr += "@interface "+className+ " : " + fatherClassName[0][0] + "\n"
    cursor.execute("select properName,properType from classProtery where className = '"+className +"'")
    proArr = cursor.fetchall()
    for pro in proArr:
        headerStr += "@property (nonatomic) " + returnTypeInit(pro[1]) + "  " + pro[0] + ";\n"
    cursor.execute("select methodName,methodReturnType,methodInputType from classMethod where className = '" + className +"'")
    classNameArr = cursor.fetchall()
    #制作基础函数
    headerStr  += "\n"
    for className in classNameArr:
        methodName = className[0].split(":")
        methodReturnType = className[1]
        methodInputType = className[2].split(":")
        inputName1 =  random.choice(word_name_list)
        inputName2 =  random.choice(word_name_list)
        inputName3 =  random.choice(word_name_list)
        #组成函数名字字符串
        headerStr += "-(" + returnTypeInit(methodReturnType) +")"+methodName[0]+":("+methodInputType[0]+"*) "+ inputName1 + " " +methodName[1] + ":(" +methodInputType[1]+"*) "+inputName2 + " "+methodName[2] + ":(" +methodInputType[2]+"*) "+inputName3+ ";\n"
    headerStr += "@end"
    cursor.close()
    conn.commit()
    conn.close()
    return headerStr

def returnTypeInit(proType):
    if proType == "int":
        return proType
    elif proType == "NSString":
        return "NSString*"
    elif proType == "UIView":
        return "UIView*"
    elif proType == "float":
        return "float"
    elif proType == "NSArray":
        return "NSArray*"
    elif proType == "NSDictionary":
        return "NSDictionary*"
    else:
        return str(proType)+"*"

#inputTypeList = ["int","NSString*","UIView*","float","NSArray*","NSDictionary*"]
def propertyInit(proType):
    if proType == "int":
        return str(random.randint(1,100))
    elif proType == "NSString":
        return "@\""+random.choice(word_name_list)+"\""
    elif proType == "UIView":
        return "[[UIView alloc]initWithFrame:CGRectMake(" + str(random.randint(1,50))+ "," + str(random.randint(1,50)) + "," +  str(random.randint(1,50)) +","+ str(random.randint(1,50)) +")]"
    elif proType == "float":
        return str(random.random())
    elif proType == "NSArray":
        return "@[@\""+random.choice(word_name_list)+"\",@\""+random.choice(word_name_list) +"\"]"
    elif proType == "NSDictionary":
        return "[NSDictionary dictionary]"
    else:
        return "[["+proType+" alloc]init]"

#遍历函数
def classNameArrFromDB():
    conn = sqlite3.connect("class.db")
    cursor = conn.cursor()
    cursor.execute("select className from classTable")
    classNameArr = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return classNameArr

def createFileByClassName(path,className):
    headerFo = open(path+"/"+className+".h","w+")
    mmFo = open(path+"/"+className+".m","w+")
    list = randomMethodStr(className)
    beforeStr = "\n"
    for classNeedName in list[0]:
        beforeStr += "#import \""+classNeedName+".h\"\n"
    
    beforeStr += "#import \""+className+".h\"\n"

    beforeStr += "\n\n@implementation "+className+"\n\n"
    beforeStr += list[1]
    beforeStr += "\n\n@end"
    mmFo.write(beforeStr)
    headerStr = headerStrInit(className,list[0])
    headerFo.write(headerStr)
    headerFo.close()
    mmFo.close()
    

#查询数据库为了测试使用
def selDB():
    conn = sqlite3.connect("class.db")
    cursor = conn.cursor()
    cursor.execute('select *from classTable')
    #使用featchall获得结果集（list）
    values = cursor.fetchall()
    print("classTable:\n")
    print(values) 
    cursor.execute('select *from classProtery')
    #使用featchall获得结果集（list）
    propertyValues = cursor.fetchall()
    print("propertyValues:\n")
    print(propertyValues) 
    cursor.execute('select *from classMethod')
    #使用featchall获得结果集（list）
    propertyValues = cursor.fetchall()
    print("classMethodValues:\n")
    print(propertyValues) 
    cursor.close()
    conn.commit()
    conn.close()


def randomSomeMethod():
    #添加随机函数
    methodStr = "\n"
    #随机函数个数
    count = 10
    classNeedArr = []
    conn = sqlite3.connect("class.db")
    cursor = conn.cursor()
    for i in range(0,count):
        methodName = random.choice(run_list)+random.choice(nerb_list)
        methodStr += "-(void)"+methodName+"{\n"
        #函数内容 由二个随机值的和
        testType = random.choice(inputTypeList)
        cursor.execute("select methodName,methodInputType,className from classMethod where methodReturnType = '" + testType +"'")
        value = cursor.fetchall()
        methodList = [random.choice(value),random.choice(value)]
        tempValue = []
        for method in methodList:
            methodNameArr = method[0].split(":")
            methodInputArr = method[1].split(":")
            methodClassName = method[2]
            addClassNeedArr(classNeedArr,methodClassName)
            tempInputName = []
            #组合值得名字
            tempRandomValue = random.choice(word_name_list)
            tempValue.append(tempRandomValue)
            for methodInputType in methodInputArr:
                addClassNeedArr(classNeedArr,methodInputType)
                inputName = random.choice(word_name_list)
                tempInputName.append(inputName)
                methodStr += "\t"
                methodStr += returnTypeInit(methodInputType) + " " + inputName + " = " + propertyInit(methodInputType) +";\n"
                addClassNeedArr(classNeedArr,methodInputType)
            #调用函数的名字
            mainName = random.choice(word_name_list)
            methodStr += "\t"
            methodStr += returnTypeInit(methodClassName) + " " + mainName + " = " + propertyInit(methodClassName)+";\n"
            methodStr += "\t"
            methodStr += returnTypeInit(testType) + " " + tempRandomValue + "=[" +mainName + " "+methodNameArr[0]+":"+tempInputName[0]+" "+methodNameArr[1]+":"+tempInputName[1]+" "+methodNameArr[2]+":"+tempInputName[2]+"];\n"
        methodStr += "\t"
        methodStr += subNameValue(tempValue,testType)+";\n"
        methodStr += "}\n\n"
        classNeedStr = "#ifdef AIV3\n"
        for classNeed in classNeedArr:
            classNeedStr += "#import \""+classNeed+".h\"\n"
        classNeedStr += "#endif\n"
    return [classNeedStr,methodStr]

def subNameValue(arr,inputType):
    if inputType == "int":
        return  "int x="+arr[0]+"+"+arr[1]
    elif inputType == "NSString":
        return "NSLog(@\"%@%@\","+arr[0]+","+arr[1]+")"
    elif inputType == "UIView":
        return "["+arr[0]+" addSubview:"+arr[1]+"]"
    elif inputType == "float":
        return "float x="+arr[0]+"+"+arr[1]
    elif inputType == "NSArray":
        return "NSArray *x=@["+ arr[0]+","+arr[1]+"]"
    elif inputType == "NSDictionary":
        return "NSLog(@\"%@%@\","+arr[0]+","+arr[1]+")"
    else:
        return "[["+inputType+" alloc]init]"

def addClassNeedArr(arr,name):
    if name not in arr:
        arr.append(name)
    return arr

def findOCFileFromFold(filePath):
    global fileNameFilterList
    list = os.listdir(filePath)
    fileArr = []
    for path in list:
        path = os.path.join(filePath,path)
        if os.path.isdir(path):
            tempList = findOCFileFromFold(path)
            for tempPath in tempList:
                fileArr.append(tempPath)
        elif path.endswith('.m'):
            isHave = False
            fileName = path.split("/")[-1]
            for filterName in fileNameFilterList:
                if filterName in fileName:
                    isHave = True
            if isHave:
                pass
            else:
                fileArr.append(path)
    
    return fileArr

def main():
    filePath = sys.argv[1]
    os.remove("class.db")
    initDataBase()
    # randomClassNameAndProper()
    # randomClassProper()
    # randomMethod()
    # classNameArr  = classNameArrFromDB()
    # for className in classNameArr:
    #     createFileByClassName(script_path+"/test",className[0])
    # file_list = findOCFileFromFold(filePath)
    # for path in file_list:
    #     method = randomSomeMethod()
    #     fo = open(path,"r+")
    #     getStr = fo.read()
    #     fo.seek(0,0)
    #     getStr = method[0]+getStr
    #     tempStr = "#if AIV3"
    #     tempStr += method[1]
    #     tempStr += "#endif\n@end"

    #     count = getStr.rfind("@end")
    #     if count >0:
    #         getStr = getStr[0:count]
    #         getStr += tempStr
    #     print getStr
    #     fo.write(getStr)
    #selDB()


if __name__ == "__main__":
    main()