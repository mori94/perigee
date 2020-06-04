# perigee

How to run the simulator

- python3 main.py datafile #outbound #switchnodes #networktype (e.g. python3 main.py 1 8 2 hash)

#outbound:      the number of outbound neighbors, normally as 8
#switchnodes: the number of switched nodes each rounds
#networktype[hash, unhash, treehash]: whether to take the nodes' hashpower into simulation and a low-latency             
                        subgraph into consideration
