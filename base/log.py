#encoding:utf-8

import os
import logging
import logging.config
import time

def initLog(fname,subtype,level = logging.DEBUG):
    if not os.path.exists('log'):
        os.mkdir("log")

    #如果已经存在日志,则备份
    filename = "log/%s%d.log" % (fname,subtype)
    timestr = time.strftime("%Y-%m-%d-%H%M%S", time.localtime())
    newname = "%s.%s.log" % (filename,timestr)
    if os.path.isfile(filename):
        if os.access(filename,os.W_OK):
            os.rename(filename,newname)
        else:
            print("log file=%s is exist,buf can not write" % filename)

    #日志格式
    fmt_str = '%(asctime)s[%(levelname)s][%(filename)s(%(funcName)s)::%(lineno)d]%(message)s'
    fmt_date = '[%Y-%m-%d %H:%M:%S]'
    formatter = logging.Formatter(fmt_str,fmt_date)

    timehandle = logging.handlers.TimedRotatingFileHandler(filename, when='midnight', interval=1, backupCount=10)
    timehandle.suffix = "%Y-%m-%d-%H%M%S.log"
    timehandle.setFormatter(formatter)
    timehandle.propagate = 0

    logging.getLogger('').setLevel(level)
    logging.getLogger('').addHandler(timehandle)


