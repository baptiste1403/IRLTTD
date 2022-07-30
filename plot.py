from matplotlib import pyplot as plt
import networkx as nx

def createImageFromGraph(G: nx.Graph):
    labels_nodes={node:f'{city}' for node,city in G.nodes(data='city')}
    labels_edges ={edge:f"{G.edges[edge]['path']}" for edge in G.edges}

    # positions for all nodes
    pos = nx.spring_layout(G, scale=5)

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=1000,node_color="lightblue",alpha=0.7)
                
    # labels
    nx.draw_networkx_labels(G, pos, labels=labels_nodes, \
                        font_size=10, \
                        font_color='black', \
                        font_family='sans-serif')

    # edges
    nx.draw_networkx_edges(G, pos,width=1, edge_color="lightblue", style="dashed")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_edges, font_color='black')

    plt.axis('off')
    plt.savefig('fig.png')
    plt.clf()
    return 'fig.png'