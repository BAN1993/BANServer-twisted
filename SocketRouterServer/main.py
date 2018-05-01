#encoding:utf-8

import logging
import ConfigParser
import sys
sys.path.append("logic")
sys.path.append("..")

import Base
import Server
import log

if __name__ == '__main__':

    log.initLog("logging.conf")
    conf = ConfigParser.ConfigParser()
    conf.read('config.ini')

    subtype = 1 # 默认为1
    if len(sys.argv) == 2:
        subtype = int(sys.argv[1])
    logging.info("subytype=%d" % subtype)

    svr = Server.Server()
    try:
        svr.init(subtype,conf)
        svr.run()
    except BaseException as e:
        logging.exception(e)
        svr.stop()
    else:
        logging.error("Crash Unknown!")
        svr.stop()

