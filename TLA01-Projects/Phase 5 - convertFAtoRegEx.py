import sys
import re
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
    jsonpath = "samples/phase5-sample/in/FA.json"#args[0] 
    isDFA=True 

    try:
            read_fa(jsonpath)
            fa = create_standard_fa()
            dfa = VisualDFA(fa)
            # dfa.show_diagram()
    except:
            try:
                isDFA=False
                read_fa(jsonpath)
                fa = create_standard_fa(1)
                dfa = VisualNFA(fa)
                # dfa.show_diagram()
            except Exception as ex:
                raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                                "mentioned a correct file or its in the correct standard format")\
                    from ex






if(isDFA):
    print("isDFA")

#    write the equation here1111111111
    # Step 1: Assign variables to each state
    variables = {s: f'x_{i}' for i, s in enumerate(dfa.states)}
    X = variables[dfa.initial_state]

    # Step 2: Write equations for each state
    equations = []
    for state in dfa.states:
        R = ''.join(f'{variables[next_state]}|' for symbol, next_state in dfa.transitions[state].items())
        R = f'({R[:-1]})'  # Remove the last | symbol
        L = '1' if state in dfa.final_states else '0'
        equations.append(f'{variables[state]}={R}{variables[state]}+{L}')

    # Step 3: Solve the set of equations
    regex = ''
    while len(equations) > 0:
        # Find an equation with only one variable
        # for i, eqn in enumerate(equations):
        #     if len(re.findall(f'\\b{variables[dfa.initial_state]}\\b', eqn)) == 0 and len(re.findall(f'\\b{variables[list(dfa.final_states)[0]]}\\b', eqn)) == 0 and len(re.findall('[a-z0-9()]+', eqn)) == 1:
        #         regex += eqn.split('=')[1]
        #         var_to_remove = variables[dfa.states[i]]
        #         break
        # else:
        #     raise ValueError("Can't solve equations")

        # Substitute variable in other equations
        equations = [re.sub(f'\\b{var_to_remove}\\b', f'({regex})', eqn) for eqn in equations]
        equations.pop(i)


else:
        # Step 1: Assign variables to each state

    variables = {s: f'x_{i}' for i, s in enumerate(dfa.states)}
    X = variables[dfa.initial_state]

    # Step 2: Write equations for each state
    equations = []
    for state in dfa.states:
        R=''
        for symbol in list(dfa.input_symbols):
            if(symbol in dfa.transitions[state]):
                for item in dfa.transitions[state][symbol]:
                    R = R+(f'{symbol}.{variables[item]}+' )
        
        # for symbol, next_state in dfa.transitions[state].items():
        #     for i in list(next_state):
        #         R = ''.join(f'{symbol}.{variables[i]}' )
        # R = f'({R[:-1]})'  # Remove the last | symbol
        L = '1' if state in dfa.final_states else '0'
        equations.append(f'{variables[state]}={R}{L}')

    # Step 3: Solve the set of equations
    ####################it has problem
    # regex = ''
    # while len(equations) > 0:
    #     # Find an equation with only one variable
    #     for i, eqn in enumerate(equations):
    #         if len(re.findall(f'\\b{variables[dfa.initial_state]}\\b', eqn)) == 0 and len(re.findall(f'\\b{variables[list(dfa.final_states)[0]]}\\b', eqn)) == 0 and len(re.findall('[a-z0-9()]+', eqn)) == 1:
    #             regex += eqn.split('=')[1]
    #             var_to_remove = variables[dfa.states[i]]
    #             break
    #     else:
    #         raise ValueError("Can't solve equations")

    #     # Substitute variable in other equations
    #     equations = [re.sub(f'\\b{var_to_remove}\\b', f'({regex})', eqn) for eqn in equations]
    #     equations.pop(i)

    #another code:
    # Step 3: Solve the set of equations
regex = ''
while len(equations) > 0:
    # Find an equation with only one variable
    for i, eqn in enumerate(equations):
        variables_in_eqn = re.findall('[a-z0-9_]+', eqn)
        variables_in_eqn=list(dict.fromkeys(variables_in_eqn))
        if len(variables_in_eqn) == 3 and variables_in_eqn[0] != X:
            regex += eqn.split('=')[1]
            var_to_remove = variables_in_eqn[0]
            break
    else:
        # No equation with only one variable found
        if len(equations) == 1:
            # Only one equation left, so it must be solved
            regex += equations[0].split('=')[1]
            break
        else:
            raise ValueError("Can't solve equations")

    # Substitute variable in other equations
    equations = [re.sub(f'\\b{var_to_remove}\\b', f'({regex})', eqn) for eqn in equations if eqn != equations[i]]
    X = var_to_remove

# Final result is stored in the regex variable
print(regex)