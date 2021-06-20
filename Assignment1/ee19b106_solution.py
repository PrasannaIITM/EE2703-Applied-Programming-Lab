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
		tokens = {}
		for line in lines[start+1:end][::-1]:
			line = line.split("#")[0].split()
			#print(line)
			name = line[0]
			if line[0][0] == "R":
				typ = "Resistor"
			elif line[0][0] == "L":
				typ = "Inductor"
			elif line[0][0] == "C":
				typ = "Capacitor"
			elif line[0][0] == "V":
				typ = "Independent Voltage source"
			elif line[0][0] == "I":
				typ = "Independent Current source"
			elif line[0][0] == "E":
				typ = "Voltage Controlled Voltage Source"
			elif line[0][0] == "G":
				typ = "Voltage Controlled Current Source"
			elif line[0][0] == "H":
				typ = "Current Controlled Voltage Source"
			elif line[0][0] == "F":
				typ = "Current Controlled Current Source"
				
			if line[0][0] in ["R", "L", "C", "V", "I"]:
				fromNode = line[1]
				toNode = line[2]
				val = line[3]
				tokens[name] = {"type" : typ, "from_node" : fromNode, "to_node" : toNode, "value" : val}
			elif line[0][0] in ["E", "G"]:
				fromNode = line[1]
				toNode = line[2]
				n3 = line[3]
				n4 = line[4]
				val = line[5]
				tokens[name] = {"type" : typ, "from_node" : fromNode, "to_node" : toNode, "n3_node" : n3, "n4_node" : n4, "value" : val}
			else:
				fromNode = line[1]
				toNode = line[2]
				voltageSource = line[3]
				val = line[4]
				tokens[name] = {"type" : typ, "from_node" : fromNode, "to_node" : toNode,"voltage_source" : voltageSource,"value" : val}
				
			
				
						
			line = line[::-1]
			print(" ".join(line))
		print(tokens)
		
except IOError:
	print('Invalid file')
	exit()

