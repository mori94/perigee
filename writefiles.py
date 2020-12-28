import networkx as nx

# Generate the shortest delay between all node pairs
def WriteDelay(OutputDelayFile, G, delay, num_node):
    fwl=open(OutputDelayFile,'w')
    for i in range(num_node):
        length, path=nx.single_source_dijkstra(G, i)
        for j in range(num_node):
            # TODO why start node delays minus destination delay
            # if len(length) < 1000:
                # print("len change", len(length))
            length[j]=round(
                    length[j]
                    + delay[int(i)]/2
                    - delay[int(j)]/2, 6)
            fwl.write(str(length[j])+'  ')
        fwl.write('\n')
    fwl.close()
    
def WriteConnection(OutputDelayFile, G, delay, neighbor):
    OutputDelayFile="Edge_"+OutputDelayFile
    fwl=open(OutputDelayFile,'a')
    for (u,v,d) in G.edges(data=True):
        fwl.write(str(round(d['weight'],0))+'  ')
    fwl.close()


def write(OutputDelayFile, G, NodeDelay, neighbor, num_node):
    WriteDelay(OutputDelayFile, G, NodeDelay, num_node)
    #WriteConnection(OutputDelayFile, G, NodeDelay, neighbor)
       
