def is_num(num):
    try:
        int(num)
        return True
    except ValueError:
#        print "%s ValueError" % num
        return False


f = open("./table1.htm")
f1 = open("./table1.txt","w")
row = -1
col = 0
action = [[0 for i in range(70)] for j in range(120)]
for i in range(120):
	for j in range(70):
		action[i][j]=-1

isfirst = 0
for i in f:
	
	flag = 0
	i = i.split("\n")[0]
	if(i == '<tr>'):
		row+=1
		col=-1
		flag = 1
		isfirst +=1
		print "this is row "+str(row)
	if(i == "</tr>"):
		flag = 1
	if(i == "<td nowrap>&nbsp;</td>"):
		col+=1
		flag = 1


	if(flag == 0):
		col+=1
		i = i.split("<td nowrap>")[1]
		i = i.split("</td>")[0]
		i = i.split("&nbsp;")
		if(is_num(i[0]) and isfirst == 0):
			#print "this is col "+str(col)+": goto "+i[0]
			action[row][col] = int(i[0])
		if(is_num(i[0]) and isfirst == 1):
			col-=1
			isfirst-=1
		if(i[0]=='accept'):
			action[row][col] = 'acc'
			print "get acc"
		if(i[0]=="shift"):

			#print "this is col "+str(col)+": shift "+i[1]
			action[row][col] = int(i[1])
		flagg=0
		if(i[0]=="reduce"):
			#print "this is col "+str(col)
			s = ''
			for j in i:
				s+=j
				s+=' '#there is an extra space. pay attention to the match problem
			
			action [row][col] = s

for i in action:
	for j in i:
		f1.write(str(j))
		f1.write("@")
	f1.write("\n")
print action[14]