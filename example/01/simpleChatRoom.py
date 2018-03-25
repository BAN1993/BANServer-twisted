# -*- coding:utf-8 -*-
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
user = {}
class ChatReci(LineReceiver):             #定义一个类,这里继承的是LineReceiver
    def __init__(self):                    #初始化2个变量
        self.name = ''
        self.state = "game"

    def connectionMade(self):                     #连接协议，当客户端连接即发出消息
        self.sendLine("input you  name?")

    def lineReceived(self, data):                 #这个函数定义了取名 打印欢迎界面，以及发送信息给连上来的用户
        if self.name == '':                       #判断名字是否为空  如果为空就进行下面的操作
            self.name = data                       #给self.name赋值
            self.sendLine("you welcome, %s!" % (self.name))       #打印欢迎信息
            user[self.name] = self                 #赋值给user
            print '%s loging' %data              #打印登录信息
        else:                                       #不为空就打印信息
            message = "<%s> %s" % (self.name, data)   #定义聊天信息
            for ur,protocol in user.items():          #取他的用户名
                if protocol != user:                   #判断他是不是一个用户 如果不是就传送消息
                    protocol.sendLine(message)         #传送消息

factory = Factory()              #定义工厂
factory.protocol = ChatReci      #绑定我的类
reactor.listenTCP(22222, factory)   #绑定端口和工厂
reactor.run()                            #启动