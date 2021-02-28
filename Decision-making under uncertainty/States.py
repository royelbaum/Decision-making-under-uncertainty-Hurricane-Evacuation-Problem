def Filter_By_Blocked_Way(state, vertex, transactionstates):
    filtered = []
    for i in transactionstates:
            if(((state[0],vertex),1) not in i[1:]):
                filtered.append(i)
    return filtered

def Find_States(v,states):
    TStates = []
    for state in states:
       if state[0] == v:
            TStates.append(state)
    return TStates

def Make_State(state,blockededges,States,graph):
        if len(blockededges)==1:
            if state[0] != blockededges[0][0] and state[0] != blockededges[0][1]:
                newstate1 = state.copy()
                newstate2 = state.copy()
                newstate3 =state.copy()
                newstate1.append((blockededges[0], graph.edges[blockededges[0]]["PBlock"]))
                newstate2.append((blockededges[0] , 1))
                newstate3.append((blockededges[0], 0))
                States.append(newstate1)
                States.append(newstate2)
                States.append(newstate3)
                return States
            else:
                newstate1 = state.copy()
                newstate2 = state.copy()
                newstate1.append((blockededges[0], 1))
                newstate2.append((blockededges[0], 0))
                States.append(newstate1)
                States.append(newstate2)
                return States
        else:
            edge = blockededges.pop(0)
            if state[0] != edge[0] and state[0] != edge[1]:
                newstate1 = state.copy()
                newstate2 = state.copy()
                newstate3 = state.copy()
                newstate1.append((edge,graph.edges[edge]["PBlock"]))
                newstate2.append((edge,0))
                newstate3.append((edge,1))
                States = Make_State(newstate1,blockededges.copy(),States,graph)
                States = Make_State(newstate2, blockededges.copy(), States, graph)
                States = Make_State(newstate3, blockededges.copy(), States, graph)
            else:
                newstate1 = state.copy()
                newstate2 = state.copy()
                newstate1.append((edge, 1))
                newstate2.append((edge, 0))
                States = Make_State(newstate1, blockededges.copy(), States, graph)
                States = Make_State(newstate2, blockededges.copy(), States, graph)
            return States

def Make_States(nodes,blockededges,graph):
    States = []
    for node in nodes:
        States = Make_State([node],blockededges.copy(),States,graph)
    return States

