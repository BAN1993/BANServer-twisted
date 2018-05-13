using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;
using System.Runtime.InteropServices;

namespace SocketClient
{
    class Program
    {
        private static byte[] result = new byte[1024];


        static void Main(string[] args)
        {
            Cryptor crypt = Cryptor.getInstance();
            crypt.setAESKey("SocketRouterSvr");

            //设定服务器IP地址
            IPAddress ip = IPAddress.Parse("127.0.0.1");
            Socket clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            try
            {
                clientSocket.Connect(new IPEndPoint(ip, 8300)); //配置服务器IP与端口
                Console.WriteLine("连接服务器成功");
            }
            catch
            {
                Console.WriteLine("连接服务器失败，请按回车键退出！");
                return;
            }

            //先收到RespConnect
            clientSocket.Receive(result);
            RespConnect respConnect = new RespConnect();
            respConnect.make(result);
            Console.WriteLine("收到:connid=" + respConnect.connid);

            {
                /*
                //测试注册
                ReqRegister pack = new ReqRegister("test05", "123456");
                byte[] buf = pack.pack();
                clientSocket.Send(buf);
                int receiveLength = clientSocket.Receive(result);
                respRegister resp = new respRegister();
                resp.make(result);
                Console.WriteLine("收到消息:flag=" + resp.flag + ",numid=" + resp.numid);
                */
            }

            {
                //测试登录
                ReqLogin pack = new ReqLogin(0,"test3003","123456");
                byte[] buf = pack.pack();
                clientSocket.Send(buf);
                int receiveLength = clientSocket.Receive(result);
                RespLogin resp = new RespLogin();
                resp.make(result);
                Console.WriteLine("收到消息:flag=" + resp.flag + ",numid=" + resp.numid);
            }

            Console.ReadKey();
        }

    }
}
