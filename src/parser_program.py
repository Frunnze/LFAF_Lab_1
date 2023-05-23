class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # List of tokens to parse
        self.current_token = None  # Current token being parsed
        self.index = -1  # Current index of the token being parsed
        self.next_token()  # Get the next token

    def next_token(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None

    def match(self, expected_token):
        # Check if the current token matches the expected token
        if self.current_token and self.current_token[0] == expected_token:
            self.next_token()  # Move to the next token
        else:
            raise SyntaxError(f"Expected {expected_token}, but found {self.current_token[0]}")

    def parse_expression(self):
        # Parse an expression consisting of terms and operators
        self.parse_term()
        while self.current_token and self.current_token[0] == 'OPERATOR':
            self.match('OPERATOR')
            self.parse_term()

    def parse_term(self):
        # Parse a term, which can be an identifier or a number
        if self.current_token and self.current_token[0] in ['IDENTIFIER', 'NUMBER']:
            self.match(self.current_token[0])
        else:
            raise SyntaxError(f"Expected IDENTIFIER or NUMBER, but found {self.current_token[0]}")

    def parse_assignment(self):
        # Parse an assignment statement
        self.match('IDENTIFIER')  # Expect an identifier
        self.match('ASSIGNMENT')  # Expect an assignment operator
        self.parse_expression()  # Parse the expression on the right-hand side of the assignment

    def parse_statement(self):
        # Parse a statement, which is an assignment statement
        self.parse_assignment()
        if self.current_token:
            raise SyntaxError(f"Unexpected token: {self.current_token[0]}")

    def parse(self):
        try:
            self.parse_statement()
            print("Parsing successful. The statement is correctly written.")
        except SyntaxError as e:
            print("Parsing failed. The statement is incorrectly written.")
            print(e)