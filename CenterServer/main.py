#encoding:utf-8

import logging
import ConfigParser
import sys
sys.path.append("logic")

import Server
import log

if __name__ == '__main__':

    subtype = 1  # 默认为1
    if len(sys.argv) == 2:
        subtype = int(sys.argv[1])

    log.initLog("center", subtype)
    logging.info("subytype=%d" % subtype)
    conf = ConfigParser.ConfigParser()
    conf.read('config.ini')

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

