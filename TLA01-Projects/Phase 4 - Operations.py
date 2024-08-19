import sys
from visualize import visualize
from FA.dfa import VisualDFA
from FA.nfa import VisualNFA
from utils import read_fa, create_standard_fa
from frozendict import frozendict


# def ChangeTransition (OldTransition, GoalState, Symbol):
#     #print(OldTransition)
#     new_set = frozenset({GoalState})
#     new_dict = frozendict({Symbol: new_set})
#     #for key, value in OldTransition.items():
#         # print(f'value is: {value}')
#         # print(f'new_dict is: {new_dict}')
#         # OldTransition.remove(value)
#         # OldTransition.update(new_dict)
#     return new_dict


def AddLambda (Source, Dest, Dict):     # Does not have a lambda transition
    ConnectToSRC = frozendict({"":frozenset({Dest})})
    Dict[Source] = ConnectToSRC
    return Dict[Source]

def AppendLambda(Source, Dest, Dict):   # already has a lambda transition
    temp = set(Dict[Source][""])
    temp.add(Dest)
    temp = frozenset(temp)
    ConnectSRCToFinal = frozendict({"":temp})
    Dict[Source] = ConnectSRCToFinal
    return Dict[Source]


def StarMain (): #Star
    """ the main function for visualize the FA"""
    args = sys.argv[1:]
    #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
    json_path = "samples/phase4-sample/star/in/FA.json"
    try:
            read_fa(json_path)
            fa = create_standard_fa(1)
            nfa = VisualNFA(fa)
            final_nfa = fa
    except Exception as ex:
        raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                            "mentioned a correct file or its in the correct standard format")\
            from ex

    states=list(nfa.states)
    states.sort()
    #print(states)

    symbols=list(nfa.input_symbols)
    symbols.sort()
    #print(symbols)
    
    Trans = nfa.transitions
    #print(Trans)

    start_state = nfa.initial_state
    #print (f'starting state: {start_state}')
    final_states = nfa.final_states
    #print (final_states)
    Star(final_nfa, states, symbols, Trans, start_state, final_states)


def Star (final_nfa, states, symbols, Trans, start_state, final_states):
    new_dict = dict(Trans)

    New_Start_State = 'q' + str(len(states))
    states.append(New_Start_State)
    states.sort()

    New_Final_State = 'q' + str(len(states))
    states.append(New_Final_State)
    states.sort()
    #print (states)

    new_dict[New_Start_State] = AddLambda(New_Start_State, start_state, new_dict)
    new_dict[New_Start_State] = AppendLambda(New_Start_State, New_Final_State, new_dict)
    final_states_copy = set(final_states.copy())
    for FinalState in final_states:
        final_states_copy.remove(FinalState)
        try:                                        # already has a lambda transition
            new_dict[FinalState] = AppendLambda(FinalState, New_Final_State, new_dict)
        
        except:                                     # Does not have a lambda transition
            new_dict[FinalState] = AddLambda(FinalState, New_Final_State, new_dict)

    new_dict[New_Start_State] = AppendLambda(New_Start_State, New_Final_State, new_dict)

    new_dict[New_Final_State] = AddLambda(New_Final_State, New_Start_State, new_dict)

    new_frozendict = frozendict(new_dict)
    final_states_copy.add(New_Final_State)
    VisulalizeFA(final_nfa, symbols, new_dict, New_Start_State, states, final_states_copy)
    #print(new_frozendict)








def UnionMain ():
    #Union
    """ the main function for visualize the FA"""
    args = sys.argv[1:]
    #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
    json_path1 = "samples/phase4-sample/union/in/FA1.json"
    json_path2 = "samples/phase4-sample/union/in/FA2.json"
    try:
            read_fa(json_path1)
            fa = create_standard_fa(1)
            nfa1 = VisualNFA(fa)
            final_nfa = fa
            read_fa(json_path2)
            fa = create_standard_fa(1)
            nfa2 = VisualNFA(fa)
    except Exception as ex:
        raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                            "mentioned a correct file or its in the correct standard format")\
            from ex

    states1=list(nfa1.states)
    states1.sort()
    #print(states1)

    symbols1=list(nfa1.input_symbols)
    symbols1.sort()
    #print(symbols1)
    
    Trans1 = nfa1.transitions
    #print(Trans1)

    start_state1 = nfa1.initial_state
    #print (f'starting state1: {start_state1}')
    #print(type(start_state1))
    final_states1 = set(nfa1.final_states)
    #print (type(final_states1))


    states2=list(nfa2.states)
    states2.sort()
    #print(type(states2))

    symbols2=list(nfa2.input_symbols)
    symbols2.sort()
    #print(symbols2)
    
    Trans2 = nfa2.transitions
    #print(Trans2)

    start_state2 = nfa2.initial_state
    #print (f'starting state2: {start_state2}')
    final_states2 = set(nfa2.final_states)
    #print (final_states2)

    Union(final_nfa, states1, symbols1, Trans1, start_state1, final_states1, states2, symbols2, Trans2, start_state2, final_states2)


