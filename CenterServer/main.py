#encoding:utf-8

import logging
import ConfigParser
import sys
sys.path.append("logic")

import Server
import log

if __name__ == '__main__':

    log.initLog("logging.conf")
    conf = ConfigParser.ConfigParser()
    conf.read('config.ini')

    # TODO 为了方便,先写死subtype为1
    subtype = 1

    svr = None
    try:
        svr = Server.Server()
        svr.init(subtype,conf)
        svr.run()

    except BaseException as e:
        logging.exception(e)
        svr.stop()

    else:
        logging.error("Crash Unknown!")
        svr.stop()

