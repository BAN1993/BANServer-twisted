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

            int connid = 0;
            {
                //先收到RespConnect
                clientSocket.Receive(result);
                ushort len = System.BitConverter.ToUInt16(result, 0);
                byte[] packbuf = new byte[len];
                Array.Copy(result, 2, packbuf, 0, len);
                string decstr = "";
                crypt.decryptAES(packbuf, out decstr);

                RespConnect respConnect = new RespConnect();
                respConnect.make(UTF8Encoding.UTF8.GetBytes(decstr));
                Console.WriteLine("连接回复:connid=" + respConnect.connid);
                connid = respConnect.connid;
            }

            {
                //测试登录
                ReqLogin pack = new ReqLogin(connid, "test3003", "123456");
                byte[] buf = pack.pack();
                clientSocket.Send(buf);

                int receiveLength = clientSocket.Receive(result);
                ushort len = System.BitConverter.ToUInt16(result, 0);
                byte[] packbuf = new byte[len];
                Array.Copy(result, 2, packbuf, 0, len);
                string decstr = "";
                crypt.decryptAES(packbuf, out decstr);

                RespLogin resp = new RespLogin();
                resp.make(UTF8Encoding.UTF8.GetBytes(decstr));
                Console.WriteLine("登录回复:flag=" + resp.flag + ",numid=" + resp.numid);
            }

            Console.ReadKey();
        }
    }
}
