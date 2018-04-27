
class A:

    def test(self):
        b = B(1,self.mycallback)

    def mycallback(self,flag):
        print("mycallback,flag=",flag)

class B:
    callback = None

    def __init__(self,num,callback):
        self.callback = callback
        print("num=",num)
        callback(num)

a = A()
a.test()