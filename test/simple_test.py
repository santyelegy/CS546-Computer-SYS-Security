import sys

def test_program(str) -> bool:
    if str[0]=="a":
        if str[1]=="b":
            if str[2]=="c":
                if str[3]=="d":
                    raise ValueError("error here")
    return True

for line in sys.stdin:
    test_program(line.decode())
