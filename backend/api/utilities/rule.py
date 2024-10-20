import re
from fastapi.responses import JSONResponse
from dataclasses import dataclass
from typing import List, Union, Dict, Any
from api.models.rule import CombineRulesInput
@dataclass
class Node:
    type: str
    value: str
    left: Union['Node', None] = None
    right: Union['Node', None] = None

class Parser:
    def __init__(self, rule_string: str):
        self.tokens = self.tokenize(rule_string)
        self.current = 0

    def tokenize(self, rule_string: str) -> List[str]:
        pattern = r'(\(|\)|\bAND\b|\bOR\b|[a-zA-Z_]\w*\s*(?:>|<|>=|<=|=)\s*(?:\d+|\'[^\']*\'))'
        return re.findall(pattern, rule_string)

    def parse(self) -> Node:
        return self.parse_expression()

    def parse_expression(self) -> Node:
        left = self.parse_term()
        while self.current < len(self.tokens) and self.tokens[self.current] == 'OR':
            self.current += 1
            right = self.parse_term()
            left = Node('operator', 'OR', left, right)
        return left

    def parse_term(self) -> Node:
        left = self.parse_factor()
        while self.current < len(self.tokens) and self.tokens[self.current] == 'AND':
            self.current += 1
            right = self.parse_factor()
            left = Node('operator', 'AND', left, right)
        return left

    def parse_factor(self) -> Node:
        if self.tokens[self.current] == '(':
            self.current += 1
            node = self.parse_expression()
            self.current += 1  # Consume closing parenthesis
            return node
        else:
            node = Node('operand', self.tokens[self.current])
            self.current += 1
            return node

def create_rule(rule_string: str) -> Node:
    parser = Parser(rule_string)
    return parser.parse()

# Helper function to print the AST
def print_ast(node: Node, level: int = 0):
    print('  ' * level + f"{node.type}: {node.value}")
    if node.left:
        print_ast(node.left, level + 1)
    if node.right:
        print_ast(node.right, level + 1)

def evaluate_rule(ast: Node, data: Dict[str, Any]) -> bool:
    if ast.type == "operand":
        key, operator, value = re.split(r'\s*(>|<|>=|<=|=)\s*', ast.value.strip(), maxsplit=2)
        
        if key not in data:
            return False
        
        data_value = data[key]
        
        # Convert value to the appropriate type
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]  # Remove quotes for string values
        elif value.replace('.', '').isdigit():
            value = float(value)
            data_value = float(data_value) if isinstance(data_value, (int, float)) else data_value
        
        # Perform the comparison
        if operator == ">":
            return data_value > value
        elif operator == "<":
            return data_value < value
        elif operator == ">=":
            return data_value >= value
        elif operator == "<=":
            return data_value <= value
        elif operator == "=":
            return data_value == value
        else:
            raise ValueError(f"Unsupported operator: {operator}")
    
    elif ast.type == "operator":
        if ast.value == "AND":
            return evaluate_rule(ast.left, data) and evaluate_rule(ast.right, data)
        elif ast.value == "OR":
            return evaluate_rule(ast.left, data) or evaluate_rule(ast.right, data)
    
    raise ValueError(f"Invalid AST node type: {ast.type}")



def combine_rules(rules: list[str], operator: str) -> Node:
    """
    Combine multiple rule strings into a single AST.
   
    :param rules: List of rule strings to combine
    :param operator: The operator to use for combining rules (e.g., 'AND', 'OR')
    :return: Combined AST
    """
    # Parse all rules into ASTs
    asts = [create_rule(rule) for rule in rules]
   
    # Combine ASTs
    if len(asts) == 1:
        return asts[0]
   
    combined_ast = asts[0]
    for ast in asts[1:]:
        combined_ast = Node('operator', operator, combined_ast, ast)
   
    return combined_ast


def is_valid_rule(rule: str) -> bool:
    """
    Check if a rule string is valid.
    
    :param rule: The rule string to validate
    :return: True if the rule is valid, False otherwise
    """
    # Check for balanced parentheses
    if rule.count('(') != rule.count(')'):
        return False
    
    # Split the rule into tokens
    tokens = re.findall(r'\(|\)|\bAND\b|\bOR\b|[a-zA-Z_]\w*\s*(?:>|<|>=|<=|=)\s*(?:\d+|\'[^\']*\')', rule)
    
    # Check for empty rule
    if not tokens:
        return False
    
    # Check each token
    for i, token in enumerate(tokens):
        if token in ('AND', 'OR'):
            # Logical operators should have operands on both sides
            if i == 0 or i == len(tokens) - 1:
                return False
            if tokens[i-1] in ('AND', 'OR', '(') or tokens[i+1] in ('AND', 'OR', ')'):
                return False
        elif token == '(':
            # Opening parenthesis should not be followed by a closing one or a logical operator
            if i == len(tokens) - 1 or tokens[i+1] in (')', 'AND', 'OR'):
                return False
        elif token == ')':
            # Closing parenthesis should not be preceded by an opening one or a logical operator
            if i == 0 or tokens[i-1] in ('(', 'AND', 'OR'):
                return False
        else:
            # Check if the token is a valid operand (e.g., "age > 30" or "department = 'Sales'")
            if not re.match(r'^[a-zA-Z_]\w*\s*(?:>|<|>=|<=|=)\s*(?:\d+|\'[^\']*\')$', token):
                return False
    
    return True
def sample_rule_check():
    rule_string = "age > 30 AND salary > 50000"
    data = {"age": 35, "salary": 60000}

    rule_ast = create_rule(rule_string)
    result = evaluate_rule(rule_ast, data)
    print(f"Evaluation Result: {result}")