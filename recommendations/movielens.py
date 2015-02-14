'''
Item Based Collaberative Filtering
@Author: Rohit
'''

import math
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0},
'Rohit': {'Snakes on a Plane': 2.67,'Just My Luck': 1.234}
}


# Euclidean distance similarity score
def sim_euclidean(prefs,person1,person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0:
        return 0
    else:
        sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                            for items in prefs[person1] if item in prefs[person2]])
        return 1/(1+sum_of_squares)


# pearson correlation score
def sim_pearson(prefs,p1,p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    
    n = len(si)

    if n == 0: return 0

    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    sum1sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2sq = sum([pow(prefs[p2][it],2) for it in si])

    psum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    numerator = psum - ((sum1*sum2)/n)
    denominator = math.sqrt((sum1sq - pow(sum1,2)/n) * (sum2sq - pow(sum2,2)/n))
    if denominator == 0: return 0
    else: return numerator/denominator
        

# This Will find the best critic for given person
def TopMatches(prefs,person,n=5,similarity=sim_pearson):
    scores = [(similarity(prefs,person,other),other) for other in prefs if other!=person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

# This will Find the Best Product Required for you
def GetRecommendations(prefs,person,n=5,similarity=sim_pearson):
    totals =  {}
    simsums = {}

    for other in prefs:
        if other == person: continue
        else:
            sim = similarity(prefs,person,other)
            if sim<=0 : continue
            for item in prefs[other]:
                if item not in prefs[person] or prefs[person][item] == 0:
                    totals.setdefault(item,0)
                    totals[item]+=prefs[other][item] * sim
                    simsums.setdefault(item,0)
                    simsums[item]+=sim
    
    rankings = [(total/simsums[item],item) for item,total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

# This Will give Recommendations for given Product
def TransformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            result[item][person] = prefs[person][item]
    return result


#Calculating similar items for given items
def CalculateSimilarItems(prefs,n=10):
    result = {}
    itemprefs = TransformPrefs(prefs)
    c = 0
    for item in itemprefs:
        c = c+1
        if c%100 == 0: print "%d %d"  %(c,len(itemprefs))
        scores = TopMatches(itemprefs,item,n=n,similarity=sim_pearson)
        result[item] = scores
    return result

def GetRecommendedItems(prefs,itemmatch,user):
    userratings = prefs[user]
    scores = {}
    totalscores = {}
    for (item,rating) in userratings.items():
        for (similarity,item2) in itemmatch[item]:
            if item2 in userratings: continue
            scores.setdefault(item2,0)
            scores[item2] = scores[item2] + (similarity*rating)
            totalscores.setdefault(item2,0)
            totalscores[item2] = totalscores[item2] + similarity
    rankings = [(score/(1+totalscores[item]),item) for item,score in scores.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

def LoadMovies(path="/home/infinity/Algo/Machine_Learning/recommendations/ml-100k"):
    movies = {}
    for line in open(path+"/u.item"):
        (Id,title) = line.split('|')[0:2]
        movies[Id] = title

    prefs = {}
    for line in open(path+"/u.data"):
        (user,movieid,rating,ts) = line.split("\t")
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]] = float(rating)
    return prefs

prefs = LoadMovies()
print "These are Recommended Movies for User:(User Based)"
print GetRecommendations(prefs,'87')[0:30]
print "\n"
print "\n"
print "These are Recommended Movies for User:(Item Based)"
itemsim = CalculateSimilarItems(prefs)
print GetRecommendedItems(prefs,itemsim,'87')[0:30]
