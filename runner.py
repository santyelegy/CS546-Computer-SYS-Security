from mutator import mutate
from coverage import find_coverage
from trim_seeds import trim_seeds
from performance_score import calculate_score,trim_with_performance_score
from config import *
from seed_scheduler import seed_scheduler
import prettytable
import timeit
import argparse


def run(args):
    ## the input are passed to the python file by stdin
    # seed_list is a list of Seed
    seed_list=[]
    # key is the pair, value is the number of times the pair is executed
    pair_set={}
    bug_seeds=[]
    # may have some problem if there are nested import, only using lineno will not work
    for i in range(args.round):
        set_len=len(pair_set)
        ##Mutate an input
        if len(seed_list)==0:
            input=args.initial_input.encode()
        else:
            buff=seed_scheduler(seed_list,pair_set).input
            input=mutate(buff,True)
        ##Run Program
        new_seed=find_coverage(input,args.program_dir,args.TIMEOUT)
        
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
            if new_seed.outcome=='FAIL':
                bug_seeds.append(new_seed)
            for pair in new_seed.coverage_set:
                pair_set[pair]+=1
        if i%args.PERFORMANCE_CYCLE==0:
            calculate_score(seed_list)
            seed_list=trim_with_performance_score(seed_list)
        if i%args.TRIM_CYCLE==0:
            seed_list=trim_seeds(seed_list,args.program_dir,args.TIMEOUT)
    return bug_seeds,pair_set,len(seed_list)

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir","--program_dir", type=str,
                    help="Program directory",default=program_dir)
    parser.add_argument("-i","--initial_input", type=str,help="Initial input",default=initial_input)
    parser.add_argument("-r","--round", type=int,help="Number of rounds",default=round)
    parser.add_argument("-t","--TIMEOUT", type=float,help="Timeout for each run",default=TIMEOUT)
    parser.add_argument("-pc","--PERFORMANCE_CYCLE", type=int,help="cycles to trim seeds base on performance score",default=PERFORMANCE_CYCLE)
    parser.add_argument("-tc","--TRIM_CYCLE", type=int,help="cycles to trim seeds by removing bytes",default=TRIM_CYCLE)
    args=parser.parse_args()
    # Start fuzzing
    print("Start fuzzing on "+program_dir)
    start_time = timeit.default_timer()
    bug_seeds,pair_set,seed_num=run(args)
    end_time=timeit.default_timer()
    line_set=set()
    for pair in pair_set:
        line_set.add(pair[0])
        line_set.add(pair[1])
    table=prettytable.PrettyTable()
    table.field_names=['Total Run time','Rounds','Avg Run time','Bug Find','Coverage pairs','Covered Lines','Seed number']
    # remove -1 line in line_set
    table.add_row([end_time-start_time,args.round,(end_time-start_time)/round,len(bug_seeds),len(pair_set),len(line_set)-1,seed_num])
    print(table)
    if len(bug_seeds)!=0:
        print("Test cases that trigger bugs:")    
        for i in range(len(bug_seeds)):
            print("Test case "+str(i+1))
            seed=bug_seeds[i]
            print(seed.input)
            print("Exception:")
            print(seed.exception)
            print()