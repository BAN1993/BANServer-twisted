import os
import logging
import logging.config


def initLog(fname):
    if os.path.exists('log'):
        print "MyLog.init:log is exists"
    else:
        os.mkdir("log")

    # logging.basicConfig(level=logging.DEBUG,
    #    format='%(asctime)s[%(levelname)s][%(filename)s][%(funcName)s.%(lineno)d]%(message)s',
    #    datefmt='[%Y-%m-%d %H:%M:%S]',
    #    filename=('log/%s_%s.log' % (fname,time.strftime("%Y%m%d-%H%M%S",time.localtime()))),
    #    filemode='w')

    logging.config.fileConfig(fname)
