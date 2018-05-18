using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;

public class client : MonoBehaviour {

    private BaseSocket m_socket = new BaseSocket();
    private byte[] m_buff = new byte[1024];
    public bool IsConnected = false;


	// Use this for initialization
	void Start () {
        Debug.Log("client start");

        m_socket.connect("127.0.0.1", 8300, RecvCallback);
	}
	
	// Update is called once per frame
	void Update () {
		
	}

    void RecvCallback(byte[] buf)
    {
        ushort buflen = 0;
        ushort appid = 0;
        uint numid = 0;
        uint xyid = 0;

        if(ProtocolBase.getProtolHand(buf, out buflen, out appid, out numid, out xyid))
        {
            if(xyid == (uint)HANDTYPE.XYID_SRS_RESP_CONNECT)
            {
                RespConnect resp = new RespConnect();
                resp.make(buf);
                Debug.Log("连接回复:connid=" + resp.connid);

                ReqLogin req = new ReqLogin(resp.connid, "test3003", "123456");
                byte[] reqbuf = req.pack();
                m_socket.sendBuf(reqbuf);
                
            }
            else if(xyid == (uint)HANDTYPE.XYID_SRS_RESP_LOGIN)
            {
                RespLogin resp = new RespLogin();
                resp.make(buf);
                Debug.Log("登录回复:flag=" + resp.flag + ",numid=" + resp.numid);
            }
        }
        else
        {
            Debug.Log("解析协议头失败");
        }
    }

}
