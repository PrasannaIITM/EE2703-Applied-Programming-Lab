import numpy as np
from sys import argv, exit


CIRCUIT = ".circuit"
END = ".end"
AC = '.ac'



class element_def(): #class for the elements
    def __init__(self,line):
        self.line = line
        self.tokens = self.line.split()
        self.name = type_of_element(self.tokens[0])
        self.from_node = self.tokens[1]
        self.to_node = self.tokens[2]


        if len(self.tokens) == 5:
            self.type = 'dc'
            self.value = float(self.tokens[4])

        elif len(self.tokens) == 6:
            self.type = 'ac'
            Vm = float(self.tokens[4])/2
            phase = float(self.tokens[5])
            real = Vm * np.cos(phase)
            imag = Vm * np.sin(phase)
            self.value = complex(real,imag)

        else:
            self.type = 'dc-only'
            self.value = float(self.tokens[3])


def type_of_element(token): #get the element name 
                            #does not support dependent sources yet
    code_to_element = {"R": "resistor", "L": "inductor", "C": "capacitor", "V": "ind voltage source", "I": "ind current source" }
    return code_to_element.get(token[0], None)


def freq(lines): #Returns the frequency of the source
    w = 0
    for line in lines:
        if line[:3] == '.ac':
            w = float(line.split()[2])
    return w

def get_key(d,value): #Gets the corresponding key for a value in the dictionary
    for key in d.keys():
        if d[key] == value :
            return key

def node_mapping(circuit): #Returns a dictionary of nodes from the circuit definition.
    d = {"GND" : 0} 
    nodes = [element_def(line).from_node for line in circuit]
    nodes += [element_def(line).to_node for line in circuit]
    nodes = list(set(nodes)) #all distinct nodes

    #print(nodes)
    cnt = 1
    for node in nodes:
        if node != 'GND' :
            d[node] = cnt
            cnt += 1
    return d

def build_dict(circuit,e): #Makes a dictionary for each component of the particular type of element
    d = {}
    ele_names = [element_def(line).tokens[0] for line in circuit if element_def(line).tokens[0][0].lower()== e]
    for i, name in enumerate(ele_names):
        d[name] = i
    return d


def find_node(circuit, node_key, node_map): #Finds the lines and position ie from/to of the given node 
    inds = []
    for i in range(len(circuit)):
        for j in range(len(circuit[i].split())):
            if circuit[i].split()[j] in node_map.keys():
                if node_map[circuit[i].split()[j]] == node_key:
                    inds.append((i, j))

    return inds


