import networkx as nx
import matplotlib.pyplot as plt 


def make_graph(filename):
    Graph = nx.Graph()
    graphfile = open(filename, "r")
    BlockedEdges = []
    for line in graphfile.readlines():
        if len(line) > 0 and line[0] == "#":
            newline = line.split()
            if line[1] == "V":
                newline[0] = newline[0].replace("#V", "")
                number_of_vertex = int(newline[0])
                for i in range(1, number_of_vertex + 1):
                    Graph.add_node(i)
            elif line[1] == "E":
                check = line.find("B")
                newline[0] = newline[0].replace("#E", "")
                newline[3] = newline[3].replace("W", "")
                if check > 0:
                    newline[4] = newline[4].replace("B", "")
                    BlockedEdges.append((int(newline[1]),int(newline[2])))
                    Graph.add_edge(int(newline[1]), int(newline[2]), weight=float(newline[3]), name=newline[0],
                                   PBlock=float(newline[4]))
                else:
                    Graph.add_edge(int(newline[1]), int(newline[2]), weight=float(newline[3]), name=newline[0],
                                   PBlock=0)
            elif newline[0] == "#Start":
                startnode = int(newline[1])
            elif newline[0] == "#Target":
                targetnode = int(newline[1])


    Graph.add_edge(startnode,targetnode ,weight=100)
    return Graph , BlockedEdges , startnode , targetnode



def Get_Vertex(index, graph):
    return graph.nodes[index]


def Find_Edegs(v,graph):
    Edges = []
    for edge in list(graph.edges):
        if int(edge[0]) ==v or int(edge[1])==v:
            Edges.append(edge)
    return Edges


def draw_g(G):
    plt.subplot(121)
    pos1 = nx.shell_layout(G)

    pos2 = pos1.copy()
    pos3 = pos1.copy()

    for i in pos2:
        pos2[i] = pos2[i] - [-0.1, 0.1]
        pos3[i] = pos3[i] - [0, 0.25]

    nodes_labels = nx.get_node_attributes(G, "P")
    nx.draw_networkx_labels(G, pos2, nodes_labels, font_size=8, font_color='green')

    edges_labels_w = nx.get_edge_attributes(G, "weight")
    edges_labels_b = nx.get_edge_attributes(G, "PBlock")
    nx.draw_networkx_edge_labels(G, pos1, edges_labels_w, font_color='blue', font_size=7)
    nx.draw_networkx_edge_labels(G, pos3, edges_labels_b, font_color='red', font_size=7)

    # when drawing to an interactive display.  Note that you may need to issue a
    # Matplotlib
    nx.draw(G, pos1, with_labels=True, font_weight='bold', font_size=13)
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()


def draw_g_dir(G):
    pos = nx.spring_layout(G)
    pos2 = pos.copy()

    for i in pos2:
        pos2[i] = pos2[i] - [-0.05, 0.08]

    nodes_P_labels = nx.get_node_attributes(G, "P")
    nodes_B_labels = nx.get_node_attributes(G, "Block")
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=7)
    nx.draw_networkx_labels(G, pos2, nodes_P_labels, font_size=7, font_color='green')
    nx.draw_networkx_labels(G, pos2, nodes_B_labels, font_size=7, font_color='red')
    nx.draw_networkx_edges(G, pos, edge_color='y', arrows=True)

    plt.show()