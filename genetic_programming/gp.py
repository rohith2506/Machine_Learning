from random import random,randint,choice
from copy import deepcopy
from math import log

class fwrapper:
	def __init__(self,function,childcount,name):
		self.function=function
		self.childcount=childcount
		self.name=name

class node:
	def __init__(self,fw,children):
		self.function=fw.function
		self.name=fw.name
		self.children=children

	def evaluate(self,inp):
		results=[n.evaluate(inp) for n in self.children]
		return self.function(results)

	def display(self,indent=0):
		print (' '*indent)+self.name
		for c in self.children:
			c.display(indent+1)


class paramnode:
	def __init__(self,idx):
		self.idx=idx
	def evaluate(self,inp):
		return inp[self.idx]

	def display(self,indent=0):
		print '%sp%d' % (' '*indent,self.idx)

class constnode:
	def __init__(self,v):
		self.v=v
	def evaluate(self,inp):
		return self.v
	def display(self,indent=0):
		print '%s%d' % (' '*indent,self.v)


addw=fwrapper(lambda l:l[0]+l[1],2,'add')
subw=fwrapper(lambda l:l[0]-l[1],2,'subtract')
mulw=fwrapper(lambda l:l[0]*l[1],2,'multiply')

def iffunc(l):
	if l[0]>0: return l[1]
	else: return l[2]

ifw=fwrapper(iffunc,3,'if')

def isgreater(l):
	if l[0]>l[1]: return 1
	else: return 0

gtw=fwrapper(isgreater,2,'isgreater')
flist=[addw,mulw,ifw,gtw,subw]

def exampletree( ):
	return node(ifw,[
		node(gtw,[paramnode(0),constnode(3)]),
		node(addw,[paramnode(1),constnode(5)]),
		node(subw,[paramnode(1),constnode(2)]),
		])

def makerandomtree(pc,maxdepth=4,fpr=0.5,ppr=0.6):
	if random( )<fpr and maxdepth>0:
		f=choice(flist)
		children=[makerandomtree(pc,maxdepth-1,fpr,ppr)
			for i in range(f.childcount)]
		return node(f,children)
	elif random( )<ppr:
		return paramnode(randint(0,pc-1))
	else:
		return constnode(randint(0,10))

def hiddenfunction(x,y):
	return x**2+2*y+3*x+5

def buildhiddenset():
	rows=[]
	for i in range(200):
		x=randint(0,40)
		y=randint(0,40)
		rows.append([x,y,hiddenfunction(x,y)])
	return rows

def scorefunction(tree,s):
	dif=0
	for data in s:
		v=tree.evaluate([data[0],data[1]])
		dif+=abs(v-data[2])
#		print dif
	return dif

random1=makerandomtree(2)
random2=makerandomtree(2)
exampletree = exampletree()
#print exampletree.evaluate([2,3])
#print exampletree.evaluate([5,3])
#print exampletree.display()
hiddenset = buildhiddenset()
#print hiddenset
print scorefunction(random2,hiddenset)
print scorefunction(random1,hiddenset)
