class myStack:#This is a stack
	def __init__(self):
		self.counter=0
		self.stack=[]
		self.state=0
		
	def push(self,a,b):
		self.stack.append(a)
		self.counter+=1
		self.state=b
	def push(self,a):
		self.stack.append(a)
		self.counter+=1
	def getWord(self,c):
		s=''
		for i in self.stack:
			s+=i
		
		stateValue=c.getValue(self.state,s)
		return (s,stateValue)
	def clear(self):
		self.state=0
		self.coutner=0
		self.stack=[]

class wordList:#This is a word list
	def __init__(self,a,b):
		self.dict={}
		self.reservedDict={}
		self.OperatorDict={}	
		for i in a:
			arr=i.split("@")
			tmp=arr[1].split("\n")
			self.reservedDict[arr[0]]=int(tmp[0])
		for i in b:
			i = i.split("@")
			
			tmp = i[1].split("\n")[0]
			self.OperatorDict[i[0]]=int(tmp)
		
	def getValue(self,k,s):
		if(k==2):
			try:
				return self.reservedDict[str(s)]
			except Exception,e:
				
				return self.reservedDict["id"]
		if(k==3):
			try:
				return self.OperatorDict[str(s)]
			except Exception,e:
				return 10086
			
		else:
			return 7
			

class syntaxAnalyzer:#the analyzer
	def __init__(self,a,b):
		self.c=a
		self.stack=myStack()
		self.result=[]
		self.OperatorDict ={}
		for i in b:
			i = i.split("@")
			self.OperatorDict[i[0]]=int(i[1].split("\n")[0])
	def isOperator(self,a):
		try:
				k=self.OperatorDict[str(a)]
				return True
		except Exception,e:
			return False
	def isCharacter(self,j):
		if(j>='a' and j<='z' or j>='A' and j<='Z'):
			return True
		else:
			return False
	def isNumber(self,j):
		if(j>='0' and j<='9'):
			return True
		else:
			return False
	def getOneRes(self):
		self.result.append(self.stack.getWord(self.c))
		self.stack.clear()
	def jump(self,j):#state transfer
		if(self.isNumber(j) and (self.stack.state==0 ) ):
			self.stack.state=1
			self.stack.push(j)
			return True
		if(self.isCharacter(j) and (self.stack.state==0 )):
			self.stack.state=2
			self.stack.push(j)
			return True
		if(self.isOperator(j) and (self.stack.state==0 )):
			self.stack.state=3
			self.stack.push(j)
			return True
		if(self.stack.state==1 and (self.isCharacter(j) or self.isOperator(j))):
			self.getOneRes()
			if(self.isCharacter(j)):
				self.stack.state=2
				self.stack.push(j)
			if(self.isOperator(j)):
				self.stack.state=3
				self.stack.push(j)
			return True
		if(self.stack.state==2 and self.isOperator(j)):
			self.getOneRes()
			self.stack.state=3
			self.stack.push(j)
			return True
		if(self.stack.state==3 and (self.isCharacter(j) or self.isNumber(j))):
			self.getOneRes()
			if(self.isCharacter(j)):
				self.stack.state=2
				self.stack.push(j)
			if(self.isNumber(j)):
				self.stack.state=1
				self.stack.push(j)
			return True
		return False
	def isLegal(self,s):
		if(self.isNumber(s) or self.isCharacter(s) or  self.isOperator(s)):
			return True
		else:
			return False
	def analyze(self,s,counter):
		#state1:number state2:ID state3:operator state4:reserved word
		
		arr=s.split(" ")
		for i in arr:
			if(i[0]=="#"):
				return 
			self.stack.clear()
			for j in i:
				
				if(not self.isLegal(j) and not j=='\n'):
					print "illegal character at "+str(counter+1)+"th line:"+str(j) 
				tmp=self.jump(j)
				if(tmp==False and not j=='\n'):
					self.stack.push(j)

			if(self.stack.state!=0):
				self.getOneRes()
				
	def res(self):
		return self.result

f1=open("./1.wordList")
f2=open("./1.source")
f3=open("./1.operatorList")
c=wordList(f1,f3)
f3.close()
f3=open("./1.operatorList")
f4 = open("./1.obj","w")
anaObj=syntaxAnalyzer(c,f3) 
s=[]
counter = 0
for i in f2:
	anaObj.analyze(i,counter)
	counter+=1
res = anaObj.res()
for i in res:
	f4.write(str(i[0])+"@"+str(i[1])+"\n")

