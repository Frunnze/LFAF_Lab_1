# Laboratory work nr. 3

### Course: Formal Languages & Finite Automata
### Author: Frunze Vladislav

----

## Theory:
Definitions:
- Lexical analysis - identification of tokens in a sequence of characters.
- Lexer - the tool used to accomplish the lexical analysis. 
- Token - the category of a lexeme in a sequence of characters. 
- Lexeme - the delimited entity in a sequence of characters that follows some pre-defined rules.

## Objectives:
1. To understand what lexical analysis is.
2. To get familiar with the inner workings of a lexer/scanner/tokenizer.
3. To implement a sample lexer of Python programming language and to show how it works.
4. To read references 1 and 2.
5. To create the report.

## Implementation description:
The lexer was written in Python for Python programming language. The class "Lexer" has just the constructor and one method called "get_tokens()". In the following sections, I will describe the constructor and the method part by part.
<br/><br/>
The tokens that I have identified in the Python programming language:
- Comment - the line that begins with '#'.
- Keyword - the list is given in the 'main' file.
- Identifier - The names given to functions, variables, etc.
- Number - integer and float numbers.
- String - the text between " and " or ' and '.
- Comparison - the comparison operators ">", "<", etc.
- Assignment - the assignment operators like "=", "+=" and so on.
- Arithmetic - the arithmetic operators like "+", "-".
- Separator - the symbols which delimit the above tokens.
- ASCII value - for unknown symbols the token name will be the ASCII value.


#### The constructor
The constructor helps to build the "Lexer" object by receiving the list of keywords in Python programming language and the Python program to tokenize.

```
    def __init__(self, program, keywords):
        self.program = program
        self.keywords = keywords
```

#### Lexer method that returns the list of tokens
First, we create a "while" loop that would analyze each character from the given program.

```
        while c < len(self.program):
```

Next, we identify and skip the whitespaces in order to get to the lexemes.

```
            if self.program[c].isspace():
                c += 1
```
<br/>
Further, we check if there is a comment token. Thus, we look if the current char is '#'. If it is, we find the index of the newline symbol '/n' at the end of the comment, and take the whole comment as the value of the token. However, the newline symbol might not be there if it is the end of the file, thus, we could just take the whole comment from the '#' char to the end of the file.

```
            elif self.program[c] == '#':
                new_line = self.program[c:].find('\n')
                if new_line != -1:
                    tokens.append(('COMMENT', self.program[c:c + new_line]))
                    c += new_line + 1
                elif new_line == -1:
                    tokens.append(('COMMENT', self.program[c:len(self.program)]))
                    c = len(self.program)
```
<br/>
Moreover, we seek the keyword or the identifier tokens. We do this if the current char of the loop is a letter or the underscore symbol. Taking into account the rules of Python to create an identifier, we build a string of the digits, letters, or underscores, with the first char a letter or an underscore. Then, we check if the built string is in the list of keywords, which would suggest that it belongs to the keyword token, otherwise to the identifier token.

```
            elif self.program[c].isalpha() or self.program[c] == '_':
                string = ''
                while c < len(self.program) and (self.program[c].isdigit() or self.program[c].isalpha() or self.program[c] == '_'):
                    string += self.program[c]
                    c += 1
                if string in self.keywords:
                    tokens.append(('KEYWORD', string))
                else:
                    tokens.append(('IDENTIFIER', string))
```
<br/>
Next, if the current char is a digit or a dot and the next char is also a digit then, we identify a number token from the next chars. We also create a boolean variable to not allow more than one dot in a number. If there are more dots combined with digits, then unnecessary dots should be taken as separator tokens.

```
            elif self.program[c].isdigit() or (self.program[c] == '.' and self.program[c + 1].isdigit()):
                number, dot = '', False
                while c < len(self.program) and (self.program[c].isdigit() or (self.program[c] == '.' and not dot)):
                    if self.program[c] == '.':
                        dot = True
                    number += self.program[c]
                    c += 1
                tokens.append(('NUMBER', number))
```
<br/>
Further, we identify string tokens. If the current char is a quote of either type, we take the whole text between the first quote and the next one of the same type. This string is added with its corresponding quotes in the token value cell of the tuple.

