
tableFile = open("./table1.txt")
action = [[0 for i in range(0,71)] for j in range(0,121)]
objFile = open("./1.obj")
wordListFile=open("./1.wordList")
code = []
debug = True
doflag = 0

def addToCode(s,p=-1):
	if(p==-1):
		arr = s.split("\n")
		for i in arr:
			if(not i==""):
				code.append(i)
	else:
		tmp = []
		print code,len(code)
		for i in range(p,len(code)):
			tmp.append(code[i])
			print i,len(code)
		code[p] = s
		for i in range(p+1,len(code)):
			code[i] = tmp[i-p-1]
		code.append(tmp[len(code)-p-1])


def gene_code(op,d,s,ss,mysigtable):
	global code
	if(op == 'equal'):
		if(not is_num(s)):
			try:
				dm = mysigtable.dict[d]
				sm = mysigtable.dict[s]
				tmp_code="LOAD R1,["+str(sm)+"]\nSTORE ["+str(dm)+"],R1\n"
				addToCode(tmp_code)
			except:
				print "Error: Undefined variable."
		else:
			dm = mysigtable.dict[d]
			tmp_code = "STORE ["+str(dm)+"],#"+str(s)+"\n"
			addToCode(tmp_code)
			
	if(op == "ADD"):
		tmp_code = ""
		if(not is_num(s)):
			s = mysigtable.dict[s]
			tmp_code+= "LOAD R4,["+str(s)+"]\n"
			s = "R1"
		else:
			s = "#"+s
		if(not is_num(ss)):
			ss = mysigtable.dict[ss]
			tmp_code+= "LOAD R5,["+str(ss)+"]\n"
			ss = "R2"
		else:
			ss = "#"+ss
		tmp_code +="ADD R3,"+s+","+ss+"\n"+"STORE ["+str(mysigtable.dict[d])+"],R3\n"
		addToCode(tmp_code)
	if(op == "SUB"):
		tmp_code = ""
		if(not is_num(s)):
			s = mysigtable.dict[s]
			tmp_code+= "LOAD R4,["+str(s)+"]\n"
			s = "R1"
		else:
			s = "#"+s
		if(not is_num(ss)):
			ss = mysigtable.dict[ss]
			tmp_code+= "LOAD R5,["+str(ss)+"]\n"
			ss = "R2"
		else:
			ss = "#"+ss
		tmp_code +="SUB R3,"+s+","+ss+"\n"+"STORE ["+str(mysigtable.dict[d])+"],R3\n"
		addToCode(tmp_code)
		
	if(op == "and list"):
		Blist = s
		tmp_code = ""
		for i in range(1,5):
			try:
				Blist[i] ="[" + str(mysigtable.dict[Blist[i]]) + "]"

			except:
				Blist[i] = "#" + str(Blist[i])
			tmp_code += "LOAD "+str(Blist[i])+",R"+str(i)+"\n"
		tmp_code +="SUB R1,R2\n"
		tmp_code +="SUB R3,R4\n"
		tmp_code +="OR R1,R3\n"
		tmp_code +="AND R1,#10000000\n"
		tmp_code +="MOV R30,R1\n"

		addToCode(tmp_code)
	if(op == "or list"):
		Blist = s
		tmp_code = ""
		for i in range(1,5):
			try:
				Blist[i] ="[" + str(mysigtable.dict[Blist[i]]) + "]"

			except:
				Blist[i] = "#" + str(Blist[i])
			tmp_code += "LOAD "+str(Blist[i])+",R"+str(i)+"\n"
		tmp_code +="SUB R1,R2\n"
		tmp_code +="SUB R3,R4\n"
		tmp_code +="AND R1,R3\n"
		tmp_code +="AND R1,#10000000\n"
		tmp_code +="MOV R30,R1\n"

		addToCode(tmp_code)

	if(op == "Relop list"):
		Blist = s
		tmp_code = ""
		for i in range(1,3):
			try:
				Blist[i] ="[" + str(mysigtable.dict[Blist[i]]) + "]"

			except:
				Blist[i] = "#" + str(Blist[i])
			tmp_code += "LOAD "+str(Blist[i])+",R"+str(i)+"\n"
		tmp_code +="SUB R1,R2\n"
		tmp_code +="AND R1,#10000000\n"
		tmp_code +="MOV R30,R1\n"
		addToCode(tmp_code)
	if(op == "while end"):
		whilelist = s
		dolist = d 
		tmp_code=""
		tmp_code+="JMP "+str(whilelist[1]-len(code)-1)+"\n"
		addToCode(tmp_code)
		tmp_code = ""
		tmp_code +="JNE "+str(len(code)-dolist[1])+",R30,#00000000"
		
		addToCode(tmp_code,d[1])
	if(op == "if then end"):
		thenlist = d 
		tmp_code=""
		tmp_code = ""
		print thenlist
		tmp_code +="JNE "+str(len(code)-thenlist[1])+",R30,#00000000"
		
		addToCode(tmp_code,d[1])


