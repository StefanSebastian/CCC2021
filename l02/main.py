
import os
import itertools

dir_path = os.path.dirname(os.path.realpath(__file__))
indir = 'level2'
output_file = os.path.join(dir_path, 'out')

inputs = [os.path.join(dir_path, indir, indir +
                       f'_{x}.in') for x in range(1, 6)]

outputs = [os.path.join(dir_path, output_file, indir +
                        f'_{x}.out') for x in range(1, 6)]


class Statement:
    def exec(self):
        raise Exception("DONT EXEC STATEMENTS")

    def length():
        raise Exception("DONT EXEC STATEMENTS")


class Start(Statement):
    def __init__(self, statements):
        self.statements = statements

    def exec(self):
        for statement in self.statements:
            statement.exec()

    def length(self):
        sum = 0

        for statement in self.execstatements:
            sum += statement.length()

        return


class Print(Statement):
    def __init__(self, token, output):
        self.token = token
        self.output = output

    def exec(self):
        self.output += [self.token]

    def length(self):
        return 2


class Return(Statement):
    def __init__(self, token):
        self.token = token

    def exec(self):
        raise Exception("DONE")

    def length(self):
        return 2


class IfElse(Statement):
    def __init__(self, condition, if_statements, else_statements):
        self.condition = condition
        self.if_statements = if_statements
        self.else_statements = else_statements

    def exec(self):
        if self.condition == 'true':
            for statement in self.if_statements:
                statement.exec()
        else:
            for statement in self.else_statements:
                statement.exec()

    def length(self):
        sum = 0

        for statement in self.if_statements:
            sum += statement.length()

        for statement in self.else_statements:
            sum += statement.length()

        return 5 + sum


def parse_if_else(tokens, output):
    if_statements = parse_statements(tokens[2:], output)

    sum = 0
    for statement in if_statements:
        sum += statement.length()

    else_statements = parse_statements(tokens[4 + sum:], output)
    return IfElse(tokens[1], if_statements, else_statements)


def parse_statements(tokens, output):
    if tokens[0] == 'start':
        return [Start(parse_statements(tokens[1:], output))]
    elif tokens[0] == 'print':
        return [Print(tokens[1], output)] + parse_statements(tokens[2:], output)
    elif tokens[0] == 'if':
        if_else_statement = parse_if_else(tokens, output)
        return [if_else_statement] + parse_statements(tokens[if_else_statement.length():], output)
    elif tokens[0] == 'return':
        return [Return(tokens[1])] + parse_statements(tokens[2:], output)
    elif tokens[0] == 'end':
        return []
    else:
        raise Exception("SHIT", tokens)


def main():
    print(inputs)
    print(outputs)

    for index, input_file in enumerate(inputs):
        out = []

        with open(input_file, 'r') as fd:
            lines = [line.strip() for line in fd.readlines()]
            lines = lines[1:]
            tokens = []
            for line in lines:
                tokens.extend(line.split(' '))

            startStatements = parse_statements(tokens, out)

            for startStatement in startStatements:
                try:
                    startStatement.exec()
                except:
                    pass

            out = ''.join(out)

            with open(outputs[index], 'w') as fdout:
                fdout.write(out)

            print("DONE")


if __name__ == '__main__':
    main()
