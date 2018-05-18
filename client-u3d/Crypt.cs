using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Text;
using System.Security.Cryptography;
using System;

public static class Crypt
{

    private static bool m_AES_hadKey;
    private static byte[] m_AES_key = new byte[16];

    public static void setAESKey(string key)
    {
        //让key合法
        if (key.Length > 16)
            return;
        if (key.Length < 16)
            key = key.PadRight(16, '\0');

        m_AES_key = UTF8Encoding.UTF8.GetBytes(key);
        m_AES_hadKey = true;
    }

    public static bool encryptAES(byte[] src, out string outstring)
    {
        outstring = "";
        if (!m_AES_hadKey)
            return false;

        //先base64编码
        string base64str = Convert.ToBase64String(src);

        //长度不足填充\0
        if (base64str.Length % 16 != 0)
        {
            int add = 16 - (base64str.Length % 16);
            base64str = base64str.PadRight(base64str.Length + add, '\0');
        }

        byte[] toEncryptArray = UTF8Encoding.UTF8.GetBytes(base64str);
        RijndaelManaged rDel = new RijndaelManaged();
        rDel.Key = m_AES_key;
        rDel.IV = m_AES_key;
        rDel.Mode = CipherMode.CBC;
        rDel.Padding = PaddingMode.None;
        ICryptoTransform cTransform = rDel.CreateEncryptor();
        byte[] resultArray = cTransform.TransformFinalBlock(toEncryptArray, 0, toEncryptArray.Length);

        //返回16进制
        outstring = ByteToHex(resultArray);
        return true;
    }

    public static bool decryptAES(byte[] src, out string outstring)
    {
        outstring = "";
        if (!m_AES_hadKey)
            return false;

        //先从16进制转换到byte
        string srcstring = UTF8Encoding.UTF8.GetString(src);
        byte[] srcbyte = HexToByte(srcstring);

        RijndaelManaged rDel = new RijndaelManaged();
        rDel.Key = m_AES_key;
        rDel.IV = m_AES_key;
        rDel.Mode = CipherMode.CBC;
        rDel.Padding = PaddingMode.Zeros;
        ICryptoTransform cTransform = rDel.CreateDecryptor();
        byte[] resultArray = cTransform.TransformFinalBlock(srcbyte, 0, srcbyte.Length);
        string resultstring = UTF8Encoding.UTF8.GetString(resultArray);
        resultstring = resultstring.TrimEnd('\0');

        //Base64解码
        byte[] outbyte = Convert.FromBase64CharArray(resultstring.ToCharArray(), 0, resultstring.ToCharArray().Length);
        outstring = UTF8Encoding.UTF8.GetString(outbyte);
        return true;
    }

    public static string ByteToHex(byte[] bytes)
    {
        string returnStr = "";
        if (bytes != null)
        {
            for (int i = 0; i < bytes.Length; i++)
            {
                returnStr += bytes[i].ToString("X2").ToLower();
            }
        }
        return returnStr;
    }

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
}