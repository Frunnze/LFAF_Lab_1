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
test_cases.append('a')
test_cases.append('aa')
print('\nTesting:')
for test in test_cases:
    print(test + ': ' + FA.check_string_method_1(test))