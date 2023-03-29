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

former_line=-1
pair_set=set()

# may have some problem if there are nested import, only using lineno will not work
def tracer(frame, event, arg):
    if event == 'line':
        global former_line
        global pair_set
        lineno = frame.f_lineno
        pair_set.add((former_line,lineno))
        former_line=lineno
    return tracer

sys.settrace(tracer)
exec(open("test.py").read())
print(pair_set)