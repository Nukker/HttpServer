# -*- coding: cp936 -*-
# Time:2012��12��12�� 15:41:11
__author__ = 'Kun'

import os

#����Ŀ¼   dirname����ֻ����unix
workpath = "/root/kun/hs"

#��Դ��Ŀ¼
apppath = workpath + os.path.sep + 'webapps'

#��־�ļ������ļ���
logpath = workpath + os.path.sep + 'logs'


#�������Ķ˿����ַ
PORT = 8080
HOST = 'localhost'

if __name__== '__main__':
    print 'workpath:', workpath
    print 'apppath:',apppath
    print 'logpath:',logpath
    print 'Port:',PORT
    print 'Host:',HOST