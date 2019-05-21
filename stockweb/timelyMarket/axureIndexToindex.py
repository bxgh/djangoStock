#-*-coding:utf8-*-
import re
import os

#功能：修改axure生成的index.html文件，增加静态文件路径
PRO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #设置项目根目录
APP_DIR = os.path.dirname(os.path.abspath(__file__))                  #设置应用根目录
axureIndexFilename=APP_DIR+'/static/index.html'                       #axure生成的index.html文件
appIdexFilename=APP_DIR+'/templates/timelyMarket/index1.html'
#一、读取axure编辑的index.html文件
htmlf=open(axureIndexFilename,'r',encoding="utf-8")                   #读取axure编辑的index.html文件
content=htmlf.read()
#二、修改相关节点路径，添加static路径
scripts = re.findall(r'(?<=src=\").+?(?=")', content, re.I)           #用正则表达式查找修改静态文件路径：src节点
scripts = list(set(scripts))                                          #去重
for script in scripts:                                                #执行修改
    replScript="{% static '"+script+"' %}"    
    content=content.replace(script,replScript)
hrefs = re.findall(r'(?<=href=\").+?(?=")', content, re.I)           #用正则表达式查找修改静态文件路径：href节点
hrefs=list(set(hrefs))                                               #执行修改
for href in hrefs:
    replhref="{% static '"+href+"' %}"
    content=content.replace(href,replhref)    
#三、html尾部添加js自定义程序
content=content.replace('<head>','<head>   {% load static %}')     #添加static声明
content=content.replace('</body>','')                              #html尾部添加js程序
content=content.replace('</html>','')
bottomFilename=APP_DIR+'/templates/timelyMarket/bottom.html'       #尾部自定义js程序文件 
bottomhtml=open(bottomFilename,'r',encoding="utf-8") 
bottomContent=bottomhtml.read()
content=content+bottomContent

klinecssFilename=APP_DIR+'/templates/timelyMarket/klinecss.html'
csshtml=open(klinecssFilename,'r',encoding="utf-8") 
cssContent=csshtml.read()
content=content.replace('</head>',cssContent)  


htmlf.close()
bottomhtml.close()
#四、修改后的html文件替换正式index.html
with open(appIdexFilename,'w',encoding= 'UTF-8')as f:              #自定义程序写入index.html
    f.write(content)
    
