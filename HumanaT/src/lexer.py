import re

class TokenType:
    STRING = 'STRING'
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    KEYWORD = 'KEYWORD'
    EOF = 'EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

def tokenize(code):
    tokens = []
    token_spec = [
        (TokenType.STRING, r'"[^"]*"'),
        (TokenType.NUMBER, r'\d+'),
        (TokenType.IDENTIFIER, r'[a-zA-Z_]\w*'),
        (TokenType.KEYWORD, r'\bsay\b|\blet\b|\bbe\b|\bif\b|\bthen\b|\brepeat\b|\btimes\b|\bis greater than\b|\bis less than\b|\bis equal to\b|\bwhile\b|\bdo\b|\bend\b'),
    ]
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_spec)
    for match in re.finditer(tok_regex, code):
        type = match.lastgroup
        value = match.group()
        tokens.append(Token(type, value))
    tokens.append(Token(TokenType.EOF, ''))
    return tokens
