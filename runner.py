import sys
from mutator import mutate
import random
from coverage import Coverage
import io
from seed import Seed
import timeit

## parameter to set
program_dir="test/simple_test.py"
initial_input=b""
DEBUG=False
round=10000
TIMEOUT=15

## the input are passed to the python file by stdin
# seed_list is a list of Seed
seed_list=[]
pair_set=set()

# find the coverage of the input
def find_coverage(input:bytes,program_dir:str)->Seed:
    coverage=Coverage()
    sys.stdin = io.BytesIO(input)
    try:
        start = timeit.default_timer()
        sys.settrace(coverage.tracer)
        exec(open(program_dir).read())
        sys.settrace(None)
        stop = timeit.default_timer()
        outcome = 'PASS'
    except:
        sys.settrace(None)
        outcome = 'FAIL'
        start=0
        stop=TIMEOUT
    return Seed(input,coverage.pair_set,outcome,stop-start)

# may have some problem if there are nested import, only using lineno will not work
for i in range(round):
    set_len=len(pair_set)
    ##Mutate an input
    if len(seed_list)==0:
        input=initial_input
    else:
        buff=random.choice(seed_list).input
        input=mutate(buff,True)
    ##Run Program
    new_seed=find_coverage(input,program_dir)
    """
    proc = subprocess.Popen("python "+program_dir,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        print(input)
        outs, errs = proc.communicate(input=input,timeout=15)
    except TimeoutExpired:
        proc.kill()
    """
    #Add new seed
    pair_set=pair_set.union(new_seed.coverage_set)
    if set_len!=len(pair_set):
        seed_list.append(new_seed)

print(pair_set)
print(seed_list)