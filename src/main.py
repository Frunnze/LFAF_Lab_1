import grammar
import finite_automaton as FA

# Write the grammar values (variant 11 from lab 1).
V_n = ['S', 'B', 'D']
V_t = ['a', 'b', 'c']
P = {
    'S': ['aB', 'bB'],
    'B': ['bD', 'cB', 'aS'],
    'D': ['b', 'aD']
}

# Define a Grammar object.
grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')

# Classify the grammar.
print(grammar_11.classify_grammar())

# Write the FA inputs. (variant 11 from lab 2)
Q = ['0', '1', '2', '3']
sigma = ['a', 'b', 'c']
F = '3'
delta = {
    '0': [('a', '1'), ('b', '2')], 
    '1': [('b', '2'), ('a', F)],
    '2': [('c', '0'), ('c', F)]
}

# Define an FA object.
FA_11 = FA.Finite_Automaton(Q, sigma, delta, '0', F)
FA_11.show_graphically()

# Convert FA to RG.
RG = FA_11.FA_to_RG()
print('\n')
print("V_n = ", RG.V_n)
print("V_t = ", RG.V_t)
print("S = ", RG.S)
print("P = ", RG.P, '\n')

# Find the type of the given FA.
print(FA_11.get_type())

# Convert the NDFA to DFA.
FA_11.convert_to_DFA()
print(FA_11.get_type(), "\n")

print("Q = ", FA_11.Q)
print("sigma = ", FA_11.sigma)
print("delta = ", FA_11.delta)
print("q0 = ", FA_11.q0)
print("F = ", FA_11.F)