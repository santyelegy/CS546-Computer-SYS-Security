import random

"""
  -128,          /* Overflow signed 8-bit when decremented  */ \
  -1,            /*                                         */ \
   0,            /*                                         */ \
   1,            /*                                         */ \
   16,           /* One-off with common buffer size         */ \
   32,           /* One-off with common buffer size         */ \
   64,           /* One-off with common buffer size         */ \
   100,          /* One-off with common buffer size         */ \
   127           /* Overflow signed 8-bit when incremented  */
"""
INTERESTING_8=[-128,-1,0,1,16,32,64,100,127]

"""
#define INTERESTING_16 \
  -32768,        /* Overflow signed 16-bit when decremented */ \
  -129,          /* Overflow signed 8-bit                   */ \
   128,          /* Overflow signed 8-bit                   */ \
   255,          /* Overflow unsig 8-bit when incremented   */ \
   256,          /* Overflow unsig 8-bit                    */ \
   512,          /* One-off with common buffer size         */ \
   1000,         /* One-off with common buffer size         */ \
   1024,         /* One-off with common buffer size         */ \
   4096,         /* One-off with common buffer size         */ \
   32767         /* Overflow signed 16-bit when incremented */
"""

INTERESTING_16=[-32768,-129,128,255,256,512,1000,1024,4096,32767]
"""
#define INTERESTING_32 \
  -2147483648LL, /* Overflow signed 32-bit when decremented */ \
  -100663046,    /* Large negative number (endian-agnostic) */ \
  -32769,        /* Overflow signed 16-bit                  */ \
   32768,        /* Overflow signed 16-bit                  */ \
   65535,        /* Overflow unsig 16-bit when incremented  */ \
   65536,        /* Overflow unsig 16 bit                   */ \
   100663045,    /* Large positive number (endian-agnostic) */ \
   2147483647    /* Overflow signed 32-bit when incremented */
"""

INTERESTING_32=[-2147483648,-100663046,-32769,32768,65535,65536,100663045,2147483647]

# replace a random byte in buff with a random interesting value
def interesting_8(buff:bytearray)->bytearray:
    index=random.randint(0,len(buff)-1)
    buff[index]=bytearray(INTERESTING_8[random.randint(0,len(INTERESTING_8)-1)].to_bytes(1,byteorder='big', signed=True))[0]
    return buff

# buff is guaranteed to be at least 2 bytes long
def interesting_16(buff:bytearray)->bytearray:
    index=random.randint(0,len(buff)-2)
    buff=buff[:index]+bytearray(INTERESTING_16[random.randint(0,len(INTERESTING_16)-1)].to_bytes(2,byteorder='big', signed=True))+buff[index+2:]
    return buff

# buff is guaranteed to be at least 4 bytes long
def interesting_32(buff:bytearray)->bytearray:
    index=random.randint(0,len(buff)-4)
    buff=buff[:index]+bytearray(INTERESTING_32[random.randint(0,len(INTERESTING_32)-1)].to_bytes(4,byteorder='big', signed=True))+buff[index+4:]
    return buff