class node:
	def __init__(self, s, num ):
		self.s = s
		self.num = num
		self.inh=''
		self.sum=''

def is_num(num):
    try:
        int(num)
        return True
    except ValueError:
#        print "%s ValueError" % num
        return False

def read_table(f):

	row = 0
	for i in f:
		i = i.split("\n")[0]
		i = i.split("@")
		col=0
		for j in i:
			action[row][col] = j
			col+=1
			#print row,col
		row+=1
def read_source(f,src):
	for i in f:
		s=''
		for j in range(0,len(i)-1):
			s+=i[j]
		s=s.split("@")
		tmp = node(s[0],s[1])
		src.append(tmp)
	src.append(node("$",49))
class wordList:
	def __init__(self,f):
		self.Dict = {}
		for i in f:
			arr=i.split("@")
			tmp=arr[1].split("\n")
			self.Dict[arr[0]]=int(tmp[0])

class sig_table:
	def __init__(self):
		self.dict = {}
		self.tablelist = {}
		self.pc = 0


class mystack:
	def __init__(self):
		self.l = []
		self.flag=0
	def push(self,a):
		if(self.flag<len(self.l)):
			self.l[self.flag] = a
			self.flag+=1
		else:
			self.l.append(a)
			self.flag+=1
	def pop(self):
		if(self.flag>0):
			self.flag-=1
			return self.l[self.flag]
		else:
			return False
	def top(self):
		return self.l[self.flag-1]
	def show(self):
		s=''
		for i in range(0,self.flag):
			s+=str(self.l[i])
			s+=","
		print s,"flag :",self.flag
	def is_empty(self):
		if(self.flag == 0):
			return True
		else:
			return False

def addToTable(sig,state, word,s,mysigtable,guiyueshi):
	
	if(sig =="while" or sig == "do" or sig == "then"):
		mark = []
		mark.append(sig+" start")
		mark.append(len(code))
		s.push(mark)
	
	if((int(state) == 10 or int(state)==29)and int(word) == 61):
		mysigtable.dict[sig] = 'needToPatch'
		if(s.is_empty() or s.top()[0]!='List'):
			patchlist = []
			patchlist.append('List')
			patchlist.append(sig)
			s.push(patchlist)
		else:
			patchlist = s.top()
			patchlist.append(sig)
	if(int(state) == 27 and int(word) == 54):
		typelist = []
		typelist.append('type')
		typelist.append(sig)
		s.push(typelist)
	if((int(state) == 10 or int(state)== 29)and int(word) == 65):
		typelist = s.pop()
		size = 0

		if(typelist[1] == "integer"):
			size = 4
		else:
			if(typelist[1] == 'real'):
				size = 8
			else:
				print "wrong type",typelist[1]
				size = 16
		patchlist = s.pop()
		for i in patchlist:
			if(i != 'List'):
				mysigtable.dict[i] = mysigtable.pc
				mysigtable.pc += size

	if((int(state) == 11 or int(state) == 32 or int(state) == 98 or int(state) == 90) and int(word) == 69):
		leftlist = []
		leftlist.append("patchleft")
		leftlist.append(sig)
		s.push(leftlist)

	if((int(state) == 33 or int(state) == 57 or int(state) == 58 or int(state) == 89 or int(state) == 92 or int(state) == 44 or int(state) == 41) and int(word) == 53):
		Flist = []
		Flist.append("Flist")
		Flist.append(sig)
		s.push(Flist)
	if((int(state) == 33 or int(state) == 57 or int(state) == 58 or int(state) == 89 or int(state) == 92 or int(state) == 44 or int(state) == 41) and int(word) == 52):
		Tlist = s.top()
		Tlist[0] = "Tlist"
	if((int(state) == 33 or int(state) == 89 or int(state) == 92 or int(state) == 44 or int(state) == 41) and int(word) == 50):
		if(debug):
			print "!!!!!!!!!!!!!!!!!!!",guiyueshi
		if(guiyueshi == "reduceE->E+T"):
			Tlist = s.pop()
			Elist = s.top()
			Elist.append("+")
			Elist.append(Tlist[1])
		if(guiyueshi == "reduceE->E-T"):
			if(debug):
				print "!!!!!!!!!!!!!!!!!!!",guiyueshi
		
			Tlist = s.pop()
			Elist = s.top()
			Elist.append("-")
			Elist.append(Tlist[1])
		
		else:
			Elist = s.top()
			Elist[0] = "Elist"
	if((int(state) == 11 or int(state) == 32 or int(state) == 98 or int(state) == 44 or int(state ) == 90) and int(word) == 67 and guiyueshi=="reduceS0->Left:=E"):
		Elist = s.pop()
		leftlist = s.pop()
		if(debug == True and (type(Elist) != list or type(leftlist) != list) ):
			print "Get list failed."
			s.show()
			return 
		if(debug):
			print s.show(),"@@@@@@@@@@@@@@@@@@@"
		if(len(Elist) == 4):
			if(Elist[2] == "+"):
				gene_code("ADD",leftlist[1],Elist[1],Elist[3],mysigtable)
			if(debug):
				print "ADD","!!!!!!!!!!!!!!!!!!!!!!!!"
			if(Elist[2] == "-"):
				gene_code("SUB",leftlist[1],Elist[1],Elist[3],mysigtable)
			if(debug):
				print "ADD","!!!!!!!!!!!!!!!!!!!!!!!!"
		
		if(len(Elist) == 2):
			gene_code("equal",leftlist[1],Elist[1],Elist[1],mysigtable)
			if(debug):
				print "equal"
	
	if((int(state) == 92 or int(state) == 44 or int(state) == 41)and int(word) == 58):
		Blist = []
		Blist.append("Relop list")
		E2 = s.pop()
		E1 = s.pop()
		Blist.append(E1[1])
		Blist.append(E2[1])
		s.push(Blist)
		s.show()
	if((int(state) == 44 or int(state) == 41)and int(word) == 56):
		if(guiyueshi == "reduceB1->B2andB2"):
			Blist = []
			Blist.append("and list")
			B21 = s.pop()
			B22 = s.pop()
			Blist.append(B21[1])
			Blist.append(B21[2])
			Blist.append(B22[1])
			Blist.append(B22[2])
			s.push(Blist)
		if(guiyueshi == "reduceB1->B2orB2"):
			Blist = []
			Blist.append("or list")
			B21 = s.pop()
			B22 = s.pop()
			Blist.append(B21[1])
			Blist.append(B21[2])
			Blist.append(B22[1])
			Blist.append(B22[2])
			s.push(Blist)

	if((int(state)== 44 or int(state) == 41) and int(word) == 55):
		s.show()
		Blist = s.pop()
		gene_code(Blist[0],Blist,Blist,Blist,mysigtalbe)
	if(int(state) == 32 and int(word) == 67 and guiyueshi=="reduceS0->beginwhilewhileBdoSendwhile"):
		s.show()
		gene_code("while end",s.pop(),s.pop(),0,mysigtalbe)
	if(int(state) == 32 and int(word) == 67 and guiyueshi=="reduceS0->beginififBthenSendif"):
		s.show()
		gene_code("if then end",s.pop(),0,0,mysigtalbe)
	
