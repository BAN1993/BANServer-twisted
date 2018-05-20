#encoding:utf-8

import os
import logging
import logging.config
import time

def initLog(fname,subtype):
    if not os.path.exists('log'):
        os.mkdir("log")

    #直接通过代码初始化日志模块

    #日志格式
    fmt_str = '%(asctime)s[%(levelname)s][%(filename)s][%(funcName)s.%(lineno)d]%(message)s'
    fmt_date = '[%Y-%m-%d %H:%M:%S]'
    formatter = logging.Formatter(fmt_str,fmt_date)
    #日志文件名
    logfilename = 'log/%s%d.log' % (fname,subtype)

    timehandle = logging.handlers.TimedRotatingFileHandler(logfilename, when='midnight', interval=1, backupCount=10)
    timehandle.suffix = "%Y-%m-%d-%H%M%S.log"
    #timehandle.setLevel(logging.DEBUG)
    timehandle.setFormatter(formatter)
    timehandle.propagate = 0
    logging.getLogger('').addHandler(timehandle)

