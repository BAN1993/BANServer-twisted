#coding: utf8

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64
import hashlib
import logging

import Base

class CryptManager(object):
    m_AES_key = None
    m_AES_mode = AES.MODE_CBC
    m_AES_hadKey = False

    #def init(self, conf):
    #    """设置默认key"""
    #    key = str(conf.get("serverConfig", "aeskey"))
    #    self.setAESKey(key)

    def setAESKey(self, key):
        self.m_AES_key = CryptManager.prefKey(key)
        self.m_AES_hadKey = True

    @staticmethod
    def prefKey(key):
        retkey = str(key)
        if len(retkey)<16:
            add = 16 - len(retkey)
            retkey = retkey + ('\0' * add)
        elif len(retkey) > 16:
            retkey = retkey[0:15]
        return retkey

    def encryptAES(self, buf):
        if not self.m_AES_hadKey or not self.m_AES_key:
            raise Base.cryptException("Key is None")

        # 先base64，防止加解密后，去掉了多余的空导致协议解析失败
        text = base64.b64encode(buf)

        cryptor = AES.new(self.m_AES_key, self.m_AES_mode, self.m_AES_key)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)

        add = 0
        if (count % length) != 0:
            add = length - (count % length)
        text = text + ('\0' * add)

        ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(ciphertext)

    @staticmethod
    def encryptAESKey(key, buf, mod = AES.MODE_CBC):
        retkey =  CryptManager.prefKey(key)
        text = base64.b64encode(buf)
        cryptor = AES.new(retkey, mod, retkey)
        length = 16
        count = len(text)
        add = 0
        if (count % length) != 0:
            add = length - (count % length)
        text = text + ('\0' * add)
        ciphertext = cryptor.encrypt(text)
        return b2a_hex(ciphertext)

    def decryptAES(self, text):
        if not self.m_AES_hadKey or not self.m_AES_key:
            raise Base.cryptException("Key is None")

        cryptor = AES.new(self.m_AES_key, self.m_AES_mode, self.m_AES_key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        plain_text.rstrip('\0')
        buf = base64.b64decode(plain_text)
        return buf

    @staticmethod
    def decryptAESKey(key ,buf, mod = AES.MODE_CBC):
        retkey = CryptManager.prefKey(key)
        cryptor = AES.new(retkey, mod, retkey)
        plain_text = cryptor.decrypt(a2b_hex(buf))
        plain_text.rstrip('\0')
        buf = base64.b64decode(plain_text)
        return buf

    def md5(self, text):
        return hashlib.md5(str(text)).hexdigest()

#gCrypt = CryptManager()
