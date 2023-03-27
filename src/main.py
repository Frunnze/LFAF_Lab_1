import lexer

keywords = ['and', 'as', 'assert', 'break', 'class', 'continue', 
            'def', 'del', 'elif', 'else', 'except', 'False', 'finally', 
            'for', 'from', 'global', 'if', 'import', 'in', 'is', 
            'lambda', 'None', 'nonlocal', 'not', 'or', 'pass', 
            'raise', 'return', 'True', 'try', 'while', 'with', 'yield', 'self']

python_program = '''
# Function that takes a list of numbers and returns their sum.
def sum_list(numbers): # The function.
    total = 0
    for num in numbers:
        total += num
    return total
my_numbers = [1, 2, 3, 4, 5]
print(sum_list(my_numbers))
'''

lexer_11 = lexer.Lexer(python_program, keywords)
tokens = lexer_11.get_tokens()
for token in tokens:
    print(token)