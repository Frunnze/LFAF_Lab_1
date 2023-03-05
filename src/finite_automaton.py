import grammar
import graphviz


class Finite_Automaton:
    # Define the constructor.
    def __init__ (self, Q, sigma, delta, q0, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    # Check if an input string can be obtained via state transition.
    def check_string_method_1(self, string):
        # Initialize the variables
        searched_state, re_string = self.q0, ''

        # Take a symbol of the string.
        for symbol in string:
            # Check where you have to go from the state you are in.
            for production in self.delta[searched_state]:
                if production[0] == symbol:
                    searched_state = production[1]

                    # Reconstruct the string by using the transition symbols.
                    re_string += production[0]
                    break

            # If you found the final state, exit the loop.
            if searched_state == self.F:
                break
            print(re_string)
        
        # If the strings are equal, and the state is the final one, then it is possible.
        if re_string == string and searched_state == self.F:
            return 'possible'
        else:
            return 'impossible'


    # Method 2 to check a string if it can be obtained via state transition.
    def check_string_method_2(self, string):
        searched_state = self.q0
        for index, symbol in enumerate(string):
            find_state = None
            for production in self.delta[searched_state]:
                if production[0] == symbol:
                    find_state = production[1]
                    break
            if not find_state:
                return 'impossible'
            elif find_state == self.F:
                if index == len(string) - 1:
                    return 'possible'
                else:
                    return 'impossible'
            else:
                searched_state = find_state
        return 'impossible'
    

    # Convert a finite automaton to a regular grammar.
    def FA_to_RG(self):
        # Set the non-terminals equal to the set of states.
        V_n = self.Q

        # Set the terminals equal to the alphabet.
        V_t = self.sigma

        # Set the start symbol.
        S = self.q0

        # Creat the production set by eliminating the final state from delta.
        P = {}
        for key in self.delta.keys():
            for production in self.delta[key]:
                if key not in P:
                    P[key] = []
                if production[1] in self.F:
                    P[key].append(production[0])
                else:
                    P[key].append(production[0] + production[1])

        # Use the above to create an RG object.
        return grammar.Grammar(V_n, V_t, P, S)
    

    # Determine if the FA is deterministic or non-deterministic.
    def get_type(self):
        # Look through each right-side of each production.
        for key in self.delta.keys():
            for i in range(len(self.delta[key])):
                for j in range(i + 1, len(self.delta[key])):

                    # If at least one state goes to two ore more states with the same transition.
                    if self.delta[key][i][0] == self.delta[key][j][0]:

                        # Return that it is an NDFA
                        return 'NDFA'
                    
        # Return DFA if it doesn't have such transitions.
        return 'DFA'


    # Convert NDFA to DFA.
    def convert_to_DFA(self):
        # Define a new delta set and state set.
        DFA_delta, Qn = {}, []

        # Initialize the starting state.
        self.q0 = (self.q0,)
        Qn.append(self.q0)

        # Go through each obtained new state beginning with the starting state.
        for state in Qn:

            # Check if the new state can go to other states with any transitions.
            for transition in self.sigma:
                new_state = ()

                # Go through each sub-state of a new state and look at their productions.
                for sub_state in state:
                    if sub_state in self.delta:
                        for production in self.delta[sub_state]:

                            # Create the new state if you find transitions from the present state.
                            if transition == production[0]:
                                new_state += (production[1],)

                        # Add the new state to the states' set.
                        if new_state not in Qn and new_state != ():
                            Qn.append(new_state)

                # Form the delta set for the DFA.
                if new_state != ():      
                    if state in DFA_delta:
                        DFA_delta[state].append((transition, new_state))
                    else:
                        DFA_delta[state] = [(transition, new_state)]

        # Define the new state set.
        self.Q = Qn

        # Define the new delta set.
        self.delta = DFA_delta

        # Find the final states and define it.
        final_state = []
        for state in self.delta.keys():
            if self.F in state:
                final_state.append(state)
        if self.F not in self.delta:
            final_state.append((self.F,))
        self.F = final_state

    
    # Represent the finite automaton graphically.
    def show_graphically(self):
        # Create a new graph
        graph = graphviz.Digraph()

        # Add nodes to the graph
        for state in self.delta.keys():
            if state in self.F:
                graph.node(str(state), shape='doublecircle')
            else:
                graph.node(str(state))
            for next_state in self.delta[state]:
                if next_state[1] in self.F:
                    graph.node(str(next_state[1]), shape='doublecircle')

        # Add edges to the graph
        for state in self.delta.keys():
            for transition, next_state in self.delta[state]:
                graph.edge(str(state), str(next_state), label=transition)

        # Render the graph
        graph.render('finite_automaton', format='png', view=True)