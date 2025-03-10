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

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.match(TokenType.EOF):
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.match(TokenType.KEYWORD, 'say'):
            return self.printStmt()
        elif self.match(TokenType.KEYWORD, 'let'):
            return self.assignStmt()
        elif self.match(TokenType.KEYWORD, 'if'):
            return self.ifStmt()
        elif self.match(TokenType.KEYWORD, 'repeat'):
            return self.loopStmt()
        elif self.match(TokenType.KEYWORD, 'while'):
            return self.whileStmt()
        else:
            raise SyntaxError('Unexpected token: ' + self.peek().value)

    def printStmt(self):
        value = self.consume(TokenType.STRING)
        return ('printStmt', value.value)

    def assignStmt(self):
        identifier = self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.KEYWORD, 'be')
        value = self.expression()
        return ('assignStmt', identifier.value, value)

    def ifStmt(self):
        condition = self.expression()
        self.consume(TokenType.KEYWORD, 'then')
        statement = self.statement()
        return ('ifStmt', condition, statement)

    def loopStmt(self):
        times = self.consume(TokenType.NUMBER)
        self.consume(TokenType.KEYWORD, 'times')
        statement = self.statement()
        return ('loopStmt', int(times.value), statement)

    def whileStmt(self):
        condition = self.expression()
        self.consume(TokenType.KEYWORD, 'do')
        statement = []
        while not self.match(TokenType.KEYWORD, 'end'):
            statement.append(self.statement())
        self.consume(TokenType.KEYWORD, 'end')
        return ('whileStmt', condition, statement)

    def expression(self):
        if self.match(TokenType.NUMBER):
            return ('number', self.consume(TokenType.NUMBER).value)
        elif self.match(TokenType.STRING):
            return ('string', self.consume(TokenType.STRING).value)
        elif self.match(TokenType.IDENTIFIER):
            return ('identifier', self.consume(TokenType.IDENTIFIER).value)
        elif self.match(TokenType.KEYWORD, 'is greater than'):
            left = self.expression()
            self.consume(TokenType.KEYWORD, 'is greater than')
            right = self.expression()
            return ('is greater than', left, right)
        elif self.match(TokenType.KEYWORD, 'is less than'):
            left = self.expression()
            self.consume(TokenType.KEYWORD, 'is less than')
            right = self.expression()
            return ('is less than', left, right)
        elif self.match(TokenType.KEYWORD, 'is equal to'):
            left = self.expression()
            self.consume(TokenType.KEYWORD, 'is equal to')
            right = self.expression()
            return ('is equal to', left, right)
        else:
            raise SyntaxError('Unexpected token in expression: ' + self.peek().value)

    def consume(self, type, value=None):
        token = self.peek()
        if token.type != type or (value and token.value != value):
            raise SyntaxError('Expected ' + (value or type) + ' but found ' + token.value)
        self.current += 1
        return token

    def match(self, type, value=None):
        token = self.peek()
        return token.type == type and (value is None or token.value is None or token.value == value)

    def peek(self):
        return self.tokens[self.current]

class Interpreter:
    def __init__(self, statements):
        self.statements = statements
        self.variables = {}

    def run(self):
        for statement in self.statements:
            self.execute(statement)

    def execute(self, statement):
        if statement[0] == 'printStmt':
            print(statement[1][1:-1])
        elif statement[0] == 'assignStmt':
            self.variables[statement[1]] = self.evaluate(statement[2])
        elif statement[0] == 'ifStmt':
            if self.evaluate(statement[1]):
                self.execute(statement[2])
        elif statement[0] == 'loopStmt':
            for _ in range(statement[1]):
                self.execute(statement[2])
        elif statement[0] == 'whileStmt':
            while self.evaluate(statement[1]):
                for stmt in statement[2]:
                    self.execute(stmt)
        else:
            raise RuntimeError('Unknown statement: ' + statement[0])

    def evaluate(self, expression):
        if expression[0] == 'number':
            return int(expression[1])
        elif expression[0] == 'string':
            return expression[1][1:-1]
        elif expression[0] == 'identifier':
            return self.variables[expression[1]]
        elif expression[0] in ('is greater than', 'is less than', 'is equal to'):
            left = self.evaluate(expression[1])
            right = self.evaluate(expression[2])
            if expression[0] == 'is greater than':
                return left > right
            elif expression[0] == 'is less than':
                return left < right
            elif expression[0] == 'is equal to':
                return left == right
        else:
            raise RuntimeError('Unknown expression: ' + expression[0])

def run(code):
    tokens = tokenize(code)
    parser = Parser(tokens)
    statements = parser.parse()
    interpreter = Interpreter(statements)
    interpreter.run()

# Example usage
code = '''
say "Hello, World!"
let x be 5
if x is greater than 3 then say "x is greater than 3"
repeat 5 times say "Hello"
let y be 0
while y is less than 3 do
    say "y is " + y
    let y be y + 1
end
'''
run(code)
