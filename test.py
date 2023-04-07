import random
seed_list=[1,2,3,4,5]
weights=[0.1,0.2,0.3,0.2,1]
print(random.choices(seed_list,weights=weights))
print(seed_list)