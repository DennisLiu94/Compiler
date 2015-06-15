f = open("./cha.txt")
f1 = open("./characterList.txt",'w')
counter = 0
for i in f:
	s = i.split(">")
	arr = s[1].split("<")
	print arr[0]
	tmp=arr[0]
	tmp+='@'
	tmp+=str(counter)
	tmp+='\n'
	counter+=1
	f1.write(tmp)
