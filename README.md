# iosMixTools
ios混淆脚本工具,主要用于游戏类。顺便安利一波:  [IOS马甲包混淆](https://blog.csdn.net/lyzz0612/article/details/80390362)    
有任何问题和建议欢迎联系： email: lyzz0612@qq.com

## Updated
这些工具用完目前还是2.1被拒, 4.3的可以尝试下；第三方加固工具试用版也被拒，目前在打算先用小游戏过审。

资源混淆感觉应该够了，但还是被4.3。这边用的游戏引擎代码基本没动，准备对它动刀了

* 定义宏加到代码不同地方，根据行号不同插入不同代码，可引入第三方库
    ```
    #define MIX_FUNC_1 {SOME CODE}
    #define MIX_FUNC(__LINE__) MIX_FUNC_##__LINE__
   ```

* 改写原有宏实现，如cocos引擎的CCASSERT,CCLOG
* 替换字符串，改为解密加密字符串

### Updated 2019/01/17
刚用小游戏提审过了，主要改地方是
1. 没加垃圾资源，但是把所有资源打成加密zip包+xor加密，启动时再解压执行。这样苹果机审应该不可能扫出重复资源来
2. 换iOS类名、函数名。原来只是加了垃圾函数，类名也只是加前缀，这次全换了完全不同的名字
3. 换机器打包、提审。本来公司就几台打包机器，提了很多次估计被标记了，一提就封号……这次是自己的电脑打包和提审的
4. 去掉热更联网检查，改为固定时间判断。原来是启动会检查更新，虽然提示是改成正在加载资源了，但有可能检测到网络数据了。这次直接固定提审1个月开放热更

## 

### 1.  addNative.py 生成oc垃圾代码工具
此脚本会扫描指定目录，给OC文件添加垃圾函数，同时创建垃圾文件到/trash目录。
#### 参数说明

* ` --oc_folder OC_FOLDER` OC_FOLDER为OC代码所在目录
* `--replace`替换OC_FOLDER下的原文件，同时原代码会备份到脚本目录下的backup_ios目录。不指定此项垃圾代码只会放到脚本目录下的target_ios/

addNative.py里还有一些配置可以看需求手动修改，如生成垃圾文件的数量，垃圾函数的数量，忽略文件列表等，具体请查看代码顶部相关注释

### 2. renameNative.py 修改类名前缀工具
类名是引用可能较为复杂的东西，工具批量替换的限制要求会比较多。如果你的项目满足以下条件，那么这个工具会比较适合你：

* 大部分类名都带相同的前缀，也只准备替换前缀；
* 大部分类都只在一个大文件夹下，它们之间相互引用，外部调用的情况较少并且你能很有把握的排除或手动替换它们；
* 类名和文件名一致；

本工具的流程是扫描指定文件夹，找到名称（或者说类名，工具假设两者是一致的）以指定前缀开始的文件；修改替换文件名前缀；并再次遍历此文件夹所有文件，将文件内容中的所有该名称也替换掉；替换xx.xcodeproj/project.pbxproj下的路径，省去在Xcode中手动添加文件（因为文件名修改了，不替换的话Xcode上还保持原来的名称会提示找不到文件）；同时为了防止文件夹名称跟文件名相同而导致替换project.pbxproj时将目录名也替换掉的情况，对文件夹名称也进行相同的流程。

#### 参数说明：

* `--add_prefix PREFIX` 添加类名前缀，有此项old_prefix和new_prefix将不起作用，此项请提前在renameNative.py文件中ignore_path_text添加不需要前缀的文件或路径
* `--old_prefix OLD_PREFIX` 替换前的类名前缀
* `--new_prefix NEW_PREFIX` 替换后的类名前缀
* `--ios_path IOS_PATH` OC文件目录
* `--proj_path PROJ_PATH ` xx.xcodeproj路径

运行示例：
`python renameNative.py --add_prefix ANDROID --ios_path xx/xx/xx/ --proj_path xx/xx/xx.xcodeproj`      
`python renameNative.py --old_prefix ANDROID --new_prefix IOS --ios_path xx/xx/xx/ --proj_path xx/xx/xx.xcodeproj`


### 3. autoBornCode.py 添加lua和png，修改资源文件MD5
此脚本会扫描指定文件夹，在路径包含/res的目录创建png, 其他地方创建lua。根据目录下的文件和文件夹数随机添加文件和子文件夹,创建数量是根据目录下原有文件和文件夹的数量随机。然后会给大部分类型资源文件添加一些无效内容来改变其MD5。

#### 参数说明

* `--res RESOURCE_DIR` 资源目录
* `--target TARGET_FOLDER` 可选参数，修改后的资源存放目录。不设置为脚本目录下的target_resource 

在代码的最前面有个匹配规则, path_exclude表示必须是不包含该字符串的路径才能创建该类型文件，path_include表示必须是包含该字符串的路径才要创建该类型文件
```
match_rule = {
    ".png": {
        "path_include": os.path.sep + "res",
    },
    ".lua": {
        # "path_include": "src",
        "path_exclude": os.path.sep + "res",
    },
}
```

**TODO**音效文件修改MD5值


### 4. iOS加固插件
[五款iOS加固产品测试与点评](http://telecom.chinabyte.com/300/14570300.shtml)

[加固产品比较](https://www.codercto.com/a/28193.html)

1. Obfuscator-LLVM

[Obfuscator-LLVM在iOS中的实践](https://www.jianshu.com/p/a631b5584de6)   
[obfuscator-llvm Github Installation](https://github.com/obfuscator-llvm/obfuscator/wiki/Installation)  
配置了一下，编译了好长时间发现支持的clang版本只到4.0，很多issue都没人管了，而且不支持字符串混淆，优点是开源，有空可以自己折腾一下

2. 网易的试用需要审核

[网易易盾](http://dun.163.com/product/ios-reinforce)

3. 顶象的试用插件有大概半个月的期限，~~只支持30%的加固，不过对我们提审的来说应该够了~~ 经试验试用版提审会被2.3.1拒绝，提示用了代码混淆

[顶象](https://www.dingxiang-inc.com/business/ios)     
[顶象文档](https://cdn.dingxiang-inc.com/public-service/docs/compiler-ios/) 


4. 几维安全、360都是在线加固的

[几维安全静态库](https://www.kiwisec.com/product/app-encrypt.html) 
[加固保iOS](http://jiagu.360.cn/#/app/android)

5. ~~数字盾甲，上传整包加固~~加固完成才发现下载需要支付，还以为免费试用的……感觉被骗了包一样

[数字盾甲](https://dun.shuzilm.cn/shield)







