using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;
using System.Net;

enum HANDTYPE
{
    XYID_SRS_BEGIN = 10001,
    XYID_SRS_RESP_CONNECT,
    XYID_SRS_REQ_LOGIN,
    XYID_SRS_RESP_LOGIN,
    XYID_SRS_REQ_REGISTER,
    XYID_SRS_RESP_REGISTER,
}

public class ProtocolBase
{
    public ushort buflen;
    public ushort appid;
    public uint numid;
    public uint xyid;

    private ushort nowindex;
    private byte[] buf = new byte[2048];
    private List<byte> byteSource = new List<byte>();
    
    public static byte[] HexToByte(string hexString)
    {
        hexString = hexString.Replace(" ", "");
        if ((hexString.Length % 2) != 0)
            hexString += " ";
        byte[] returnBytes = new byte[hexString.Length / 2];
        for (int i = 0; i < returnBytes.Length; i++)
            returnBytes[i] = Convert.ToByte(hexString.Substring(i * 2, 2).Trim(), 16);
        return returnBytes;
    }

    public ProtocolBase()
    {
        this.buflen = 0;
        this.appid = 0;
        this.numid = 0;
        this.xyid = 0;
    }

    public static bool getProtolHand(byte[] buf,out ushort buflen,out ushort appid,out uint numid,out uint xyid)
    {
        buflen = 0;
        appid = 0;
        numid = 0;
        xyid = 0;
        if (buf.Length < 12)
            return false;
        buflen = System.BitConverter.ToUInt16(buf, 0);
        appid = System.BitConverter.ToUInt16(buf, 2);
        numid = System.BitConverter.ToUInt32(buf, 4);
        xyid = System.BitConverter.ToUInt32(buf, 8);
        return true;
    }

    //-------------------------------------------------------------------------------recv byte
    /// <summary>
    /// buf >> class
    /// 解析开始
    /// </summary>
    /// <param name="buf"></param>
    public void makeBegin(byte[] buf)
    {
        this.nowindex = 0;
        this.buf = buf;
        getHand();
    }

    /// <summary>
    /// buf >> class
    /// 解析协议头
    /// </summary>
    private void getHand()
    {
        if (this.buf.Length < nowindex + 12)
            throw new Exception("getHand len err");
        this.buflen = System.BitConverter.ToUInt16(this.buf, 0);
        this.appid = System.BitConverter.ToUInt16(this.buf, 2);
        this.numid = System.BitConverter.ToUInt32(this.buf, 4);
        this.xyid = System.BitConverter.ToUInt32(this.buf, 8);
        this.nowindex += 12;
    }

    public short getShort()
    {
        if (this.buf.Length < this.nowindex + 2)
            throw new Exception("getShort len err");
        short num = System.BitConverter.ToInt16(this.buf, this.nowindex);
        this.nowindex += 2;
        return num;
    }

    public ushort getUShort()
    {
        if (this.buf.Length < this.nowindex + 2)
            throw new Exception("getUShort len err");
        ushort num = System.BitConverter.ToUInt16(this.buf, this.nowindex);
        this.nowindex += 2;
        return num;
    }

    public int getInt()
    {
        if (this.buf.Length < this.nowindex + 4)
            throw new Exception("getInt len err");
        int num = System.BitConverter.ToInt32(this.buf, this.nowindex);
        this.nowindex += 4;
        return num;
    }

    public uint getUInt()
    {
        if (this.buf.Length < this.nowindex + 4)
            throw new Exception("getUInt len err");
        uint num = System.BitConverter.ToUInt32(this.buf, this.nowindex);
        this.nowindex += 4;
        return num;
    }

    /// <summary>
    /// buf >> class
    /// 解析string
    /// </summary>
    /// <returns></returns>
    public string getString()
    {
        ushort len = getUShort();
        if (this.buf.Length < this.nowindex + len)
            throw new Exception("getString len err");
        this.nowindex += len;
        return System.BitConverter.ToString(this.buf, nowindex, len);
    }

    //-------------------------------------------------------------------------------create byte
    /// <summary>
    /// class >> buf
    /// 打包开始
    /// </summary>
    public void packBegin()
    {
        this.nowindex = 0;
        this.byteSource.Clear();
        Array.Clear(buf, 0, buf.Length);
        packHand();
    }

    /// <summary>
    /// class >> buf
    /// 打包协议头
    /// </summary>
    private void packHand()
    {
        byteSource.AddRange(getFromUShort(this.buflen));
        byteSource.AddRange(getFromUShort(this.appid));
        byteSource.AddRange(getFromUInt(this.numid));
        byteSource.AddRange(getFromUInt(this.xyid));
    }

    public void packShort(short num)
    {
        byteSource.AddRange(getFromShort(num));
    }

    public void packUShort(ushort num)
    {
        byteSource.AddRange(getFromUShort(num));
    }

    public void packInt(int num)
    {
        byteSource.AddRange(getFromInt(num));
    }

    public void packUInt(uint num)
    {
        byteSource.AddRange(getFromUInt(num));
    }

    public void packString(string str)
    {
        byteSource.AddRange(getFromUShort((ushort)str.Length));
        byteSource.AddRange(getFromString(str));
    }

