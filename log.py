# -*- coding: utf-8 -*-
# Time:2012��12��12�� 17:11:45
__author__ = 'Kun'

import os,datetime,sys

try:
    import config
except ImportError:
    print 'Can\'t find the config file!!'
    sys.exit(0)

def get_log_filename():
    return datetime.datetime.now().strftime('server.%Y-%m-%d-%H-%M-%S.log')

class log():
    ######��־����######
    def __init__(self):
        self.log_file_path = config.logpath
        self.log_file = config.logpath + os.sep + get_log_filename()
        print self.log_file
        if not os.path.exists(self.log_file_path):
            os.makedirs(self.log_file_path)

    def write(self,msg):
        self.file = open(self.log_file,'ab')
        self.file.write(msg)
        self.file.close()
        print msg

    def info(self, msg):
        msg = self.getTime() + ' [INFO] ' + msg
        self.write(msg)

    def error(self, msg):
        msg = self.getTime() + ' [ERROR] ' + msg
        self.write(msg)

    def warning(self, msg):
        msg = self.getTime() + ' [WARNING] ' + msg
        self.write(msg)

    def getTime(self):
        return datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')


if __name__ == '__main__':
    log = log()
    log.info('helloboy\n')
    log.error('testerror\n')
