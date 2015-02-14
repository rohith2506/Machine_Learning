import math
import random
import time

people = [('Seymour','BOS'),
('Franny','DAL'),
('Zooey','CAK'),
('Walt','MIA'),
('Buddy','ORD'),
('Les','OMA')]

destination='LGA'
def getminutes(t):
	x = time.strptime(t,'%H:%M')
	return x[3] * 60 + x[4]

flights = {}
for line in file('schedule.txt'):
	orig,dest,depart,arrrival,price = line.strip().split(',')
	flights.setdefault((orig,dest),[])
	flights[(orig,dest)].append((depart,arrrival,int(price)))

def printschedule(r):
	for d in range(len(r)/2):
		name = people[d][0]
		origin = people[d][1]
		In = flights[(origin,destination)][r[d]]
		Out = flights[(destination,origin)][r[d+1]]
		print '%10s %10s %5s-%5s $%3s %5s-%5s $%3s' % (name,origin,In[0],In[1],In[2],Out[0],Out[1],Out[2])

def schedulecost(sol):
	totalprice = 0
	latestarrival = 0
	earliestdep = 24*60
	for d in range(len(sol)/2):
		origin = people[d][1]
		outbound = flights[(origin,destination)][int(sol[d])]
		returnf  = flights[(destination,origin)][int(sol[d+1])]
		totalprice = totalprice + outbound[2]
		totalprice = totalprice + returnf[2]
		if latestarrival < getminutes(outbound[1]): latestarrival = getminutes(outbound[1])
		if earliestdep > getminutes(returnf[0]): earliestdep = getminutes(returnf[0])
	totalwait = 0
	for d in range(len(sol)/2):
		outbound = flights[(origin,destination)][int(sol[d])]
		returnf  = flights[(destination,origin)][int(sol[d+1])]
		totalwait = totalwait + latestarrival - getminutes(outbound[1])
		totalwait = totalwait + getminutes(returnf[0]) - earliestdep
	if latestarrival > earliestdep : totalprice = totalprice + 50
	return totalprice + totalwait

def randomoptimize(domain,costf):
	best = 99999999
	bestr = None
	for i in range(10000):
		r = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
		cost = costf(r)
		if cost < best:
			best = cost
			bestr = r
	print bestr,best,r
	return r

def hillclimb(domain,costf):
	sol = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
	while True:
		neighbours = []
		for j in range(len(domain)):
			if sol[j] > domain[j][0]:
				neighbours.append(sol[0:j] + [sol[j] + 1] + sol[j+1:])
			if sol[j] < domain[j][1]:
				neighbours.append(sol[0:j] + [sol[j] - 1] + sol[j+1:])
		current = costf(sol)
		best = current
		for j in range(len(neighbours)):
			cost = costf(neighbours[j])
			if cost < best:
				best = cost
				sol = neighbours[j]
		if best == current:
			break
	return sol

def simulatedannealing(domain,costf,T = 10000.0, cool = 0.95, step = 1):
	vec = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
	while  T > 0.1:
		i = random.randint(0,len(domain)-1)
		Dir = random.randint(-step,step)
		vecb = vec[:]
		vecb[i] = vecb[i] + Dir
		if vecb[i] < domain[i][0]: vecb[i] = domain[i][0]
		if vecb[i] > domain[i][1]: vecb[i] = domain[i][1]
		ea = costf(vec)
		eb = costf(vecb)
		p = pow(math.e,(-ea-eb)/T)
		if (eb < ea or random.random() < p):
			vec = vecb
		T = T * cool
	return vec

def geneticoptimize(domain,costf,popsize=50,step=1,mutprob=0.2,elite=0.2,maxiter=100):
	#Mutation operation
	def mutate(vec):
		i = random.randint(0,len(domain)-1)
		if random.random() < 0.5 and vec[i] > domain[i][0]:
			return vec[0:i] + [vec[i] - step] + vec[i+1:]
		elif vec[i] < domain[i][1]:
			return vec[0:i] + [vec[i] + step] + vec[i+1:]
	#CrossOver operation
	def crossover(r1,r2):
		i = random.randint(1,len(domain) - 2)
		return r1[0:i] + r2[i:]
	pop = []
	for i in range(0,popsize):
		vec = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
		pop.append(vec)
	topelite = int(elite * popsize)
	best  = 9999999
	bests = []
	for i in range(maxiter):
		scores = [(costf(v),v) for v in pop]
		scores.sort()
		print len(scores)
		ranked = [v for (s,v) in scores]
		pop = ranked[0:topelite]
		while len(pop) < popsize:
			if random.random() < mutprob:
				c = random.randint(0,topelite)
				pop.append(mutate(ranked[c]))
			else:
				c1 = random.randint(0,topelite)
				c2 = random.randint(0,topelite)
				pop.append(crossover(ranked[c1],ranked[c2]))
		print scores[0][0]
		if scores[0][0]  < best:
			best = scores[0][0]
			bests = scores[0][1]
	return bests

print flights
s=[1,4,3,2,7,3,6,3,2,4,5,3]
printschedule(s)
print "Normal cost %d" %(schedulecost(s))
domain = [(0,8)] * (len(people) * 2)
smod = randomoptimize(domain,schedulecost)
print "Random Searching %d" %(schedulecost(smod))
printschedule(smod)
print "\n"
smod = hillclimb(domain,schedulecost)
print "Hill Climbing %d" %(schedulecost(smod))
printschedule(smod)
print "\n"
smod = simulatedannealing(domain,schedulecost)
print "simulated Annealing %d" %(schedulecost(smod))
printschedule(smod)
smod = geneticoptimize(domain,schedulecost)
print "genetic optimtization %d" %(schedulecost(smod))
printschedule(smod)
