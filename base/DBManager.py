#encoding:utf-8

import MySQLdb
import logging

"""
    数据库管理类
    1.需要定时调用onTimer来保持连接
    2.查询用select,其他用querry
"""

class DBManager(object):
    m_ip = ''
    m_port = 0
    m_user = ''
    m_pwd = ''
    m_datatable = ''
    m_charset = ''

    dbConn = None
    isConnected = False
    reNowCount = 0 #距离上次ping的时间
    reConnTime = 60 # 60秒自动连接一次db

    def init(self, ip,port,user="root",pwd="123456",database="py_test",charset="utf8"):
        try:
            self.m_ip           = ip
            self.m_port         = port
            self.m_user         = user
            self.m_pwd          = pwd
            self.m_datatable    = database
            self.m_charset      = charset
            logging.info("ip=%s,port=%d,user=%s,pwd=%s,database=%s,charset=%s" % (self.m_ip, self.m_port, self.m_user, self.m_pwd, self.m_datatable, self.m_charset))
            self.dbConn = MySQLdb.Connect(host = self.m_ip,
                                          port = self.m_port,
                                          user = self.m_user,
                                          passwd = self.m_pwd,
                                          db = self.m_datatable,
                                          charset = self.m_charset)
            self.isConnected = True
            return True
        except BaseException as e:
            raise
    ## def init(self, ip, port, user, passwd, datatable):

    def mPing(self):
        if not self.dbConn or not self.isConnected:
            try:
                self.dbConn = MySQLdb.Connect(host=self.m_ip,
                                              port=self.m_port,
                                              user=self.m_user,
                                              passwd=self.m_pwd,
                                              db=self.m_datatable,
                                              charset='utf8')
                self.isConnected = True
            except BaseException as e:
                logging.exception(e)
                self.isConnected = False
                return
        # noinspection PyBroadException
        try:
            self.dbConn.ping()
        except:
            self.dbConn.ping(True)
    ## def mPing(self):

    def onTimer(self):
        self.reNowCount += 1
        if self.reNowCount % self.reConnTime == 0:
            self.mPing()
            self.reNowCount = 0
    ## def onTimer(self):

    def select(self, sqlstr = ''):
        if not self.isConnected:
            logging.error("db is not connected")
            return False, 0, []
        try:
            tmpCursor = self.dbConn.cursor()
            row = tmpCursor.execute(sqlstr)
            self.dbConn.commit()
            result = tmpCursor.fetchall()
            tmpCursor.close()
            return True, row, result
        except BaseException as e:
            logging.exception(e)
            tmpCursor.close()
            return False, 0, []
    ## def select(self, sqlstr = ''):

    def querry(self, sqlstr = ''):
        if not self.isConnected:
            logging.error("db is not connected")
            return False, 0, []
        try:
            tmpCursor = self.dbConn.cursor()
            row = tmpCursor.execute(sqlstr)
            self.dbConn.commit()
            result = tmpCursor.fetchall()
            tmpCursor.close()
            return True, row, result
        except BaseException as e:
            self.dbConn.rollback()
            tmpCursor.close()
            logging.exception(e)
            return False, 0, []
    ## def querry(self, sqlstr = ''):

gDBManager = DBManager()