    /// <summary>
    /// class >> buf
    /// 打包结束
    /// </summary>
    /// <returns></returns>
    public byte[] packEnd()
    {
        this.buf = this.byteSource.ToArray();
        replaceHandLen();
        //加密
        string crystr = "";
        Crypt.encryptAES(this.buf, out crystr);
        byte[] len = getFromUShort((ushort)crystr.Length);
        byte[] crtbuf = UTF8Encoding.UTF8.GetBytes(crystr);
        byte[] endbuf = new byte[crtbuf.Length + 2];
        endbuf[0] = len[0];
        endbuf[1] = len[1];
        Array.Copy(crtbuf, 0, endbuf, 2, crtbuf.Length);
        this.buf = endbuf;
        return this.buf;
    }

    /// <summary>
    /// class >> buf
    /// 替换buf的包大小
    /// </summary>
    private void replaceHandLen()
    {
        byte[] lenBuf = getFromUShort(this.nowindex);
        for (int i = 0; i < 2; i++)
        {
            this.buf[i] = lenBuf[i];
        }
    }

    private byte[] getFromShort(short num)
    {
        this.nowindex += (ushort)Marshal.SizeOf(num);
        return BitConverter.GetBytes(num);
    }

    private byte[] getFromUShort(ushort num)
    {
        this.nowindex += (ushort)Marshal.SizeOf(num);
        return BitConverter.GetBytes(num);
    }

    private byte[] getFromUInt(uint num)
    {
        this.nowindex += (ushort)Marshal.SizeOf(num);
        return BitConverter.GetBytes(num);
    }

    private byte[] getFromInt(int num)
    {
        this.nowindex += (ushort)Marshal.SizeOf(num);
        return BitConverter.GetBytes(num);
    }

    private byte[] getFromString(string str)
    {
        this.nowindex += (ushort)str.Length;
        return System.Text.Encoding.Default.GetBytes(str);
    }
}

public class RespConnect : ProtocolBase
{
    public int connid;

    public RespConnect()
    {
        this.xyid = (uint)HANDTYPE.XYID_SRS_RESP_CONNECT;
        this.connid = 0;
    }

    public void make(byte[] buf)
    {
        makeBegin(buf);
        this.connid = getInt();
    }

    public byte[] pack()
    {
        packBegin();
        packInt(this.connid);
        return packEnd();
    }
}

public class ReqLogin : ProtocolBase
{
    public int connid;
    public string userid;
    public string password;

    public ReqLogin(int connid, string userid, string password)
    {
        this.xyid = (uint)HANDTYPE.XYID_SRS_REQ_LOGIN;
        this.connid = connid;
        this.userid = userid;
        this.password = password;
    }

    public void make(byte[] buf)
    {
        makeBegin(buf);
        this.connid = getInt();
        this.userid = getString();
        this.password = getString();
    }

    public byte[] pack()
    {
        packBegin();
        packInt(this.connid);
        packString(this.userid);
        packString(this.password);
        return packEnd();
    }
}

public class RespLogin : ProtocolBase
{
    enum FLAG
    {
        SUCCESS = 0,
        NOUSER = 1,
        PWDERR = 2,
        DBERR = 3,
    }

    public int connid;
    public int flag;
    public int numid;

    public RespLogin()
    {
        this.xyid = (uint)HANDTYPE.XYID_SRS_RESP_LOGIN;
        this.connid = 0;
        this.flag = (int)RespLogin.FLAG.SUCCESS;
        this.numid = 0;
    }

    public void make(byte[] buf)
    {
        makeBegin(buf);
        this.connid = getInt();
        this.flag = getInt();
        this.numid = getInt();
    }

    public byte[] pack()
    {
        packBegin();
        packInt(this.connid);
        packInt(this.flag);
        packInt(this.numid);
        return packEnd();
    }
}

public class ReqRegister : ProtocolBase
{
    public string userid;
    public string password;

    public ReqRegister(string userid, string password)
    {
        this.xyid = (uint)HANDTYPE.XYID_SRS_REQ_REGISTER;
        this.userid = userid;
        this.password = password;
    }

    public void make(byte[] buf)
    {
        makeBegin(buf);
        this.userid = getString();
        this.password = getString();
    }

    public byte[] pack()
    {
        packBegin();
        packString(this.userid);
        packString(this.password);
        return packEnd();
    }
}

public class RespRegister : ProtocolBase
{
    enum FLAG
    {
        SUCCESS = 0,
        USED_USERID = 1,
        DBERR = 2,
        CREATEERR = 3,
    }

    public int flag;
    public int numid;

    public RespRegister()
    {
        this.xyid = (uint)HANDTYPE.XYID_SRS_RESP_REGISTER;
        this.flag = (int)RespRegister.FLAG.SUCCESS;
        this.numid = 0;
    }

    public void make(byte[] buf)
    {
        makeBegin(buf);
        this.flag = getInt();
        this.numid = getInt();
    }

    public byte[] pack()
    {
        packBegin();
        packInt(this.flag);
        packInt(this.numid);
        return packEnd();
    }
}

