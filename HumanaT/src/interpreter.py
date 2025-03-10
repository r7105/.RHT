class Interpreter:
    def __init__(self, statements):
        self.statements = statements
        self.variables = {}
        self.functions = {}

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
        elif statement[0] == 'functionStmt':
            self.functions[statement[1]] = statement
        elif statement[0] == 'returnStmt':
            return self.evaluate(statement[1])
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
