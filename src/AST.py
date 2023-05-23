import ast

class ASTNode:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        return child

    def __str__(self):
        return f'{self.token_type}: {self.value}'


class AST:
    def create_ast(tokens):
        # Create the root node of the AST
        root = ASTNode('PROGRAM')

        # Construct the AST by adding child nodes
        current_node = root
        current_node = current_node.add_child(ASTNode(tokens[0][0], tokens[0][1]))
        current_node.add_child(ASTNode(tokens[1][0], tokens[1][1]))
        current_node.add_child(ASTNode(tokens[3][0], tokens[3][1]))
        current_node = current_node.add_child(ASTNode('body', None))
        parent = current_node
        current_node = current_node.add_child(ASTNode(tokens[7][0], tokens[7][1]))
        current_node.add_child(ASTNode(tokens[6][0], tokens[6][1]))
        current_node.add_child(ASTNode(tokens[8][0], tokens[8][1]))
        current_node = parent
        current_node = current_node.add_child(ASTNode(tokens[9][0], tokens[9][1]))
        current_node.add_child(ASTNode(tokens[10][0], tokens[10][1]))
        current_node.add_child(ASTNode(tokens[11][0], tokens[11][1]))
        current_node.add_child(ASTNode(tokens[12][0], tokens[12][1]))
        current_node = current_node.add_child(ASTNode(tokens[15][0], tokens[15][1]))
        current_node.add_child(ASTNode(tokens[14][0], tokens[14][1]))
        current_node = current_node.add_child(ASTNode(tokens[17][0], tokens[17][1]))
        current_node.add_child(ASTNode(tokens[16][0], tokens[16][1]))
        current_node.add_child(ASTNode(tokens[18][0], tokens[18][1]))
        current_node = parent
        current_node = current_node.add_child(ASTNode(tokens[19][0], tokens[19][1]))
        current_node.add_child(ASTNode(tokens[20][0], tokens[20][1]))

        # Return the root of the constructed AST
        return root
    

    def create_ast_method_2(source_code):
        # Parse the source code into an AST using the 'ast' module
        tree = ast.parse(source_code)

        # Print the AST for debugging or analysis
        print(ast.dump(tree))