from mutator import mutate
from coverage import find_coverage
from trim_seeds import trim_seeds
from performance_score import calculate_score,trim_with_performance_score
from config import *
from seed_scheduler import seed_scheduler

## the input are passed to the python file by stdin
# seed_list is a list of Seed
seed_list=[]
# key is the pair, value is the number of times the pair is executed
pair_set={}

# may have some problem if there are nested import, only using lineno will not work
for i in range(round):
    set_len=len(pair_set)
    ##Mutate an input
    if len(seed_list)==0:
        input=initial_input
    else:
        buff=seed_scheduler(seed_list,pair_set).input
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
    for pair in new_seed.coverage_set:
        if pair not in pair_set:
            pair_set[pair]=0
    # only count when the pair is added to the pair_set
    if set_len!=len(pair_set):
        seed_list.append(new_seed)
        for pair in new_seed.coverage_set:
            pair_set[pair]+=1
    if i%PERFORMANCE_CYCLE==0:
        calculate_score(seed_list)
        seed_list=trim_with_performance_score(seed_list)
    if i%TRIM_CYCLE==0:
        seed_list=trim_seeds(seed_list,program_dir)

print(pair_set)
print(seed_list)