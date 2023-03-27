class Lexer:
    def __init__(self, program, keywords):
        self.program = program
        self.keywords = keywords

    # Return the list of tokens.
    def get_tokens(self):
        tokens, c = [], 0
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
                if string in self.keywords:
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