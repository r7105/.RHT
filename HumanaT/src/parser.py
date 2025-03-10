from lexer import TokenType

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
        return token.type == type and (value is None or token.value == value)

    def peek(self):
        return self.tokens[self.current]
