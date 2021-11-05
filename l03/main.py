
import os 
import itertools

dir_path = os.path.dirname(os.path.realpath(__file__))
indir = 'level3'
output_file = os.path.join(dir_path, 'out')

inputs = [os.path.join(dir_path, indir, indir + '_example.in')] + [os.path.join(dir_path, indir, indir + f'_{x}.in')  for x in range(1, 6)]

outputs = [os.path.join(dir_path, output_file, indir + '_example.out')]+ [os.path.join(dir_path, output_file, indir + f'_{x}.out')  for x in range(1, 6)]

stack = []


def handle_return(tokens, out, i, variables):
    raise ValueError('done job')

def handle_print(tokens, out, i, variables):
    out.append(tokens[i+1])
    return i + 2

def handle_var(tokens, out, i, variables):
    name = tokens[i + 1]
    value = tokens[i + 2]

    if name in variables:
        out.clear()
        out.append('ERROR')
        raise ValueError('done job')

    variables[name] = value
    return i + 3

def handle_set(tokens, out, i, variables):
    name = tokens[i + 1]
    value = tokens[i + 2]

    if name not in variables:
        out.clear()
        out.append('ERROR')
        raise ValueError('done job')

    variables[name] = value
    return i + 3

def handle_condition(literal, out, variables):
    if literal == 'true':
        return True
    if literal == 'false':
        return False

    if literal not in variables:
        out.clear()
        out.append('ERROR')
        raise ValueError('done job')

    return variables[literal]

def handle_if(tokens, out, i, variables):
    next_ = tokens[i + 1]
    condition = handle_condition(next_, out, variables)
    i += 2

    while True:
        if tokens[i] == 'end':
            i += 1
            break
        if condition:
            i = handlers[tokens[i]](tokens, out, i, variables)
        else:
            i += 1
    if tokens[i] == 'else':
        i += 1
        while True:
            if tokens[i] == 'end':
                i += 1
                break
            if not condition:
                i = handlers[tokens[i]](tokens, out, i, variables)
            else:
                i += 1
    return i

handlers = {
    'return': handle_return,
    'var': handle_var,
    'set': handle_set,
    'print': handle_print,
    'if': handle_if,
}

def main():
    print(inputs)
    print(outputs)

    for index, input_file in enumerate(inputs):
        out = []

        with open(input_file, 'r') as fd:
            lines = [line.strip() for line in fd.readlines()]
            n = int(lines[0])
            lines = lines[1:]
            tokens = []
            for line in lines:
                tokens.extend(line.split())
            
            # tokens = tokens[1:-1]

            programs = []

            for token in tokens:
                if token == 'start':
                    programs.append([])
                programs[-1].append(token)

            print(programs)
            out_file = []

            for program in programs:
                i = 0
                out = []
                program = program[1:-1]
                variables = {}

                aux = tokens
                tokens = program

                while i < len(tokens):
                    token = tokens[i]
                    try:
                        i = handlers[token](tokens, out, i, variables)
                    except ValueError:
                        break

                tokens = aux
                out_file.append(''.join(out))

            out_file = '\n'.join(out_file)
            with open(outputs[index], 'w') as fdout:
                fdout.write(out_file)


if __name__ == '__main__':
    # print(inputs)
    main()
