
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
indir = 'level3'
output_file = os.path.join(dir_path, 'out')

inputs = [os.path.join(dir_path, indir, indir + '_example.in')] + \
    [os.path.join(dir_path, indir, indir + f'_{x}.in') for x in range(1, 6)]

outputs = [os.path.join(dir_path, output_file, indir + '_example.out')] + \
    [os.path.join(dir_path, output_file, indir +
                  f'_{x}.out') for x in range(1, 6)]


class Statement:
    def exec(self, output, variables):
        raise Exception("DONT EXEC STATEMENTS")

    def length():
        raise Exception("DONT EXEC STATEMENTS")


class Start(Statement):
    def __init__(self, statements):
        self.statements = statements

    def exec(self, output, variables):
        for statement in self.statements:
            statement.exec(output, variables)

    def length(self):
        sum = 0

        for statement in self.execstatements:
            sum += statement.length()

        return


class Print(Statement):
    def __init__(self, token):
        self.token = token

    def exec(self, output, variables):
        if self.token in variables:
            self.token = variables[self.token].value
        output += [self.token]

    def length(self):
        return 2


class Return(Statement):
    def __init__(self, token):
        self.token = token

    def exec(self, output, variables):
        raise EnvironmentError("DONE")

    def length(self):
        return 2


class IfElse(Statement):
    def __init__(self, condition, if_statements, else_statements):
        self.condition = condition
        self.if_statements = if_statements
        self.else_statements = else_statements

    def exec(self, output, variables):
        if self.condition in variables:
            self.condition = variables[self.condition].value

        if self.condition != 'true' and self.condition != 'false':
            output.clear()
            output += ["ERROR"]
            raise EnvironmentError("ERROR")

        if self.condition == 'true':
            for statement in self.if_statements:
                statement.exec(output, variables)
        else:
            for statement in self.else_statements:
                statement.exec(output, variables)

    def length(self):
        sum = 0

        for statement in self.if_statements:
            sum += statement.length()

        for statement in self.else_statements:
            sum += statement.length()

        return 5 + sum


class Var(Statement):
    def __init__(self, variable):
        self.variable = variable

    def exec(self, output, variables):
        if self.variable.name in variables:
            output.clear()
            output += ["ERROR"]
            raise EnvironmentError("ERROR")

        if self.variable.value in variables:
            self.variable.value = variables[self.variable.value].value

        variables[self.variable.name] = self.variable

    def length(self):
        return 3


class Set(Statement):
    def __init__(self, variable):
        self.variable = variable

    def exec(self, output, variables):
        if not self.variable.name in variables:
            output.clear()
            output += ["ERROR"]
            raise EnvironmentError("ERROR")

        if self.variable.value in variables:
            self.variable.value = variables[self.variable.value].value

        variables[self.variable.name] = self.variable

    def length(self):
        return 3


class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value


def parse_if_else(tokens):
    if_statements = parse_statements(tokens[2:])

    sum = 0
    for statement in if_statements:
        sum += statement.length()

    else_statements = parse_statements(tokens[4 + sum:])
    return IfElse(tokens[1], if_statements, else_statements)


def parse_statements(tokens):
    if tokens[0] == 'start':
        return [Start(parse_statements(tokens[1:]))]
    elif tokens[0] == 'print':
        return [Print(tokens[1])] + parse_statements(tokens[2:])
    elif tokens[0] == 'if':
        if_else_statement = parse_if_else(tokens)
        return [if_else_statement] + parse_statements(tokens[if_else_statement.length():])
    elif tokens[0] == 'set':
        return [Set(Variable(tokens[1], tokens[2]))] + parse_statements(tokens[3:])
    elif tokens[0] == 'var':
        return [Var(Variable(tokens[1], tokens[2]))] + parse_statements(tokens[3:])
    elif tokens[0] == 'return':
        return [Return(tokens[1])] + parse_statements(tokens[2:])
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

            programs = []

            for token in tokens:
                if token == "start":
                    programs.append([])
                programs[-1].append(token)

            startStatements = []
            for program in programs:
                startStatements += parse_statements(program)

            print(len(startStatements))

            variables = {}
            output = ""

            for startStatement in startStatements:
                variables = {}
                out = []

                try:
                    startStatement.exec(out, variables)
                except EnvironmentError:
                    pass

                output += ''.join(out) + "\n"

            with open(outputs[index], 'w') as fdout:
                fdout.write(output)

            print("DONE")


if __name__ == '__main__':
    main()
