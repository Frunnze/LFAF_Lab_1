import random
import finite_automaton

class Grammar:
    # Define the constructor.
    def __init__(self, V_n, V_t, P, S):
        self.V_n = V_n
        self.V_t = V_t
        self.P = P
        self.S = S
    

    # Create the function which would generate a string.
    def generate_string(self):
        string, index = self.S, 0
        while (index < len(string)):
            # Check each symbol of the string.
            symbol = string[index]

            # If the symbol is a non-terminal.
            if symbol in self.V_n:
                # Randomly find a rule after -> for the non-terminal.
                post_rule = random.choice(self.P[symbol])

                # Replace the non-terminal with the found rule.
                string = string.replace(symbol, post_rule, 1)

                # Remain at the same index.
                index -= 1
            index += 1

        return string


    # Create the function which would generate 5 strings.
    def generate_strings(self):
        str_list, str_num = [], 5
        while (str_num != 0):
            string = self.generate_string()
            if string not in str_list:
                print(string)
                str_list.append(string)
                str_num -= 1
        return str_list


    # Convert the grammar object to a finite automaton object.
    def grammar_to_FA(self):
        # Create the alphabet for the FA.
        sigma = self.V_t

        # Create a list of states, which is just V_n + the final state.
        Q, F = [], 'X'
        Q = self.V_n
        Q.append(F)

        # Decide on the initial state and build the delta set.
        q0, delta = self.S, {}
        for state, productions in self.P.items():
            for production in productions:
                if len(production) == 1:
                    production += F
                if state in delta:
                    delta[state].append((production[0], production[1]))
                else:
                    delta[state] = [(production[0], production[1])]
        
        # Create an object of the type Finite_Automaton.
        return finite_automaton.Finite_Automaton(Q, sigma, delta, q0, F)