def Union (final_nfa, states1, symbols1, Trans1, start_state1, final_states1, states2, symbols2, Trans2, start_state2, final_states2):
    new_dict1 = dict(Trans1)            # Dictionary of first FA Transitions
    new_dict2 = dict(Trans2)            # Dictionary of second FA Transitions
    #print(new_dict2)
    Result_dict = new_dict1.copy()      # Final Result FA's Transitions
    Result_States = states1.copy()      # Final Result FA's States


    New_Start_State = 'q' + str(len(states1) + len(states2))                                    # New Start state
    Result_States.append(New_Start_State)                                                       # Adding new start state to the list of result states
    Result_States.sort()                                                                        # Sorting result states
    Result_dict[New_Start_State] = AddLambda(New_Start_State, start_state1, Result_dict)        # Connecting new start state to the first FA's start state with lambda
    

    New_Final_State = 'q' + str(len(states1) + len(states2) + 1)                                    # New final state
    Result_States.append(New_Final_State)                                                           # Adding new final state to the list of result states
    Result_States.sort()                                                                            # Sorting result states
    #print (Result_States)
    for FinalState in final_states1:                                                                # Connecting first FA's final state to the new final state with lambda
        try:                                        # already has a lambda transition
            Result_dict[FinalState] = AppendLambda(FinalState, New_Final_State, Result_dict)
        
        except:                                     # Does not have a lambda transition
            Result_dict[FinalState] = AddLambda(FinalState, New_Final_State, Result_dict)
    # Result_dict[New_Final_State] = frozendict({"":frozenset()})
    Result_dict[New_Final_State] = frozendict()


    new_dict2_copy = new_dict2.copy()       # Copy of dictionary of second FA Transitions
    changedStart2 = False                   # To track changes of second FA's start state
    StatesRelationDict = {}                 # Dictionary for saving what each of second FA's states' names will be 
    #print(StatesRelationDict)
    for state in states2:                                                                                               # Changing second FA's states' names
        New_state = 'q' + str(len(Result_States) - len(states2) + 1)                                                    # state's new name
        StatesRelationDict[state]= New_state                                                                            # Updating the dictionary of new names
        #print (StatesRelationDict)
        Result_States.append(New_state)                                                                                 # Adding the new state to the list of result states
        #new_dict2_copy[New_state] = ChangeTransition(new_dict2[state], New_state, 'b')
        #print(new_dict2_copy[New_state])
        if state == start_state2 and changedStart2 == False:                                                            # if the state is the second FA's start state, it should be changed once
            #print(f'state is: {state} and start state2 is:  {start_state2} and new state is: {New_state}')
            start_state2 = New_state                                                                                    # Changing the start state
            changedStart2 = True                                                                                        # The start state changed; it shouldn't change again
        if state in final_states2:                                                                                      # Changing the final state of the second FA
            final_states2.remove(state)                                                                                 # Removing the old final state from the list of second FA's final states 
            final_states2.add(New_state)                                                                                # Updating the list of second FA's final states (adding the new final state)

    #print (Result_dict)
    #print(new_dict2)
    for state in states2:                                                                                               # Updating transitions of the second FA with the new states names
        #print(set(new_dict2[state]['b']))
        # if ('q1' in set(new_dict2[state]['b'])):
        #     print ('state in set(new_dict2[state][''])')
        for sym in symbols2:                                                                                            # Checking if there is a transition for every symbol
            #print(f'current symbol is: {sym}')
            try:                                                                                                        # A state may not have a transition for a specific symbol
                tempset = set(new_dict2[state][sym])                                                                    # set of states that this state has a transition to
                tempset_copy = tempset.copy()                                                                           # copy of the temp set
                #print(f'1. temp set is: {tempset}')
                for st in tempset_copy:                                                                                 # for each state in the copy of the tempset
                    #print(f'state is {st}')
                    tempset.remove(st)                                                                                  # removing the state
                    newst = StatesRelationDict[st]
                    #print(f'type of newst is: {type(newst)}')
                    tempset.add(newst)                                                                                  # adding the new name from the dictionary
                    #print('tempst updated')
                #print(f'2. temp set is: {tempset}')
                #print (type(new_dict2[state][sym]))
                tempset = frozenset(tempset)
                connection = frozendict({sym:tempset})
                # print(connection)
                # print(f'Version 1 of new_dict2_copy[state] : {new_dict2_copy[state]}')
                #new_dict2_copy[state] = connection
                Result_dict[StatesRelationDict[state]] = connection                                                     # updating the result dict
                # print(f'Version 2 of new_dict2_copy[state] : {new_dict2_copy[state]}')
                # print(tempset)
            except Exception as e:
                #print(f'Error is: {e}')
                print()
            #print("*********************")

    # print(Result_dict)
    # print("*************")
    # print(new_dict2_copy)
    # for state in states1:
    #     del new_dict2_copy[state]

    
    #Result_dict.update(new_dict2_copy)
    #print(f'Start State2: {start_state2}   and final state2: {final_states2}')
    
    Result_dict[New_Start_State] = AppendLambda(New_Start_State, start_state2, Result_dict)         # connecting the new start state to the second FA's start state with lambda
    #print (Result_dict)
    for FinalState in final_states2:                                                                # connecting the final states of the second FA to the new final state with lambda
        try:                                        # already has a lambda transition
            Result_dict[FinalState] = AppendLambda(FinalState, New_Final_State, Result_dict)
        
        except:                                     # Does not have a lambda transition
            Result_dict[FinalState] = AddLambda(FinalState, New_Final_State, Result_dict)
    Result_symbs = set(symbols1 + symbols2)
    VisulalizeFA(final_nfa, Result_symbs, Result_dict, New_Start_State, Result_States, [New_Final_State])
    print(Result_dict)








