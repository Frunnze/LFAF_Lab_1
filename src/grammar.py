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
    

    # Classify the grammar based on Chomsky's hierarchy.
    def classify_grammar(self):
        # Determine if it is a Recursively Enumerable Grammar or a Context-Sensitive Grammar.
        type_0_or_1 = False
        for key in self.P.keys():
            # Find if some left-side part of a production has a length > 1.
            if len(key) != 1:
                type_0_or_1 = True
                break
        if type_0_or_1 == True:
            for key in self.P.keys():
                for value in self.P[key]:
                    # Return type 0 if it has the epsilon in the right-side part of a production.
                    if value == '':
                        return 'Type 0. Recursively Enumerable Grammar'
            # Return type 1 if it doesn't have the epsilon.
            return 'Type 1. Context-Sensitive Grammar'

        # Determine if it is a Context-Free Grammar or Regular Grammar.
        if type_0_or_1 == False:
            right_RG = left_RG = False
            for key in self.P.keys():
                # Look in the right-side part of productions for non-Regular Grammars.
                for value in self.P[key]:
                    # Look through each symbol of the right-side part of productions.
                    for index, symbol in enumerate(value):
                        # Find if non-terminals are not in their place. That is, either right or left side.
                        if symbol in self.V_n and len(value) != 1:
                            if index == 0:
                                left_RG = True
                                if right_RG:
                                    return 'Type 2. Context-Free Grammar'
                            elif index == len(value) - 1:
                                right_RG = True
                                if left_RG:
                                    return 'Type 2. Context-Free Grammar'
                            else:
                                return 'Type 2. Context-Free Grammar'
            return 'Type 3. Regular Grammar'