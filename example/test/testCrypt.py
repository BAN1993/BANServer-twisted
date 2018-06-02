import sys
sys.path.append("../base")

import Base
import CryptManager

gCrypt = CryptManager.CryptManager()
gCrypt.setAESKey("SocketRouterSvr")
outsre = gCrypt.encryptAES("abc123")
print(outsre)

instr = gCrypt.decryptAES(outsre)
print(instr)