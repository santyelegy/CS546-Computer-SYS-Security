# requires python version>3.9
import random
import string
import ctypes
import interesting_val
#out_buf
#in_buf

HAVOC_STACK_POW2=7
HAVOC_BLK_SMALL=32
HAVOC_BLK_MEDIUM=128
HAVOC_BLK_LARGE=1500

ARITH_MAX=35

# assume max >1
# return range: 1 ~ max
def choose_block_len(max,round)->int:
    case_max=0
    if round>10000:
       case_max+=1
    if round>10000000:
       case_max+=1
    case=random.randint(0,case_max)
    if case==0:
        min_value = 1
        max_value = HAVOC_BLK_SMALL
    elif case==1:
        min_value = HAVOC_BLK_SMALL
        max_value = HAVOC_BLK_MEDIUM
    elif case==2:
        min_value = HAVOC_BLK_MEDIUM
        max_value = HAVOC_BLK_LARGE
    if min_value>max:
        min_value=1
    return  min_value+ random.randint(0,min(max_value, max) - min_value)

def rand_char()->bytes:
    #return random.choice(string.ascii_letters ).encode()
    return random.choice(string.ascii_letters+ string.digits + string.punctuation).encode()

# ignore overflow
def add_byte(original:int,value:int)->int:
    return (original+value)%256


def rand_byte()->bytes:
    return random.randbytes(1)
### still need to implement, AFL use very complex mutation
# byte flips, arithmetics, known ints, havoc, trim
# interesting value, ineresting value with random endian

# Its quite strange there are very few insersion in the mutating process
def mutate_one(buff:bytes,use_char:bool,round:int)->bytes:
    buff=bytearray(buff)
    if use_char:
        mutator=rand_char
    else:
        mutator=rand_byte
    # avoid index out of range
    avaliable_list=[13]
    # TODO: before exhausted, only do bit flip, arith, interesting value
    # TODO: after exhausted, do splice
    if len(buff)>0:
        avaliable_list.extend([0,1,4,5,10,11,12,13])
    elif len(buff)>2:
        avaliable_list.extend([2,6,7,14])
    elif len(buff)>4:
        avaliable_list.extend([3,8,9])
    case=random.choice(avaliable_list)

    # start the switch statement
    if case==0:
        # bit filp
        bit_index=random.randint(0,6)
        mask=1<<bit_index
        index=random.randint(0,len(buff)-1)
        buff[index]^=mask
    elif case==1:
        # set byte to interesting value
        buff=interesting_val.interesting_8(buff)
    elif case==2:
        # set word to interesting value
        buff=interesting_val.intersting_16(buff)
    elif case==3:
        # set double word to interesting value
        buff=interesting_val.intersting_32(buff)
    elif case==4:
        # subtract from byte (1,ARITH_MAX)
        index=random.randint(0,len(buff)-1)
        buff[index]=add_byte(buff[index],-random.randint(1,ARITH_MAX))
    elif case==5:
        # add to byte (1,ARITH_MAX)
        index=random.randint(0,len(buff)-1)
        buff[index]=add_byte(buff[index],random.randint(1,ARITH_MAX))
    elif case==6:
        # subtract from word, random endian
        index=random.randint(0,int(len(buff)/2)-1)*2+1
        buff[index]=add_byte(buff[index],-random.randint(1,ARITH_MAX))
    elif case==7:
        # add from word, random endian
        index=random.randint(0,int(len(buff)/2)-1)*2+1
        buff[index]=add_byte(buff[index],random.randint(1,ARITH_MAX))
    elif case==8:
        # subtract from dword, random endian
        index=random.randint(0,int(len(buff)/4)-1)*4+3
        buff[index]=add_byte(buff[index],-random.randint(1,ARITH_MAX))
    elif case==9:
        # add from dword, random endian
        index=random.randint(0,int(len(buff)/4)-1)*4+3
        buff[index]=add_byte(buff[index],random.randint(1,ARITH_MAX))
    elif case==10:
        # set random byte to random value
        if len(buff)==0:
            return bytes(b'')
        index=random.randint(0,len(buff)-1)
        buff[index:index+1]=rand_byte()
    elif case==11 or case==12:
        # delete bytes
        index=random.randint(0,len(buff)-1)
        buff=buff[:index]+buff[index+1:]
    elif case==13:
        # Clone bytes (75%) or insert a block of constant bytes (25%).
        clone=random.randint(0,3)!=0
        if len(buff)>1 and clone:
            clone_to=random.randint(0,len(buff)-1)
            length=choose_block_len(len(buff)-1,round)
            start=random.randint(0,len(buff)-length)
            buff=buff[:clone_to]+buff[start:start+length]+buff[clone_to:]
        else:

            length=choose_block_len(HAVOC_BLK_LARGE,round)
            start=0
            # insert random 0-256 
            to_insert=bytearray(b"")
            for i in range(length):
                to_insert+=rand_char()
            if len(buff)<=1:
                buff=buff+to_insert
            else: 
                clone_to=random.randint(0,len(buff)-1)
                buff=buff[:clone_to]+to_insert+buff[clone_to:]

    elif case==14:
        # Overwrite bytes with a randomly selected chunk (75%) or fixed bytes (25%).
        overwrite=random.randint(0,3)!=0
        length=choose_block_len(len(buff)-1,round)
        start=random.randint(0,len(buff)-length)
        clone_to=random.randint(0,len(buff)-length)
        if overwrite:
            buff=buff[:clone_to]+buff[start:start+length]+buff[clone_to+length:]
        else:
            to_insert=bytearray("")
            for i in range(length):
                to_insert+=rand_char()
            buff=buff[:clone_to]+to_insert+buff[clone_to+length:]
    return bytes(buff)

def mutate(buff:bytes,use_char:bool)->bytes:
    for i in range(random.randint(1,HAVOC_STACK_POW2)):
        buff=mutate_one(buff,use_char,i)
    return buff

if __name__ == '__main__':
    buff=b"initial input"
    buff=mutate_one(buff,True,0)
    print(buff)