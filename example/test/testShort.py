import struct

buflen = 1
appid = 1100
xyid = 10002
numid = 40000000
bs_buf = struct.pack("HHII", buflen,appid,xyid,numid)
print bs_buf

(a,b,c,d,) = struct.unpack("HHII",bs_buf)
print a,b,c,d