def dealWithObj(src,action,stack,wl,yuyis,sigtalbe):
	length = len(src)
	stack.push(0)
	flag =0
	global doflag
	while(True):
		stack.show()
		print src[flag].s,src[flag].num	
		tmp = action[int(stack.top())][int(src[flag].num)]
		if(src[flag].s == "while"):
			addToTable("while",0,0,yuyis,sigtalbe,0)
			
		if(is_num(tmp)):
			if(src[flag].s == "do"):
				addToTable("do",0,0,yuyis,sigtalbe,0)
			if(src[flag].s == "then"):
				addToTable("then",0,0,yuyis,sigtalbe,0)
			stack.push(int(tmp))
			flag +=1
		else:
			if(tmp=='acc'):
				return 0
			else:
				print "this is tmp :",tmp
				tmp = tmp.split(" ")
				length = len(tmp)
				
				if(not tmp[length-1]=='-2' and not tmp[length-2]=='-2'):
					kkk = length - 4
					for i in range(0,kkk):
						stack.pop()
					state = stack.top()
					print state, wl.Dict[tmp[1]]
					stack.push(action[int(state)][wl.Dict[tmp[1]]])
					print "guiyue"+str(action[int(state)][wl.Dict[tmp[1]]])	
					print "this is src", src[flag-1].s
					guiyueshi = ""
					for guiyuetmp in tmp:
						guiyueshi +=guiyuetmp
					addToTable(src[flag-1].s, state, wl.Dict[tmp[1]],yuyis,sigtalbe,guiyueshi)
				
					
				else:
					print "guiyue wei kong "
					state = stack.top()
					stack.push(action[int(state)][wl.Dict[tmp[1]]])
		

src = []
read_source(objFile,src)
read_table(tableFile)
sta = mystack()
yuyi = mystack()
wl = wordList(wordListFile)
mysigtalbe = sig_table()

dealWithObj(src,action,sta,wl,yuyi,mysigtalbe)

print mysigtalbe.dict
for i in code:
	print i