from typing import List
from seed import Seed

# calculate the score for each seed base on execution time and coverage size
# seeds with a lower execution time and a higher coverage size will have a higher score
def calculate_score(seeds:List[Seed])->List[Seed]:
    # calculate the total execution time for all seeds
    total_time=0
    for seed in seeds:
        total_time+=seed.time
    # calculate the total coverage size for all seeds
    total_coverage_size=0
    for seed in seeds:
        total_coverage_size+=len(seed.coverage_set)
    # calculate the score for each seed base on average execution time
    average_time=total_time/len(seeds)
    for seed in seeds:
        if seed.time*0.1>average_time:
            seed.performance_score=10
        elif seed.time*0.25>average_time:
            seed.performance_score=25
        elif seed.time*0.5>average_time:
            seed.performance_score=50
        elif seed.time*0.75>average_time:
            seed.performance_score=75
        elif seed.time*4<average_time:
            seed.performance_score=300
        elif seed.time*3<average_time:
            seed.performance_score=200
        elif seed.time*2<average_time:
            seed.performance_score=150
    # adjust the score for each seed base on coverage size
    average_coverage_size=total_coverage_size/len(seeds)
    for seed in seeds:
        if len(seed.coverage_set)*0.3>average_coverage_size:
            seed.performance_score*=3
        elif len(seed.coverage_set)*0.5>average_coverage_size:
            seed.performance_score*=2
        elif len(seed.coverage_set)*0.75>average_coverage_size:
            seed.performance_score*=1.5
        elif len(seed.coverage_set)*3<average_coverage_size:
            seed.performance_score*=0.25
        elif len(seed.coverage_set)*2<average_coverage_size:
            seed.performance_score*=0.5
        elif len(seed.coverage_set)*1.5<average_coverage_size:
            seed.performance_score*=0.75
    return seeds