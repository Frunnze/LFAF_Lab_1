import random
import itertools
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
        

    # Laboratory nr. 4.
    # Eliminate epsilon productions.
    def eliminate_eps(self):
        N_eps = self.S
        while N_eps != None:
            N_eps = None
            for left_side in self.P.keys():
                for right_side in self.P[left_side]:
                    if '' == right_side:
                        # Delete the epsilon productions, if found.
                        self.P[left_side].remove(right_side)
                                
                        # Remember the right side non-terminal of the found epsilon production.
                        N_eps = left_side
                        break

                # Delete the left side of the production if there are no right side symbols for it.
                if N_eps and len(self.P[N_eps]) == 0:
                    del self.P[left_side]
                    break

            # Add the productions to offset the epsilon elimination.
            if N_eps:
                # Make a copy of the production dictionary.
                copy_P = {k: list(v) for k, v in self.P.items()}

                # Go through each production and find the once with the N_eps.
                for left_side in self.P.keys():
                    for right_side in self.P[left_side]:
                        if N_eps in right_side:
                            # Find all indices where the N_eps occurs in the string.
                            indices = [i for i, char in enumerate(right_side) if char == N_eps]

                            # Generate all possible combinations of the indices where N_eps occurs.
                            combinations = []
                            for i in range(1, len(indices) + 1):
                                for combination in itertools.combinations(indices, i):
                                    combinations.append(combination)

                            # Generate all possible productions with or without N_eps based on the combinations.
                            new_productions = []
                            for combination in combinations:
                                temp = right_side
                                for i in combination[::-1]:
                                    temp = temp[:i] + temp[i+1:]
                                new_productions.append(temp)
                            
                            # Use the copy of the dictionary to save the new productions.
                            copy_P[left_side].extend(list(dict.fromkeys(new_productions)))
                
                # Store the new productions in the original dictionary.
                self.P = {k: list(v) for k, v in copy_P.items()}
        return self.P
    

    # Eliminate renamings in the CFG.
    def eliminate_renaming(self):
        keys_to_delete = []

        # Go through each production.
        for left_side in self.P.keys():
            unit_prod = True

            # Stop only if there are no unit productions with the same left side non-terminal.
            while unit_prod:
                unit_prod = False

                # Go through all productions in which the left side is the same.
                for right_side in self.P[left_side]:

                    # Eliminate cases such as A -> A
                    if right_side == left_side:
                        self.P[left_side].remove(right_side)
                        unit_prod = True

                    # Check if some production has the right side as a non-terminal.
                    elif right_side in self.V_n:
                        unit_prod = True

                        # Deal with situations when the found non-terminal is not a key of the dictionary.
                        if right_side not in self.P.keys():
                            self.P[left_side].remove(right_side)

                        # Deal with non-cyclic renamings.
                        elif left_side not in self.P[right_side]:
                            # Delete the found right side non-terminal and add its productions.
                            self.P[left_side].remove(right_side)
                            self.P[left_side] += self.P[right_side]
                        
                        # Deal with cyclic reanamings.
                        elif left_side in self.P[right_side]:
                            # Delete the non-terminal of the current production from the productions of the found non-terminal.
                            while left_side in self.P[right_side]:
                                self.P[right_side].remove(left_side)

                            # Delete the found right side non-terminal and add its productions.
                            self.P[left_side].remove(right_side)
                            self.P[left_side] += self.P[right_side]

                            # Delete all the productions with the non-terminals that created cycles.
                            self.P[right_side] = []
                            keys_to_delete.append(right_side)
                    
            self.P[left_side] = list(dict.fromkeys(self.P[left_side]))

        for key in list(self.P.keys()):
            if len(self.P[key]) == 0 or key in keys_to_delete:
                del self.P[key]
        return self.P
    

    # Eliminate non-productive non-terminals in a CFG.
    def eliminate_non_productive(self):
        # Find all the productions where the left-side is a non-terminal and the right-side is just one terminal.
        prod = []
        for left_side in self.P.keys():
            for right_side in self.P[left_side]:
                if right_side in self.V_t:
                    prod.append(left_side)
                    break

        # Use the found productive non-terminals to find other productives.
        prod_found = True
        while prod_found:
            prod_found = False
            for left_side in self.P.keys():
                if left_side not in prod:
                    for right_side in self.P[left_side]:
                        count = 0
                        for symbol in right_side:
                            if symbol in self.V_n and symbol not in prod:
                                break
                            count += 1
                        if count == len(right_side):
                            prod.append(left_side)
                            prod_found = True
                            break
                    if prod_found:
                        break

        # Find the difference between non-terminal and productive lists to indentify the non-productives.
        non_prod = list(set(self.V_n) - set(prod))

        # Eliminate the productions with the non-productives.
        for left_side in self.P.keys():
            temp_list = self.P[left_side][:]
            for right_side in self.P[left_side]:
                if any(symbol in right_side for symbol in non_prod):
                    temp_list.remove(right_side)
            self.P[left_side] = temp_list
        for key in non_prod:
            if key in self.P.keys():
                del self.P[key]

        self.V_n = prod
        return self.P
    

    # Eliminate inaccessible symbols in a CFG.
    def eliminate_inaccessibles(self):
        # Initialize the access list with the start symbol.
        acces = [self.S]

        # Find all the symbols of the productions that you can access through 'S'.
        for symbol in acces:
            if symbol in self.P.keys():
                for right_side in self.P[symbol]:
                    for s in list(right_side):
                        if s not in acces:
                            acces.append(s)
        
        # Determine the inaccessibles list and delete them from V_n and V_t sets.
        inacces = list(set(self.V_n + self.V_t) - set(acces))
        self.V_n = [s for s in self.V_n if s not in inacces]
        self.V_t = [s for s in self.V_t if s not in inacces]

        # Delete the keys of the dictioanary that are non-terminals in the inaccessibles list.
        for key in inacces:
            if key in self.P.keys():
                del self.P[key]
        
        # Delete every production in which the right side contains inaccessible symbols.
        for left_side in self.P.keys():
            temp_list = self.P[left_side][:]
            for right_side in self.P[left_side]:
                if any(symbol in right_side for symbol in inacces):
                    temp_list.remove(right_side)
            self.P[left_side] = temp_list
        return self.P
    

    # Translate the prepared CFG into the Chomsky Normal Form.
    def to_CNF(self):
        # Create a new start symbol S0 if the start symbol S occurs on some right side.
        for left_side in list(self.P.keys()):
            for right_side in self.P[left_side]:
                if self.S in right_side:
                    self.S = 'S0'
                    self.V_n.append('S0')
                    self.P['S0'] = ['S']
                    break

        self.eliminate_eps()
        self.eliminate_renaming()
        self.eliminate_non_productive()
        self.eliminate_inaccessibles()

        # Bring the right sides of all productions in a list format.
        self.P = {k: [list(prod) for prod in v] for k, v in self.P.items()}

        # Create a temporary dictioanry to note which terminal needs a non-terminal assigned.
        temp_dict = {k: '' for k in self.V_t}

        # Use this variable to create the new non-terminals.
        new_non_terminal = 0

        # Go through each production except the ones as S -> a.
        for left_side in list(self.P.keys()):
            for index, right_side in enumerate(self.P[left_side]):
                if len(right_side) > 1:

                    # Go through each symbol of a right side of a production.
                    for i, s in enumerate(right_side):

                        # Replace the terminal with a non-terminal and add the last to the P set.
                        if s in self.V_t:
                            if temp_dict[s] == '':
                                new_non_terminal += 1
                                new_NT = 'X' + str(new_non_terminal)
                                self.P[new_NT] = [[s]]
                                temp_dict[s] = new_NT
                                self.V_n.append(new_NT)
                            else:
                                new_NT = temp_dict[s]
                            self.P[left_side][index][i] = new_NT
        

        # Go through the right sides of productions.
        keys_list = list(self.P.keys())
        x_dict = {}
        for left_side in keys_list:
            for index, right_side in enumerate(self.P[left_side]):
                if len(right_side) > 2:
                    new_NT = None
                    # Check if there are new non-terminals (X...) that contain the same right part.
                    for x, v in x_dict.items():
                        if v == self.P[left_side][index][1:]:
                            new_NT = x
                            break

                    # Replace the right part with the found new non-terminal, otherwise create a new non-terminal.
                    if new_NT:
                        del self.P[left_side][index][1:]
                        self.P[left_side][index].append(new_NT)
                    else:
                        new_non_terminal += 1
                        new_NT = 'X' + str(new_non_terminal)
                        self.P[new_NT] = [self.P[left_side][index][1:]]
                        x_dict[new_NT] = self.P[left_side][index][1:]
                        self.V_n.append(new_NT)
                        del self.P[left_side][index][1:]
                        self.P[left_side][index].append(new_NT)
                        keys_list.append(new_NT)
        
        return self.P