``` 
            elif self.program[c] == "'" or self.program[c] == '"':
                quote, string = self.program[c], ''
                c += 1
                while c < len(self.program) and self.program[c] != quote:
                    string += self.program[c]
                    c += 1
                tokens.append(('STRING', quote + string + quote))
                c += 1
```
<br/>
Next, we extract comparison operator tokens. If the current char and the next char belong to the below first list, or if the current char belongs to the below second list then we found a comparison operator token, which we add to the 'tokens' list accordingly with a tuple.

``` 
            elif self.program[c:c+2] in ['==', '!=', '<=', '>=']:
                tokens.append(('COMPARISON', self.program[c:c+2]))
                c += 2
            elif self.program[c] in ['<', '>']:
                tokens.append(('COMPARISON', self.program[c]))
                c += 1
```
<br/>
Moreover, we can identify assignment operator tokens. If the current char and the next char, as an entity, belong to the below first list, or if the current char is '=' then we found an assignment operator token, which we add to the 'tokens' list.

``` 
            elif self.program[c:c+2] in ['+=', '-=', '*=', '/=']:
                tokens.append(('ASSIGNMENT', self.program[c:c+2]))
                c += 2
            elif self.program[c] in '=':
                tokens.append(('ASSIGNMENT', self.program[c]))
                c += 1
```
<br/>
Next, we can determine arithmetic operator tokens. If the current char and the next char, as an entity, belong to ['//', '**'], or if the current char is in '+-*/%' then we found an arithmetic operator token, which we add to the 'tokens' list.

``` 
            elif self.program[c:c+2] in ['//', '**']:
                tokens.append(('ARITHMETIC', self.program[c:c+2]))
                c += 2
            elif self.program[c] in '+-*/%':
                tokens.append(('ARITHMETIC', self.program[c]))
                c += 1
```
<br/>
Also, we can identify separator tokens. If the current char is in '()[]{},.;:', then it is a separator char. Thus, we add it to the 'tokens' list.

``` 
            elif self.program[c] in '()[]{},.;:':
                tokens.append(('SEPARATOR', self.program[c]))
                c += 1
```

<br/>
Lastly, if the current char is unknown by the lexer, then the token name in the token tuple is going to be the ASCII value, and the lexeme is going to be the unknown char alone.

``` 
            else:
                tokens.append((ord(self.program[c]), self.program[c]))
                c += 1
```


#### The main file which instantiates the class and tests the method.
```
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
```

## Conclusions / Screenshots / Results
### Results:
Result 1:
```
Input:
# Function that takes a list of numbers and returns their sum.
def sum_list(numbers): # The function.
    total = 0
    for num in numbers:
        total += num
    return total
my_numbers = [1, 2, 3, 4, 5]
print(sum_list(my_numbers))

Output:
('COMMENT', '# Function that takes a list of numbers and returns their sum.')
('KEYWORD', 'def')
('IDENTIFIER', 'sum_list')
('SEPARATOR', '(')
('IDENTIFIER', 'numbers')
('SEPARATOR', ')')
('SEPARATOR', ':')
('COMMENT', '# The function.')
('IDENTIFIER', 'total')
('ASSIGNMENT', '=')
('NUMBER', '0')
('KEYWORD', 'for')
('IDENTIFIER', 'num')
('KEYWORD', 'in')
('IDENTIFIER', 'numbers')
('SEPARATOR', ':')
('IDENTIFIER', 'total')
('ASSIGNMENT', '+=')
('IDENTIFIER', 'num')
('KEYWORD', 'return')
('IDENTIFIER', 'total')
('IDENTIFIER', 'my_numbers')
('ASSIGNMENT', '=')
('SEPARATOR', '[')
('NUMBER', '1')
('SEPARATOR', ',')
('NUMBER', '2')
('SEPARATOR', ',')
('NUMBER', '3')
('SEPARATOR', ',')
('NUMBER', '4')
('SEPARATOR', ',')
('NUMBER', '5')
('SEPARATOR', ']')
('IDENTIFIER', 'print')
('SEPARATOR', '(')
('IDENTIFIER', 'sum_list')
('SEPARATOR', '(')
('IDENTIFIER', 'my_numbers')
('SEPARATOR', ')')
('SEPARATOR', ')')
```