def ConcatMain():
    #Union
    """ the main function for visualize the FA"""
    args = sys.argv[1:]
    #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
    json_path1 = "samples/phase4-sample/concat/in/FA1.json"
    json_path2 = "samples/phase4-sample/concat/in/FA2.json"
    try:
            read_fa(json_path1)
            fa = create_standard_fa(1)
            nfa1 = VisualNFA(fa)
            final_nfa = fa
            read_fa(json_path2)
            fa = create_standard_fa(1)
            nfa2 = VisualNFA(fa)
    except Exception as ex:
        raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                            "mentioned a correct file or its in the correct standard format")\
            from ex

    states1=list(nfa1.states)
    states1.sort()
    #print(states1)

    symbols1=list(nfa1.input_symbols)
    symbols1.sort()
    #print(symbols1)
    
    Trans1 = nfa1.transitions
    #print(Trans1)

    start_state1 = nfa1.initial_state
    #print (f'starting state1: {start_state1}')
    #print(type(start_state1))
    final_states1 = set(nfa1.final_states)
    #print (type(final_states1))


    states2=list(nfa2.states)
    states2.sort()
    #print(type(states2))

    symbols2=list(nfa2.input_symbols)
    symbols2.sort()
    #print(symbols2)
    
    Trans2 = nfa2.transitions
    #print(Trans2)

    start_state2 = nfa2.initial_state
    #print (f'starting state2: {start_state2}')
    final_states2 = set(nfa2.final_states)
    #print (final_states2)
    # nfa1 = VisualNFA(fa)
    # nfa1.show_diagram()
    Concat(final_nfa, states1, symbols1, Trans1, start_state1, final_states1, states2, symbols2, Trans2, start_state2, final_states2)

