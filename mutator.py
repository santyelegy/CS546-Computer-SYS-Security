# requires python version>3.9
import random
import string
#out_buf
#in_buf

def rand_char()->bytes:
    #return random.choice(string.ascii_letters + string.digits + string.punctuation).encode()
    return random.choice(string.ascii_letters).encode()

def rand_byte()->bytes:
    return random.randbytes(1)
### still need to implement, AFL use very complex mutation
# byte flips, arithmetics, known ints, havoc, trim
def mutate_one(buff:bytes,use_char:bool)->bytes:
    buff=bytearray(buff)
    if use_char:
        mutator=rand_char
    else:
        mutator=rand_byte
    case=random.randint(0,2)
    if case==0:
        # byte filp
        if len(buff)==0:
            return bytes(b'')
        index=random.randint(0,len(buff)-1)
        buff[index:index+1]=mutator()
    elif case==1:
        # add byte
        if len(buff)==0:
            return bytes(mutator())
        index=random.randint(0,len(buff)-1)
        buff=buff[:index]+mutator()+buff[index:]
    elif case==2:
        # trim byte
        if len(buff)<=1:
            return bytes(b'')
        index=random.randint(0,len(buff)-1)
        buff=buff[:index]+buff[index+1:]
    return bytes(buff)

def mutate(buff:bytes,use_char:bool,round:int=5)->bytes:
    for i in range(round):
        buff=mutate_one(buff,use_char)
    return buff

if __name__ == '__main__':
    buff=b"initial input"
    for i in range(100):
        buff=mutate(buff,True)
        print(buff)