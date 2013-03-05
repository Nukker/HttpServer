# -*- coding: cp936 -*-
# Time:2012年12月12日 15:41:11
__author__ = 'Kun'

import os

#工作目录   dirname方法只兼容unix
workpath = "/root/kun/hs"

#资源根目录
apppath = workpath + os.path.sep + 'webapps'

#日志文件保存文件夹
logpath = workpath + os.path.sep + 'logs'


#服务器的端口与地址
PORT = 8080
HOST = 'localhost'

if __name__== '__main__':
    print 'workpath:', workpath
    print 'apppath:',apppath
    print 'logpath:',logpath
    print 'Port:',PORT
    print 'Host:',HOST