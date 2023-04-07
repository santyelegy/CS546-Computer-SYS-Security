from seed import Seed
from typing import List
import random

EXPONENT=5

# The main challenge is How to calculate the number of times a path is executed. 
# We change the pair_set to a dictionary, with key as the pair and value as the number of times the pair is executed.
# We will not change the count in pair_set when trimming the seed_list for time complexity reason.
def seed_scheduler(seed_list:List[Seed],pair_set:dict)->Seed:
    for seed in seed_list:
        energy=0
        for pair in seed.coverage_set:
            energy+=pair_set[pair]
        seed.energy_score=1/(energy**5)
    # choose a seed from the seed_list based on the energy_score (possiblity)
    # need Python 3.6 or higher
    # random.choices(population, weights=None, *, cum_weights=None, k=1) Return a k sized list of elements chosen from the population with replacement
    return random.choices(seed_list,weights=[seed.energy_score for seed in seed_list])[0]