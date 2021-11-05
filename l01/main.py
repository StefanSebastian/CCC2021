
import os 


dir_path = os.path.dirname(os.path.realpath(__file__))
indir = 'level1'
output_file = os.path.join(dir_path, 'output')

inputs = [os.path.join(dir_path, indir, indir + f'_{x}.in')  for x in range(1, 6)]

out = []

def main():
    for input_file in inputs:
        with open(input_file, 'r') as fd:
            lines = [line.strip() for line in fd.readlines()]
            n = int(lines[0])
            print(n)

if __name__ == '__main__':
    print(inputs)
    main()
