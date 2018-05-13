import sys
sys.path.append("../base")

import Base
from CryptManager import gCrypt

gCrypt.setAESKey("SocketRouterSvr")
outsre = gCrypt.encryptAES("abc123")
print(outsre)

instr = gCrypt.decryptAES(outsre)
print(instr)