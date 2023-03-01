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