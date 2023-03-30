### Reference from AFL white paper
#The instrumentation injected into compiled programs captures branch (edge)
#coverage, along with coarse branch-taken hit counts. The code injected at
#branch points is essentially equivalent to:
#  cur_location = <COMPILE_TIME_RANDOM>;
#  shared_mem[cur_location ^ prev_location]++; 
#  prev_location = cur_location >> 1;
###

import sys

test_file="test.py"


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