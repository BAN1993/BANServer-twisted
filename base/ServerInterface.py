#encoding:utf-8

from abc import ABCMeta, abstractmethod

class ServerBase(object):
    """
    server基类
    所有server都要继承并实现
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def newClient(self,conn):
        """
        新的客户端连接
        :param conn: ConnectServerProtocl
        :return: void
        """
        pass

    @abstractmethod
    def recvFromClient(self,conn,data):
        """
        收到消息
        :param conn: ConnectServerProtocl
        :param data: buf
        :return: void
        """
        pass

    @abstractmethod
    def loseClient(self,conn):
        """
        与客户端失去连接
        :param conn: ConnectServerProtocl
        :return: void
        """
        pass

class ClientBase(object):
    """
    client基类
    若要连接其他服务,则应该继承和实现此类
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def connectSuccess(self,appid,client):
        """
        成功连接到server
        :param appid: server id
        :param conn: ConnectorClient
        :return: void
        """
        pass

    @abstractmethod
    def lostServer(self,appipd,conn):
        """
        失去和server的连接
        :param appid: server id
        :param conn: ConnectClientProtocl
        :return: void
        """
        pass

    @abstractmethod
    def recvFromServer(self,appid,conn,data):
        """
        收到server的消息
        :param appid: server id
        :param conn: ConnectClientProtocl
        :param data: buf
        :return: void
        """
        pass



