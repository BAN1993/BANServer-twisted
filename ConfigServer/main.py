#encoding:utf-8

import logging
import ConfigParser
import sys
sys.path.append("logic")

import Server
import log

if __name__ == '__main__':

    log.initLog("config", 1)
    conf = ConfigParser.ConfigParser()
    conf.read('config.ini')

    svr = None
    try:
        svr = Server.Server()
        svr.init(conf)
        svr.run()

    except BaseException as e:
        logging.exception(e)
        svr.stop()

    else:
        logging.error("Crash Unknown!")
        svr.stop()