Result 2:
```
Input:
# This program checks if a number is odd or even.
def check_odd_even(num):
    if num % 2 == 0:
        return "even"
    else:
        return "odd"
num = int(input("Enter a number: "))
result = check_odd_even(num)
print(num + " " + result)

Output:
('COMMENT', '# This program checks if a number is odd or even.')
('KEYWORD', 'def')
('IDENTIFIER', 'check_odd_even')
('SEPARATOR', '(')
('IDENTIFIER', 'num')
('SEPARATOR', ')')
('SEPARATOR', ':')
('KEYWORD', 'if')
('IDENTIFIER', 'num')
('ARITHMETIC', '%')
('NUMBER', '2')
('COMPARISON', '==')
('NUMBER', '0')
('SEPARATOR', ':')
('KEYWORD', 'return')
('STRING', '"even"')
('KEYWORD', 'else')
('SEPARATOR', ':')
('KEYWORD', 'return')
('STRING', '"odd"')
('IDENTIFIER', 'num')
('ASSIGNMENT', '=')
('IDENTIFIER', 'int')
('SEPARATOR', '(')
('IDENTIFIER', 'input')
('SEPARATOR', '(')
('STRING', '"Enter a number: "')
('SEPARATOR', ')')
('SEPARATOR', ')')
('IDENTIFIER', 'result')
('ASSIGNMENT', '=')
('IDENTIFIER', 'check_odd_even')
('SEPARATOR', '(')
('IDENTIFIER', 'num')
('SEPARATOR', ')')
('IDENTIFIER', 'print')
('SEPARATOR', '(')
('IDENTIFIER', 'num')
('ARITHMETIC', '+')
('STRING', '" "')
('ARITHMETIC', '+')
('IDENTIFIER', 'result')
('SEPARATOR', ')')
```

Result 3:
```
Input:
# What happens with unknown symbols.
unknown_1 = $
unknown_2 = @

Output:
('COMMENT', '# What happens with unknown symbols.')
('IDENTIFIER', 'unknown_1')
('ASSIGNMENT', '=')
(36, '$')
('IDENTIFIER', 'unknown_2')
('ASSIGNMENT', '=')
(64, '@')
```

Result 4:
```
Input:
number = 200.200..200..

Output:
('IDENTIFIER', 'number')
('ASSIGNMENT', '=')
('NUMBER', '200.200')
('SEPARATOR', '.')
('NUMBER', '.200')
('SEPARATOR', '.')
('SEPARATOR', '.')
```

Result 5: Tokenizing the tokenizer (only the first 23 tokens)
```
Output:
('KEYWORD', 'class')
('IDENTIFIER', 'Lexer')
('SEPARATOR', ':')
('KEYWORD', 'def')
('IDENTIFIER', '__init__')
('SEPARATOR', '(')
('KEYWORD', 'self')
('SEPARATOR', ',')
('IDENTIFIER', 'program')
('SEPARATOR', ',')
('IDENTIFIER', 'keywords')
('SEPARATOR', ')')
('SEPARATOR', ':')
('KEYWORD', 'self')
('SEPARATOR', '.')
('IDENTIFIER', 'program')
('ASSIGNMENT', '=')
('IDENTIFIER', 'program')
('KEYWORD', 'self')
('SEPARATOR', '.')
('IDENTIFIER', 'keywords')
('ASSIGNMENT', '=')
('IDENTIFIER', 'keywords')
```

### Conclusions
* Lexer is an indispensable part of the compiler or interpreter, as it has to send the tokens to the parser, which builds a syntax tree from the given tokens.
* To build a Lexer you need the tokens or in other words, the categories of symbols or combinations of symbols that you might find in the given sequence of characters.
* You can create a "get_tokens()" method in various ways. One way is to go through each char of the given sequence and analyze where it belongs by creating cases for each token that you have identified.

## References
* "Kaleidoscope Introduction and the Lexer." LLVM Tutorial: https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html
* "Lexical analysis." Wikipedia: https://en.wikipedia.org/wiki/Lexical_analysis