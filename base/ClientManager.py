#encoding:utf-8

import sys
sys.path.append("../base")
import logging

import Base
import ServerInterface
import ConnectorClient

"""
    连接客户端管理类
    1.支持多个连接
"""

class ClientManager(ServerInterface.ClientBase):

    m_server = None
    m_reconnect = True

    m_mainAppid = 0
    m_allClientList = {} # [appid] = ConnectorClient 所有连接的列表
    m_sendClientList = {} # [appid] = ConnectorClient 有效连接的列表

    def __init__(self,server,reconnect=True):
        self.m_server = server
        self.m_reconnect = reconnect

    def setMainConnect(self,appid):
        """设置主连接"""
        self.m_mainAppid = appid

    def addConnect(self,appid,host,port):
        """默认设置第一个连接为主连接"""
        if self.m_mainAppid <= 0:
            self.m_mainAppid = appid

        if self.m_allClientList.has_key(appid):
            logging.warning("appid=%s is in list" % appid)
            return
        else:
            client = ConnectorClient.ConnectorClient(self)
            client.connect(appid,host,port)
            self.m_allClientList[appid] = client
    
    def connectSuccess(self,appid,client,flag):
        if flag:
            if self.m_sendClientList.has_key(appid):
                logging.warning("appid=%s is in send list" % appid)
            else:
                logging.info("add appid=%d to send list" % appid)
                self.m_sendClientList[appid] = client
        else:
            logging.error("can not connect to appid=%d" % appid)

    def connectLost(self,appid,client):
        if self.m_sendClientList.has_key(appid):
            logging.warning("appid=%d lose connect,move from send list" % appid)
            del self.m_sendClientList[appid]
        else:
            logging.warning("appid=%s lost connect,but not in send list" % appid)
        
        if self.m_reconnect:
            logging.info("appid=%d try reconnect" % appid)
            client.reConnect()
        
    def recvData(self,packlen,appid,srcappid,numid,xyid,data):
        self.m_server.recvData(packlen,appid,srcappid,numid,xyid,data)

    def sendData(self,buf,appid=0):
        """appid=0则往主连接发"""
        if appid != 0:
            if self.m_sendClientList.has_key(appid):
                self.m_sendClientList[appid].sendData(buf)
            else:
                logging.error("appid=%d not in send list" % appid)
        else:
            if self.m_sendClientList.has_key(self.m_mainAppid):
                self.m_sendClientList[self.m_mainAppid].sendData(buf)
            else:
                logging.error("mainappid=%d not in send list" % self.m_mainAppid)
