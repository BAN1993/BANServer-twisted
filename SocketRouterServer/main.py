#encoding:utf-8

import logging
import ConfigParser
import sys
sys.path.append("logic")
sys.path.append("..")

import Server
import log

if __name__ == '__main__':

	log.initLog("logging.conf")
	conf = ConfigParser.ConfigParser()
	conf.read('config.ini')

	try:
		svr = Server.Server(conf)
		svr.run()
	except BaseException as e:
		logging.exception(e)
		exit()
	else:
		logging.error("Crash Unknown!")
		exit()

