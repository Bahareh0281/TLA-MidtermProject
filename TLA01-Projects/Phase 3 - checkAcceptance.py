import sys
import json
from visualize import visualize
from FA.dfa import VisualDFA
from FA.nfa import VisualNFA
from utils import read_fa, create_standard_fa
from automata.fa.nfa import NFA

if __name__ == '__main__':
    """ the main function for visualize the FA"""
    args = sys.argv[1:]
    #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
    jsonpath = "samples/phase3-sample/in/input2.json"#args[0] 
    isDFA=True 

    try:
            read_fa(jsonpath)
            FA = create_standard_fa()
            dfa = VisualDFA(FA)
            dfa.show_diagram()
    except:
            try:
                isDFA=False
                read_fa(jsonpath)
                fa = create_standard_fa(1)
                nfa = VisualNFA(fa)
                nfa.show_diagram()
            except Exception as ex:
                raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                                "mentioned a correct file or its in the correct standard format")\
                    from ex


inputString="abaa"
index=0

if(isDFA):
    
    currentState=dfa.initial_state
    while(index<len(inputString)):
        if inputString[index] in dfa.transitions[currentState]:
            currentState=dfa.transitions[currentState][inputString[index]]
            index+=1
        else:
            print("Rejected")
            break
    if(currentState in dfa.final_states):
        print("Acepted")
    else:
        print("Rejected")
else:
    #we will convert nfa to dfa and then check the string
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

    #end of converting to dfa

    # nfa = VisualNFA(fa)
    # nfa.show_diagram()
    currentState={fa["initial_state"]}
    accept=True
    while(index<len(inputString)):
        cs=list(currentState)[0]
        if inputString[index] in fa["transitions"][cs]:
            currentState=fa["transitions"][cs][inputString[index]]
            index+=1
            if(currentState)=={'trap'}:
                print("Rejected")
                accept=False
                break
        else:
            print("Rejected")
            accept=False
            break
    if accept:
        if(list(currentState)[0] in fa["final_states"]):
            print("Accepted")
        else:
            print("Rejected")

    

