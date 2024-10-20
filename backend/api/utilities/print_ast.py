def print_ast(ast, level=0):
    if ast:
        print("  " * level + f"Node: {ast.type}, Value: {ast.value}")
        print_ast(ast.left, level + 1)
        print_ast(ast.right, level + 1)