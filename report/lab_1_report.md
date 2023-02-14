# Laboratory work nr. 1

### Course: Formal Languages & Finite Automata
### Author: Frunze Vladislav

----

## Theory
Definitions:
* Language - a means of communicating information, by using visual or audio interpretations of words (strings).
* Formal language - a set of strings based on an alphabet that are generated with the help of a grammar.
* String - a combination of symbols generated with the help of rules from the production set.
* Grammar - an entity defined by four elements: the set of non-terminal symbols, the set of terminal symbols, the start symbol, and the set of production rules.
* Automaton - an abstract, or as I like to call it, imaginary computational device.
* Finite automaton - an automaton with a finite amount of memory, that is, it has a limited amount of states and transitions. In addition, like a grammar, it is constituted of several elements: the finite set of states, an alphabet, a transition function, the initial state, and a set of final states.

Conversion from Grammar to FA:
<br/>
In order to convert a Grammar (regular) to a Finite automaton, we need to follow the below algorithm:
1. Equalize the alphabets.
2. Equalize the set of states with the set of non-terminal symbols. Also, add a final state.
3. Denote the initial state.
4. Create the transition function, which means associating a state with another state to which this transition goes. Take all the possible associations of the function and add them into a set.

## Objectives:

* To define what is a language and find out what it needs to be considered a formal language.
* To create a local and remote repository on GitHub for the laboratory work.
* Decide on a programming language to use for the laboratory.
* Create a report for the laboratory.
* Solve the given problems:
<br/>a) Implement a type/class for your grammar;
<br/>b) Add one function that would generate 5 valid strings from the language expressed by your given grammar;
<br/>c) Implement some functionality that would convert an object of type Grammar to one of type Finite Automaton;
<br/>d) For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;


## Implementation description
#### My grammar (variant 11):
```
Variant 11:
VN = {S, B, D}, 
VT = {a, b, c}, 
P = { 
    S → aB
    S → bB
    B → bD
    D → b
    D → aD
    B → cB
    B → aS
}
```

#### Grammar method which generates a string using the given grammar 
First, we initialize the string with the start symbol of the grammar. In an iteration of the "while" loop, we check the symbol of the string if it is a non-terminal symbol. If it is, we choose randomly a post-production rule (the rule after ->) for the non-terminal symbol, replace the non-terminal with the found rule, and remain at the same index for the next iteration.

```
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
```
The below function uses the one above to generate 5 strings:
```
    def generate_strings(self):
        str_list, str_num = [], 5
        while (str_num != 0):
            string = self.generate_string()
            if string not in str_list:
                print(string)
                str_list.append(string)
                str_num -= 1
        return str_list
```

#### Grammar method that converts the Grammar object to a Finite Automaton object:
First, we create the alphabet for FA, by attributing to it the set of terminal symbols from the Grammar. The same thing we do with the set of states by attributing to it the set of non-terminal symbols and a final state. In addition, we define the initial state of the automaton and build the delta set, and subsequently create the FA with the defined elements.
```
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
```

#### FA Method that checks if an input string can be obtained via state transition
In the first place, we initialize two variables: one contains the state, and the other the string that is formed by the transition. In an iteration of the "for" loop, we seek a state to go from the current state, and if we find one, we use the transition (terminal symbol) to reconstruct the mentioned string. After "for", if the strings are equal, and the state is the final one, then state transition is possible, otherwise, no.
```
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
```
Method 2:
```
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
```

#### The main file which instantiates the classes and tests class methods.
```
import grammar

# Write the grammar values.
V_n = ['S', 'B', 'D']
V_t = ['a', 'b', 'c']
P = {
    'S': ['aB', 'bB'],
    'B': ['bD', 'cB', 'aS'],
    'D': ['b', 'aD']
}

# Define a Grammar object.
grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')

# Generate 5 strings.
test_cases = grammar_11.generate_strings()

# Translate the grammar to FA.
FA = grammar_11.grammar_to_FA()

# Test the "check_string" methods.
test_cases.append('aaaffh')
test_cases.append('aaabbbbbbbbbbb')
test_cases.append('reredede')
test_cases.append('aaaaaaaaa')
test_cases.append('')
test_cases.append('aa')
print('\nTesting:')
for test in test_cases:
    print(test + ': ' + FA.check_string_method_1(test))
```

## Conclusions / Screenshots / Results
### Results:
Result 1:
```
abb
acbaaaaab
babaaaacccbb
aabcbaab
acbb

Testing:
abb: possible
acbaaaaab: possible
babaaaacccbb: possible
aabcbaab: possible
acbb: possible
```
Result 2:
```
bbaaab
acbb
bbb
aabaabb
aabaacbaaab

Testing:
bbaaab: possible
acbb: possible
bbb: possible
aabaabb: possible
aabaacbaaab: possible
```
Result 3 (with additional randomly chosen strings for testing):
```
acbab
bbaaab
aaaaaaabaaab
bcabbb
acccaabab

Testing:
acbab: possible
bbaaab: possible
aaaaaaabaaab: possible
bcabbb: possible
acccaabab: possible
aaaffh: impossible
aaabbbbbbbbbbb: impossible
reredede: impossible
aaaaaaaaa: impossible
a: impossible
aa: impossible
```

### Conclusions
* All in all, this laboratory work helped me understand more in-depth regular grammars, what a finite automaton is, and how to convert regular grammar to a finite automaton.
* Moreover, some methods like the "generate_string" method of the Grammar class or the "check_string" method of the Finite_Automaton method can be implemented in numerous ways.
* The last, can be used to check if you implemented the "generate_string" method correctly, which basically means that a Finite_Automaton object verifies a Grammar object.

## References
* Cojuhari I., Duca L., & Fiodorov I. Formal Languages and Finite Automata Guide for practical lessons. Technical University of Moldova
