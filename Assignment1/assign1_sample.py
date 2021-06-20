from sys import argv, exit


CIRCUIT = ".circuit"
END = ".end"

#accept the name of netlist file as commandline
if len(argv) != 2:
    print('\nUsage: %s <inputfile>' % argv[0]) #check if the user has actually provided the 						#filename or not and give appropriate error
						#message if needed.
    exit()


try:
    with open(argv[1]) as f:
        lines = f.readlines()
        start = -1
        end = -2
        for line in lines:              # extracting circuit definition start and end lines
            if CIRCUIT == line[:len(CIRCUIT)]:
                start = lines.index(line)
            elif END == line[:len(END)]:
                end = lines.index(line)
                break
        if start >= end:                # validating circuit block
            print('Invalid circuit definition')
            exit(0)

        for line in reversed([' '.join(reversed(line.split('#')[0].split())) for line in lines[start+1:end]]):
            print(line)                 # print output
	
except IOError:
    print('Invalid file')
    exit()



