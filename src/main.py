import lexer
from graphviz import Digraph
import AST
import parser_program


# Function to build a graph representation of an AST node and its children
def build_graph(node, graph):
    graph.node(str(id(node)), str(node))
    for child in node.children:
        graph.edge(str(id(node)), str(id(child)))
        build_graph(child, graph)


python_program = '''
def sum_list(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total
'''

# Tokenize the Python program using the lexer
lexer_11 = lexer.Lexer(python_program)
tokens = lexer_11.get_tokens_with_regex()

# Print the tokens
for token in tokens:
    print(token)

# Create an Abstract Syntax Tree (AST) from the tokens
ast = AST.AST.create_ast(tokens)

# Create a graph using the Digraph class from the graphviz library
graph = Digraph()

# Build the graph representation of the AST
build_graph(ast, graph)

# Render and view the AST graph
graph.render('ast_graph', format='png', view=True)

# Create the AST using the second method.
AST.AST.create_ast_method_2(python_program)


python_program = '''
total = total + num
'''

# Tokenize the Python program using the lexer
lexer_11 = lexer.Lexer(python_program)
tokens = lexer_11.get_tokens_with_regex()

# Print the tokens
for token in tokens:
    print(token)

# Parse the tokens using the parser
parser = parser_program.Parser(tokens)
parser.parse()