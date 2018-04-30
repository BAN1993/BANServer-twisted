import struct

buf = struct.pack("H",123)
(num,) = struct.unpack("H",buf)
print(num,type(num))

buf2 = struct.pack("H",int(num))
(num2,) = struct.unpack("H",buf2)
print(num2)