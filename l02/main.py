
import os 
import itertools

dir_path = os.path.dirname(os.path.realpath(__file__))
indir = 'level2'
output_file = os.path.join(dir_path, 'out')

inputs = [os.path.join(dir_path, indir, indir + f'_{x}.in')  for x in range(1, 6)]

outputs = [os.path.join(dir_path, output_file, indir + f'_{x}.out')  for x in range(1, 6)]



stack = []

def main():
    print(inputs)
    print(outputs)

    return 0

    for index, input_file in enumerate(inputs):
        out = []

        with open(input_file, 'r') as fd:
            lines = [line.strip() for line in fd.readlines()]
            n = int(lines[0])
            lines = lines[1:]
            # tokens = list(itertools.chain.from_iterable(lines))
            # tokens = ''.join()
            tokens = []
            for line in lines:
                tokens.extend(line.split(' '))
            
            tokens = tokens[1:-1]

            i = 0
            while i < len(tokens):
                token = tokens[i]

                if token == 'print':
                    out.append(tokens[i+1])
                    i += 2

            out = ''.join(out)


            with open(outputs[index], 'w') as fdout:
                fdout.write(out)

if __name__ == '__main__':
    # print(inputs)
    main()
