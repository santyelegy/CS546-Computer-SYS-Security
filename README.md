# CS546-Computer-SYS-Security

Rutgers Spring 2023 COMP SYS SECURITY 16:198:546:01

Professor: Shiqing Ma

## Goals
- [x] code coverage
- [x] Implement a basic fuzzer with random generation and UNIX signal Oracle 
- [x] Implement corpus for coverage test
- [ ] Implement the heuristics generation with the corpus
- [ ] Implement more robust mutator
- [ ] Compare the performance of this implementation with the official AFL
- [x] Try to modify it to an in-memory fuzzer to break the UNIX fork bottleneck
- [ ] ~~Replace the heuristic generation with deep learning methods or something equivalent, compare the performance (number of bugs, times)~~ (Not quite possible, discrete problem)

## Tips

Using subprocess is significantly slower than directly calling exec

Redirect the stdin to make the file input