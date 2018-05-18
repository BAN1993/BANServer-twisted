using System.Net;
using System.Net.Sockets;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Text;
using System;


public delegate void RecvCallback(byte[] buf);

public class BaseSocket
{
    private RecvCallback m_recvCallback = null;
    private Socket m_socket = null;
    private byte[] m_buff = new byte[1024];
    private string m_poolBuf = "";

    public void connect(string ip,int port,RecvCallback cb)
    {
        Crypt.setAESKey("SocketRouterSvr");
        m_recvCallback = cb;

        m_socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        IPAddress address = IPAddress.Parse(ip);
        IPEndPoint ep = new IPEndPoint(address, port);
        m_socket.Connect(ep);
        m_socket.BeginReceive(m_buff, 0, m_buff.Length, SocketFlags.None, new System.AsyncCallback(ReceiveFromServer), m_socket);
    }

    void ReceiveFromServer(System.IAsyncResult ar)
    {
        //获取当前正在工作的Socket对象
        Socket worker = ar.AsyncState as Socket;
        int ByteRead = 0;
        try
        {
            //接收完毕消息后的字节数
            ByteRead = worker.EndReceive(ar);
        }
        catch (System.Exception ex)
        {
            Debug.LogError(ex.ToString());
        }
        if (ByteRead > 0)
        {
            string strbuf = Encoding.UTF8.GetString(m_buff).TrimEnd('\0');
            m_poolBuf = m_poolBuf + strbuf;
            string outstr;
            while (getPacketBuf(out outstr))
            {
                m_recvCallback(UTF8Encoding.UTF8.GetBytes(outstr));
            }
        }
        //继续异步等待接受服务器的返回消息
        worker.BeginReceive(m_buff, 0, m_buff.Length, SocketFlags.None, new System.AsyncCallback(ReceiveFromServer), worker);
    }

    public bool getPacketBuf(out string buf)
    {
        buf = "";
        if (m_poolBuf.Length < 2)
            return false;
        string lenstr = m_poolBuf.Substring(0, 2);
        ushort len = System.BitConverter.ToUInt16(UTF8Encoding.UTF8.GetBytes(lenstr), 0);
        byte[] packbuf = new byte[len];
        if (m_poolBuf.Length < len + 2)
            return false;
        Array.Copy(UTF8Encoding.UTF8.GetBytes(m_poolBuf), 2, packbuf, 0, len);
        Crypt.decryptAES(packbuf, out buf);

        int buflen = m_poolBuf.Length;
        if (buflen == len + 2)
        {
            m_poolBuf = "";
        }
        else
        {
            m_poolBuf = m_poolBuf.Substring(len + 2, buflen);
        }
        return true;
    }

    public void sendBuf(byte[] buf)
    {
        //clientSocket.BeginSend(sendData, 0, sendData.Length, SocketFlags.None, new System.AsyncCallback(SendToServer), clientSocket);
        m_socket.Send(buf);
    }
}