def Concat(final_nfa, states1, symbols1, Trans1, start_state1, final_states1, states2, symbols2, Trans2, start_state2, final_states2):
    new_dict1 = dict(Trans1)            # Dictionary of first FA Transitions
    # print (new_dict1)
    new_dict2 = dict(Trans2)            # Dictionary of second FA Transitions
    # print(new_dict2)
    Result_dict = new_dict1.copy()      # Final Result FA's Transitions
    Result_States = states1.copy()      # Final Result FA's States


    # New_Start_State = 'q' + str(len(states1) + len(states2))                                    # New Start state
    # Result_States.append(New_Start_State)                                                       # Adding new start state to the list of result states
    # Result_States.sort()                                                                        # Sorting result states
    # Result_dict[New_Start_State] = AddLambda(New_Start_State, start_state1, Result_dict)        # Connecting new start state to the first FA's start state with lambda
    # print(Result_dict)
    s1 = 'q'
    s2 = str(len(states1) + len(states2))
    #New_Final_State = 'q' + str(len(states1) + len(states2))
    New_Final_State = "".join([s1, s2])
    Result_States.append(New_Final_State)                                                           # Adding new final state to the list of result states
    Result_States.sort() 
    New_Final_State2 = 'q' + str(len(states1) + len(states2) + 2) 
    if len(final_states1) > 1:
                                    # New final state
        Result_States.append(New_Final_State2)                                                           # Adding new final state to the list of result states
        Result_States.sort()                                                                            # Sorting result states
        #print (Result_States)
        for FinalState in final_states1:                                                                # Connecting first FA's final state to the new final state with lambda
            try:                                        # already has a lambda transition
                Result_dict[FinalState] = AppendLambda(FinalState, New_Final_State2, Result_dict)
            
            except:                                     # Does not have a lambda transition
                Result_dict[FinalState] = AddLambda(FinalState, New_Final_State2, Result_dict)
    Result_dict[New_Final_State] = frozendict({})  ######################
    
    #print(Result_dict)

    new_dict2_copy = new_dict2.copy()       # Copy of dictionary of second FA Transitions
    changedStart2 = False                   # To track changes of second FA's start state
    StatesRelationDict = {}                 # Dictionary for saving what each of second FA's states' names will be 
    #print(StatesRelationDict)
    for state in states2:                                                                                               # Changing second FA's states' names
        New_state = 'q' + str(len(Result_States) - len(states2) + 2)                                                    # state's new name
        StatesRelationDict[state]= New_state                                                                            # Updating the dictionary of new names
        #print (StatesRelationDict)
        Result_States.append(New_state)                                                                                 # Adding the new state to the list of result states
        #new_dict2_copy[New_state] = ChangeTransition(new_dict2[state], New_state, 'b')
        #print(new_dict2_copy[New_state])
        if state == start_state2 and changedStart2 == False:                                                            # if the state is the second FA's start state, it should be changed once
            #print(f'state is: {state} and start state2 is:  {start_state2} and new state is: {New_state}')
            start_state2 = New_state                                                                                    # Changing the start state
            changedStart2 = True                                                                                        # The start state changed; it shouldn't change again
        if state in final_states2:                                                                                      # Changing the final state of the second FA
            final_states2.remove(state)                                                                                 # Removing the old final state from the list of second FA's final states 
            final_states2.add(New_state)                                                                                # Updating the list of second FA's final states (adding the new final state)
    for state in states2:                                                                                               # Updating transitions of the second FA with the new states names
        #print(set(new_dict2[state]['b']))
        for sym in symbols2:                                                                                            # Checking if there is a transition for every symbol
            try:                                                                                                        # A state may not have a transition for a specific symbol
                tempset = set(new_dict2[state][sym])                                                                    # set of states that this state has a transition to
                tempset_copy = tempset.copy()                                                                           # copy of the temp set
                for st in tempset_copy:                                                                                 # for each state in the copy of the tempset
                    tempset.remove(st)                                                                                  # removing the state
                    newst = StatesRelationDict[st]
                    tempset.add(newst)
                tempset = frozenset(tempset)
                connection = frozendict({sym:tempset})
                Result_dict[StatesRelationDict[state]] = connection
            except Exception as e:
                print()

    
    if len(final_states1) > 1:
        Result_dict[New_Final_State2] = AddLambda(New_Final_State2, start_state2, Result_dict)
    else:
        for FS in final_states1:
            print(f'FS is {FS}')
            Result_dict[FS] = AddLambda(FS, start_state2, Result_dict)


    for FinalState in final_states2:                                                                # connecting the final states of the second FA to the new final state with lambda
        print(f'Final state is: {FinalState}')
        try:                                        # already has a lambda transition
            Result_dict[FinalState] = AppendLambda(FinalState, New_Final_State, Result_dict)
        
        except:                                     # Does not have a lambda transition
            Result_dict[FinalState] = AddLambda(FinalState, New_Final_State, Result_dict)
    Result_symbs = set(symbols1 + symbols2)
    print(Result_dict)
    VisulalizeFA(final_nfa, Result_symbs, Result_dict, start_state1, Result_States, {New_Final_State})


def VisulalizeFA (final_nfa, Symbols, Result_dict, start_state, Result_States, final_states):
    Result_symbs = set(Symbols)
    final_nfa["initial_state"] = start_state
    final_nfa["states"] = set(Result_States)
    final_nfa["transitions"] = Result_dict
    final_nfa["input_symbols"] = set(Result_symbs)
    final_nfa["final_states"] =  set(final_states)
    vis = VisualNFA(final_nfa)
    vis.show_diagram()


if __name__ == '__main__':
    
    # StarMain()
    # UnionMain()
    ConcatMain()
    print("hello")

    
