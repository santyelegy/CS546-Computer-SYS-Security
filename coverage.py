### Reference from AFL white paper
#The instrumentation injected into compiled programs captures branch (edge)
#coverage, along with coarse branch-taken hit counts. The code injected at
#branch points is essentially equivalent to:
#  cur_location = <COMPILE_TIME_RANDOM>;
#  shared_mem[cur_location ^ prev_location]++; 
#  prev_location = cur_location >> 1;
###

import sys
from seed import Seed
import timeit
import io



# may have some problem if there are nested import, only using lineno will not work
class Coverage:
    def __init__(self) -> None:
        self.former_line=-1
        self.pair_set=set()

    def tracer(self,frame, event, arg):
        if event == 'line':
            lineno = frame.f_lineno
            self.pair_set.add((self.former_line,lineno,))
            #self.pair_set.add(frame.f_code.co_name)
            self.former_line=lineno
        return self.tracer
    
# find the coverage of the input and run the code
# TODO: add timeout
def find_coverage(input:bytes,program_dir:str,time_out:float)->Seed:
    coverage=Coverage()
    sys.stdin = io.BytesIO(input)
    try:
        start = timeit.default_timer()
        sys.settrace(coverage.tracer)
        exec(open(program_dir).read())
        sys.settrace(None)
        stop = timeit.default_timer()
        outcome = 'PASS'
        exception=None
    except Exception as e:
        sys.settrace(None)
        outcome = 'FAIL'
        exception=e
        start=0
        stop=time_out
    return Seed(input,coverage.pair_set,outcome,stop-start,exception)