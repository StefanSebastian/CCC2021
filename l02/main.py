
import os 
import itertools

dir_path = os.path.dirname(os.path.realpath(__file__))
indir = 'level2'
output_file = os.path.join(dir_path, 'out')

inputs = [os.path.join(dir_path, indir, indir + '_example.in')] + [os.path.join(dir_path, indir, indir + f'_{x}.in')  for x in range(1, 6)]

outputs = [os.path.join(dir_path, output_file, indir + '_example.out')]+ [os.path.join(dir_path, output_file, indir + f'_{x}.out')  for x in range(1, 6)]



stack = []

def handle_return(tokens, out, i):
    raise ValueError('done job')

def handle_print(tokens, out, i):
    out.append(tokens[i+1])
    return i + 2

def handle_if(tokens, out, i, variables):
    next_ = tokens[i + 1]
    condition = False

    if next_ == 'true':
        condition = True
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
                tokens.extend(line.split(' '))
            
            tokens = tokens[1:-1]

            i = 0
            while i < len(tokens):
                token = tokens[i]
                try:
                    i = handlers[token](tokens, out, i)
                except ValueError:
                    break

            out = ''.join(out)

            with open(outputs[index], 'w') as fdout:
                fdout.write(out)

if __name__ == '__main__':
    # print(inputs)
    main()
