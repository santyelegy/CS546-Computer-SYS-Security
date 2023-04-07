from typing import List
from coverage import find_coverage
from seed import Seed

TRIM_START_STEPS=4
TRIM_MIN_BYTES=16
TRIM_END_STEPS=1024

#Trim all new test cases to save cycles when doing deterministic checks. 
# The trimmer uses power-of-two increments somewhere between 1/16 and 1/1024 of file size, to keep the stage short and sweet.
def trim_seeds(seeds:List[Seed],program_dir:str)->List[Seed]:
    # trim seeds while keeping code coverage
    if len(seeds)<5:
        return seeds
    # start from high to low, trim the input to the minimum
    remove_len=max(len(seeds)/TRIM_START_STEPS,TRIM_MIN_BYTES)
    # Continue until the number of steps gets too high or the stepover gets too small.
    while remove_len>max(len(seeds)/TRIM_END_STEPS,TRIM_MIN_BYTES):
        remove_pos=remove_len
        while remove_pos<len(seeds):
            #trim the input
            trim_avail=min(remove_len,len(seeds)-remove_pos)
            if trim_avail<=0:
                break
            buff=seeds[remove_pos].input
            coverage=seeds[remove_pos].coverage_set
            new_buff=buff[:remove_pos]+buff[remove_pos+trim_avail:]
            #find the coverage of the new input
            new_seed=find_coverage(new_buff,program_dir)
            # if the deletion keeps the coverage, we make the deletion permanent
            if len(new_seed.coverage_set)==len(coverage):
                seeds[remove_pos]=new_seed
            else:
                remove_pos+=trim_avail
        remove_len/=2
    return seeds
