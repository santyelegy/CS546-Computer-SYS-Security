# CS546-Computer-SYS-Security

Rutgers Spring 2023 COMP SYS SECURITY 16:198:546:01

Professor: Shiqing Ma
## Dependency
```
prettytable
Python>=3.9
```
## Usage
All of the arguments have default values, can directly run by `python runner.py`.

The program to fuzz must take inputs from stdin, the fuzzer will generate bytes and feed them to the target program throug stdin.

All arguments
```
usage: runner.py [-h] [-dir PROGRAM_DIR] [-i INITIAL_INPUT] [-r ROUND] [-t TIMEOUT] [-pc PERFORMANCE_CYCLE] [-tc TRIM_CYCLE]

options:
  -h, --help            show this help message and exit
  -dir PROGRAM_DIR, --program_dir PROGRAM_DIR
                        Program directory
  -i INITIAL_INPUT, --initial_input INITIAL_INPUT
                        Initial input
  -r ROUND, --round ROUND
                        Number of rounds
  -t TIMEOUT, --TIMEOUT TIMEOUT
                        Timeout for each run
  -pc PERFORMANCE_CYCLE, --PERFORMANCE_CYCLE PERFORMANCE_CYCLE
                        cycles to trim seeds base on performance score
  -tc TRIM_CYCLE, --TRIM_CYCLE TRIM_CYCLE
                        cycles to trim seeds by removing bytes
```
## Goals
- [x] code coverage
- [x] Implement a basic fuzzer with random generation and UNIX signal Oracle 
- [x] Implement corpus for coverage test
- [x] Implement the heuristics generation with the corpus
- [x] Implement more robust mutator
- [ ] Compare the performance of this implementation with the official AFL
- [x] Try to modify it to an in-memory fuzzer to break the UNIX fork bottleneck
- [ ] ~~Replace the heuristic generation with deep learning methods or something equivalent, compare the performance (number of bugs, times)~~ (Not quite possible, need neural program smoothing)
- [x] Provide API for power scheduler of the seeds
- [x] Bug/ Coverage report generator

## AFL Fuzzer
- [x] trim L/S (important)
- [x] * performance score
- [x] extras (interesting value)
- [x] havoc 

arith L/8 - deterministic arithmetics. The fuzzer tries to subtract or add small integers to 8-, 16-, and 32-bit values. The stepover is always 8 bits.
interest L/8 - deterministic value overwrite. The fuzzer has a list of known "interesting" 8-, 16-, and 32-bit values to try. The stepover is 8 bits.

extras - deterministic injection of dictionary terms. This can be shown as "user" or "auto", depending on whether the fuzzer is using a user-supplied dictionary (-x) or an auto-created one. You will also see "over" or "insert", depending on whether the dictionary words overwrite existing data or are inserted by offsetting the remaining data to accommodate their length.

havoc - a sort-of-fixed-length cycle with stacked random tweaks. The operations attempted during this stage include bit flips, overwrites with random and "interesting" integers, block deletion, block duplication, plus assorted dictionary-related operations (if a dictionary is supplied in the first place).