def upd_matrix(node_key): #Updates the M and b matrix for the given node
    inds = find_node(circuit, node_key, node_map)
    for ind in inds:
        #getting all the attributes of the element using the class definition
        element = element_def(circuit[ind[0]])
        ele_name = circuit[ind[0]].split()[0]
        #resistors
        if ele_name[0] == 'R':
            if ind[1] == 1: #from_node
                neig_key = node_map[element.to_node]
                M[node_key, node_key] += 1/(element.value)
                M[node_key, neig_key] -= 1/(element.value)
                    
            if ind[1] == 2 : #to_node
                neig_key = node_map[element.from_node]
                M[node_key, node_key] += 1/(element.value)
                M[node_key, neig_key] -= 1/(element.value)      
        #inductors
        if ele_name[0] == 'L' :
            try:
                if ind[1]== 1:
                    neig_key = node_map[element.to_node]
                    M[node_key, node_key] -= complex(0,1/(2 * np.pi * w * element.value))
                    M[node_key, neig_key] += complex(0,1/(2 * np.pi * w * element.value))
                if ind[1] == 2 :
                    neig_key = node_map[element.from_node]
                    M[node_key, node_key] -= complex(0,1/(2 * np.pi * w * element.value))
                    M[node_key, neig_key] += complex(0,1/(2 * np.pi * w * element.value))
            except ZeroDivisionError: #in dc case as w = 0, handle it separately
                idx = ind_d[ele_name]
                if ind[1]== 1:
                    neig_key = node_map[element.to_node]
                    M[node_key, n + k + idx] += 1 
                    M[n + k + idx, node_key] -= 1
                    b[n + k + idx] = 0
                if ind[1]== 2:
                    M[node_key, n + k + idx] -= 1
                    M[n + k + idx, node_key] += 1
                    b[n + k + idx] = 0
        #capacitors
        if ele_name[0] == 'C' :
            if ind[1]== 1: #from_node
                neig_key = node_map[element.to_node]
                M[node_key, node_key] += complex(0, 2 * np.pi * w * (element.value))
                M[node_key, neig_key] -= complex(0, 2 * np.pi * w * (element.value))
            if ind[1] == 2 :#to_node
                neig_key = node_map[element.from_node]
                M[node_key, node_key] += complex(0, 2 * np.pi * w * (element.value))
                M[node_key, neig_key] -= complex(0, 2 * np.pi * w * (element.value))
        #independent voltage source
        if ele_name[0] == 'V' :
            index = volt_d[ele_name]
            if ind[1]== 1:
                neig_key = node_map[element.to_node]
                M[node_key,n+index] += 1
                M[n+index,node_key] -= 1
                b[n+index] = element.value
            if ind[1] == 2 :
                neig_key = node_map[element.from_node]
                M[node_key,n+index] -= 1
                M[n+index,node_key] +=1
                b[n+index] = element.value
        #independent current source
        if ele_name[0] == 'I' :
            if ind[1]== 1:
                b[node_key] -= element.value
            if ind[1] == 2 :
                b[node_key] += element.value
    
#main function starts here
#accept the name of netlist file as commandline
if len(argv) != 2:
    print('\nUsage: %s <inputfile>' % argv[0])  #check if the user has actually provided the 		
    				                            #filename or not and give appropriate error
					                            #message if needed.
    exit()
try:
    with open(argv[1]) as f:
        lines = f.readlines()
        w = freq(lines)  #frequency of the source, currently supports only single frequency circuits
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

        
        circuit = []
        for line in [' '.join(line.split('#')[0].split()) for line in lines[start+1:end]]:
            circuit.append(line)                
        #1. preprocessing of the file done

        node_map = node_mapping(circuit)
        #2. table of distinct nodes present in the circuit
        #numbers assigned to the nodes correspond to the rows of the incidence matirx


        volt_d = build_dict(circuit, "v")
        ind_d = build_dict(circuit,'l')
        
        k = len([i for i in range(len(circuit)) if circuit[i].split()[0][0] == 'V'])
        n = len(node_map)
        dim = n + k   
        #dimension of M if source is AC.
        #if source is DC, we need to add inductors also

        if w == 0: #dc signal, l acts as closed wire in steady state.
            M = np.zeros((dim+len(ind_d),dim+len(ind_d)),dtype=np.complex)
            b = np.zeros(dim+len(ind_d),dtype=np.complex)
        else:
            M = np.zeros((dim,dim),dtype=np.complex)
            b = np.zeros(dim,dtype=np.complex)

        for i in range(len(node_map)): #update matrix for the ith node
            upd_matrix(i)
        #as Vgnd = 0
        M[0] = 0
        M[0,0] =1

        #M and b arrays are constructed
        print('The node dictionary is :',node_map)
        print('M = :\n',M)
        print('b = :\n',b)


        #solve Mx = b
        try:
            x = np.linalg.solve(M,b)    
        except Exception:
            print('The incidence matrix cannot be inverted as it is singular.')
            sys.exit()

        print('Voltage convention -> From node is at a lower potential')     
        
        for i in range(n):
            print("Voltage at node {} is {}".format(get_key(node_map,i),x[i]))
        for j in range(k):
            print('Current through source {} is {}'.format(get_key(volt_d,j),x[n+j]))
        if w == 0:
            for i in range(len(ind_d)):
                print("Current through inductor {} is {}".format(get_key(ind_d,i),x[n+k+i]))


except IOError:
    print('Invalid file')
    exit()