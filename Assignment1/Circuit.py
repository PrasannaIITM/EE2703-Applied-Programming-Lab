FILE=input("Enter filename: ");
F=open(FILE, 'r');
F_new=F.readlines();

F_new=[i.replace('\n','') for i in F_new];

c1=0;
c2=0;
for i in range(len(F_new)):
	if F_new[i]==".circuit":
		c1=i;
	elif F_new[i]==".end":
		c2=i;
		break;

Circuit=[F_new[i] for i in range(c1+1,c2)];

Circuit=[i.split() for i in Circuit];

C={};
Circ={};
ConSou=["E","G","H","F"];
LLL=[];
for line in Circuit:
	L=[];
	for i in line:
		if "#" not in i:
			L.append(i);
		else:
			break;
	LLL+=[L];
Circuit=LLL;

for line in Circuit:
	if line[0][0] not in ConSou:
		n1=line[1];
		n2=line[2];
		Val=line[3];
		name=line[0];
		C.update({name:[n1,n2,Val]});
	else:
		if line[0][0] in ["E","G"]:
			[n1,n2,n3,n4]=line[1:5];
			Val=line[5];
			name=line[0];
			C.update({name:[n1,n2,n3,n4,Val]});
		else:
			n1=line[1];
			n2=line[2];
			Dep=line[3];
			Val=line[4];
			name=line[0];
			C.update({name:[n1,n2,Dep,Val]});
			
print(C,'\n');

def RevPrint():
	print(".circuit","\n");
	for line in Circuit:
		L=[i for i in reversed(line)];
		e=" ".join(L);
		print(e,"\n");
	print(".end");
	
RevPrint();
