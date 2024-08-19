import sys
from visualize import visualize
from FA.dfa import VisualDFA
from FA.nfa import VisualNFA
from utils import read_fa, create_standard_fa

from automata.fa.nfa import NFA

if __name__ == '__main__':
    """ the main function for visualize the FA"""
    args = sys.argv[1:]
    #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
    json_path = "samples/phase1-sample/in/input1.json"
    try:
            read_fa(json_path)
            fa = create_standard_fa(1)
            nfa = VisualNFA(fa)
    except Exception as ex:
        raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                            "mentioned a correct file or its in the correct standard format")\
            from ex

    # visualize(json_path)  # visualize the FA

    states=list(nfa.states)
    symbols=list(nfa.input_symbols)
    symbols.sort()
    states.sort()
newStart={nfa.initial_state}
newFinal={"0"}
newFinal.remove("0")

newTr={}

print(type(newTr))
print(type(nfa.transitions['q0']))

if("" in nfa.transitions[nfa.initial_state]):
    for ns in list(nfa.transitions[nfa.initial_state][""]):
        newStart.add(ns)


queue = [newStart]
dfa_states=[newStart]
for x in nfa.final_states:
    if(x in newStart):
        newFinal.add(frozenset(newStart))
        break

while queue:
        currentSet = queue.pop(0)
        for symbol in symbols:
            next_states = {"a"}
            next_states.remove("a")
            for currentState in currentSet:
                if(symbol in nfa.transitions[currentState]):
                    for temp in list(nfa.transitions[currentState][symbol]):
                        
                        next_states.add(temp)
                        Lstack=[]
                        if "" in nfa.transitions[temp]:
                            for lambdaT in list (nfa.transitions[temp][""] ):
                                Lstack.append(lambdaT)
                                next_states.add(lambdaT)
                            while( Lstack):
                                Ltemp=Lstack[0]
                                Lstack.remove(Ltemp)
                                if "" in nfa.transitions[Ltemp]:
                                    for t in list (nfa.transitions[Ltemp][""] ):
                                        next_states.add(t)
                                        Lstack.append(t)
                        

            if next_states and next_states not in dfa_states:
                dfa_states.append(next_states)
                queue.append(next_states)
                for x in nfa.final_states:
                    if(x in next_states):
                        newFinal.add(frozenset(next_states))
                        break
            
            if next_states:

                if '-'.join(currentSet) in newTr:
                    newTr['-'.join(currentSet)].update({symbol:{'-'.join(next_states)}})
                else:
                     newTr.update({'-'.join(currentSet):{symbol:{'-'.join(next_states)}}}) 

            else:
                if {"trap"} in dfa_states:
                    if '-'.join(currentSet) in newTr:
                        newTr['-'.join(currentSet)].update({symbol:{"trap"}})
                    else:
                        newTr.update({'-'.join(currentSet):{symbol:{"trap"}}}) 
                else:
                    dfa_states.append({"trap"})
                    newTr.update({"trap":{symbols[0]:{"trap"}}})
                    for trapS in symbols:
                        newTr["trap"].update({trapS:{"trap"}})

                    if '-'.join(currentSet) in newTr:
                        newTr['-'.join(currentSet)].update({symbol:{"trap"}})
                    else:
                        newTr.update({'-'.join(currentSet):{symbol:{"trap"}}}) 

print("this is the end of DFA")

stringStates=set()
for s in dfa_states:
    stringStates.add('-'.join(s))
fa["initial_state"]='-'.join(newStart)
fa["states"]=stringStates
StringFinalStates=set()
for s in newFinal:
    StringFinalStates.add('-'.join(s))
fa["final_states"]=StringFinalStates
fa["transitions"]=newTr

nfa = VisualNFA(fa)
nfa.show_diagram()
print("done")

