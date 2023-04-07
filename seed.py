
class Seed:
    def __init__(self, input:bytes, coverage_set:set(), outcome:str, time:float ):
        self.input = input
        self.coverage_set = coverage_set
        self.outcome = outcome
        self.time = time
        # give new seeds a high score to allow them run a bit longer
        self.performance_score = 10000
        self.energy_score = 1
    
    def __str__(self) -> str:
        return self.input.__repr__()
    
    def __repr__(self) -> str:
        return self.input.__repr__()