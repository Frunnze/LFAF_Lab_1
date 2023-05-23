import re

class Lexer:
    def __init__(self, program):
        self.program = program

    # Return the list of tokens (lab 3).
    def get_tokens(self):
        tokens, c = [], 0
        keywords = ['and', 'as', 'assert', 'break', 'class', 'continue', 
            'def', 'del', 'elif', 'else', 'except', 'False', 'finally', 
            'for', 'from', 'global', 'if', 'import', 'in', 'is', 
            'lambda', 'None', 'nonlocal', 'not', 'or', 'pass', 
            'raise', 'return', 'True', 'try', 'while', 'with', 'yield', 'self']

        while c < len(self.program):
            # Skip whitespaces.
            if self.program[c].isspace():
                c += 1

            # Identify the comment token.
            elif self.program[c] == '#':
                new_line = self.program[c:].find('\n')
                if new_line != -1:
                    tokens.append(('COMMENT', self.program[c:c + new_line]))
                    c += new_line + 1
                elif new_line == -1:
                    tokens.append(('COMMENT', self.program[c:len(self.program)]))
                    c = len(self.program)

            # Find keyword and identifier tokens.
            elif self.program[c].isalpha() or self.program[c] == '_':

                # Find the next delimited string.
                string = ''
                while c < len(self.program) and (self.program[c].isdigit() or self.program[c].isalpha() or self.program[c] == '_'):
                    string += self.program[c]
                    c += 1

                # Determine if the string is an identifier or a keyword.
                if string in keywords:
                    tokens.append(('KEYWORD', string))
                else:
                    tokens.append(('IDENTIFIER', string))

            # Find number token.
            elif self.program[c].isdigit() or (self.program[c] == '.' and self.program[c + 1].isdigit()):
                number, dot = '', False
                while c < len(self.program) and (self.program[c].isdigit() or (self.program[c] == '.' and not dot)):
                    if self.program[c] == '.':
                        dot = True
                    number += self.program[c]
                    c += 1
                tokens.append(('NUMBER', number))

            # Identify string token.
            elif self.program[c] == "'" or self.program[c] == '"':
                quote, string = self.program[c], ''
                c += 1
                while c < len(self.program) and self.program[c] != quote:
                    string += self.program[c]
                    c += 1
                tokens.append(('STRING', quote + string + quote))
                c += 1

            # Identify comparison token.
            elif self.program[c:c+2] in ['==', '!=', '<=', '>=']:
                tokens.append(('COMPARISON', self.program[c:c+2]))
                c += 2
            elif self.program[c] in ['<', '>']:
                tokens.append(('COMPARISON', self.program[c]))
                c += 1

            # Identify assignment token.
            elif self.program[c:c+2] in ['+=', '-=', '*=', '/=']:
                tokens.append(('ASSIGNMENT', self.program[c:c+2]))
                c += 2
            elif self.program[c] in '=':
                tokens.append(('ASSIGNMENT', self.program[c]))
                c += 1

            # Identify arithmetic operator token.
            elif self.program[c:c+2] in ['//', '**']:
                tokens.append(('ARITHMETIC', self.program[c:c+2]))
                c += 2
            elif self.program[c] in '+-*/%':
                tokens.append(('ARITHMETIC', self.program[c]))
                c += 1

            # Identify separator token.
            elif self.program[c] in '()[]{},.;:':
                tokens.append(('SEPARATOR', self.program[c]))
                c += 1

            # In case the char is unknown, write its ASCII value.
            else:
                tokens.append((ord(self.program[c]), self.program[c]))
                c += 1
        return tokens
    

    # Return the list of tokens (lab 5).
    def get_tokens_with_regex(self):
        tokens = []
        
        # Regular expressions for different token types
        token_types = [
            ('NUMBER', r'\d+(\.\d*)?'),            
            ('STRING', r'\".*?\"|\'.*?\''),                  
            ('KEYWORD', r'(if|else|while|for|def|return|in)(?!\w)'), 
            ('IDENTIFIER', r'[a-zA-Z_]\w*'),                 
            ('OPERATOR', r'[+\-*%/]'),                      
            ('COMPARISON', r'==|!=|<=|>=|<|>'),             
            ('ASSIGNMENT', r'='),                            
            ('SEPARATOR', r'\(|\)|\[|\]|\{|\}|,|;|:'),
            ('NEWLINE', r'\n'),                              
            ('SKIP', r'[ \t]+'),                              
            ('COMMENT', r'#.*'),                              
            ('UNKNOWN', r'.'),                                
        ]

        # Create a pattern by joining the regular expressions for all token types
        token_pattern = '|'.join('(?P<%s>%s)' % spec for spec in token_types)

        # Compile the pattern into a regular expression object
        regex = re.compile(token_pattern)

        # Iterate over matches in the input string
        for match in regex.finditer(self.program):
            # Get the token type from the match group name
            token_type = match.lastgroup

            # Get the actual matched value
            token_value = match.group(token_type)

             # Add the token to the list
            if token_type == 'UNKNOWN':
                tokens.append((token_type, ord(token_value)))
            elif token_type != 'SKIP' and token_type != 'NEWLINE':
                tokens.append((token_type, token_value)) 
            
        return tokens