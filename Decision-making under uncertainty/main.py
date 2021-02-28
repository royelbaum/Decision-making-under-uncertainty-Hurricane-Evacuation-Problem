from Graph import *
from States import *
import random
GOAL_REWARD=0


def Get_Probability_Of_Action(fromstate,tostate):

    for i in range(1,len(fromstate)):
        if (tostate[i][1] != fromstate[i][1]):
            if tostate[i][1]==0:
                return 1.0-fromstate[i][1]
            else:
                return fromstate[i][1]
    return 1


def issublist(sl,l):
    for i in sl :
        if i not in l:
            return False
    return True

def utility_matrix(graph, targetnode,states):
    Utilities={}
    for s in states:
        Utilities[tuple(s)]=-10000
        if s[0] == targetnode:
            Utilities[tuple(s)]=GOAL_REWARD
    for i in range(len(graph.nodes)):
        for state in list(filter(lambda x:x[0]!=targetnode,states)):
            action_utility = -1000
            for n in graph.adj[state[0]]:
                if (((state[0],n),1) in state[1:]) or (((n,state[0]),1) in state[1:]):
                    continue
                tmp_U=0
                blocked_e_s=[]
                for b in state[1:]:
                    if b[0][0] == n or b[0][1] == n:
                        if b[1]==0 or b[1]==1:
                            blocked_e_s.append(b)

                    else:
                        blocked_e_s.append(b)
                Tstates=list(filter(lambda s:s[0]==n and issublist(blocked_e_s,s[1:]) ,states))
                if Tstates==[]:
                    print("state= ",state,"\tn=",n,"\n blocked_e_s=", blocked_e_s)
                for state_tag in Tstates:

                    pr=Get_Probability_Of_Action(state,state_tag)
                    tmp_U+=Utilities[tuple(state_tag)]*pr
                tmp_U+=reward(state,(state[0],n),targetnode,graph)
                if tmp_U>=action_utility:
                    # best_n=n
                    action_utility=tmp_U

            Utilities[tuple(state)]=action_utility
    print("for unreachable states the default utility is -1000")
    print("utilities= ",Utilities)
    return Utilities


def reward(state,step,target,graph):
    if step[1]==0:
        return float('-inf')
    if state[0]==target:
        return GOAL_REWARD
    return -1*graph.edges[step]["weight"]

##returns the best optimal way from the start node to the end
def bestpolicy(state,graph,states,target):
    u_matrix = utility_matrix(graph, target, states)
    state_action = best_action_matrix(graph, states, target, u_matrix)
    policy=[]
    while (state[0]!=target):
        blockages=[]
        for b in state[1:]:
            if b[1]>0 and b[1]<1:
                r=random.random()
                print("randomly ", r, "\t if " , b[0], "is blocked ")
                if r<b[1]:
                    blockages.append((b[0],1))
                else:
                    blockages.append((b[0],0))
            else:
                blockages.append(b)
        state=[state[0]]+blockages
        action=state_action[tuple(state)][0]
        if action==-1:
            print("dead end ",policy)
            return
        policy.append(action)
        state=[action]+state[1:]
    print("policy=" , policy)

##returns the matrix for all best action for each position
def best_action_matrix(graph,states,target,u_matrix):
    state_action={}
    for state in states:
        best_n = 0
        best_u = float('-inf')
        for n in graph.adj[state[0]]:
            if (((state[0], n), 1) in state[1:]) or (((n, state[0]), 1) in state[1:]):
                continue

            blocked_e_s = []
            for b in state[1:]:
                if b[0][0] == n or b[0][1] == n:
                    if b[1] == 0 or b[1] == 1:
                        blocked_e_s.append(b)
                else:
                    blocked_e_s.append(b)
            Tstates = list(filter(lambda s: s[0] == n and issublist(blocked_e_s, s[1:]), states))
            tmp_u=reward(state,(state[0],n),target,graph)
            for s in Tstates:
                tmp_u+=Get_Probability_Of_Action(state,s)*u_matrix[tuple(s)]


            if best_u <= tmp_u:
                best_n = n
                best_u = tmp_u
        if best_u <= -1000 or best_n == 0:
            state_action[tuple(state)]= [-1,-1000]
        else:
            state_action[tuple(state)]= [best_n,best_u]
    return state_action



##simulate a varsios of action and let the user choose if an edge is blocked or not
def simulator(graphname):
    graph, BlockedEdges, startnode, targetnode = make_graph(graphname)
    nodes = list(graph.nodes)

    States = Make_States(nodes, BlockedEdges, graph)
    curr_state=[startnode]+list(map(lambda e:(e,graph.edges[e]["PBlock"]),BlockedEdges))
    u_matrix = utility_matrix(graph, targetnode,States)
    state_action=best_action_matrix(graph,States,targetnode,u_matrix)

    while(True):
        if curr_state[0]==targetnode or curr_state[0]==-1:
            return
        for n in graph.adj[curr_state[0]]:
            if (curr_state[0],n) in BlockedEdges:
                blocked_e = (curr_state[0], n)
            else:
                blocked_e = (n,curr_state[0])
            if blocked_e in BlockedEdges and (blocked_e,1)not in curr_state[1:] and (blocked_e,0) not in curr_state[1:]  :
                print("is ", blocked_e, "blocked?(0/1)" )
                isb=int(input())
                newBlockeE=[]
                for i in range(len(curr_state[1:])):
                    if blocked_e == curr_state[1:][i][0]:
                        newBlockeE.append((blocked_e,isb))
                    else:
                        newBlockeE.append(curr_state[1:][i])
                curr_state=[curr_state[0]]+newBlockeE

        policy=state_action[tuple(curr_state)]
        print("the best action is: ",(curr_state[0],policy[0])," \n for state= ",curr_state,"\twith utility= ",policy[1])
        curr_state=[policy[0]]+curr_state[1:]

## return the best action to do with the current knowlage about the world
def get_best_action(graphname):
    graph, BlockedEdges, startnode, targetnode = make_graph(graphname)
    nodes = list(graph.nodes)

    States = Make_States(nodes, BlockedEdges, graph)
    u_matrix = utility_matrix(graph, targetnode, States)
    state_action = best_action_matrix(graph, States, targetnode, u_matrix)
    print(state_action)
    while (True):
        print("enter vertex:")
        state=[int(input())]
        for e in BlockedEdges:
            print ("enter pr for ",e)
            isb=float(input())
            state.append((e,isb))
        policy=state_action[tuple(state)]
        print("the best action for ",state," is = ",policy[0],"\twith utility= ",policy[1])
        print("exit?(y/n)")
        tocon=input()
        if(tocon=='y'):
            return
## simulator that choose ramdomly by the probebility if the edge is blocked or not
def randsimulator(graphname):
    graph, BlockedEdges, startnode, targetnode = make_graph(graphname)
    nodes = list(graph.nodes)

    States = Make_States(nodes, BlockedEdges, graph)
    state = [startnode] + list(map(lambda e: (e, graph.edges[e]["PBlock"]), BlockedEdges))
    bestpolicy(state, graph, States, targetnode)


simulator("input1.txt")
get_best_action("input1.txt")
randsimulator("input1.txt")
randsimulator("input2.txt")
randsimulator("input3.txt")
graph, BlockedEdges, startnode, targetnode = make_graph("graph.txt")
draw_g(graph)
