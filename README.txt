================================================
Overview
================================================
The following contains two algorithms designed to solve the Travelling Salesmen Problem:

- Genetic Search Algorithm
- Simulated Annealing Algorithm


================================================
Example input file
================================================
NAME = <string =name-of-the-data-file>,
SIZE = <integer n = the number of cities in the instance>,
<list-of-integers d1, d2, d3, . . . , dm> where the list consists of 
the distances between cities (1,2),(1,3), . . . ,(1, n),
then the distances between cities (2,3),(2,4), . . . ,(2, n),...
and finally the distance between the cities (n-1, n).

E.g.
NAME = SampleCities,
SIZE = 5,
3, 4, 3, 4,
5, 6, 5,
5, 8,
5