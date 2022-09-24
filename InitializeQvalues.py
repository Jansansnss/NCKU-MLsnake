import itertools
import json
import random

#sqs = [''.join(s) for s in list(itertools.product(*[['0','1','2','3']] * 12))]
sq = []
for a in ('0','1'):
    for b in ('0','1'):
        for c in ('0','1'):
            sq.append(['2',a,b,c])
            sq.append([a,'2',b,c])
            sq.append([a,b,'2',c])
            sq.append([a,b,c,'2'])
sq = [''.join(s) for s in list(sq)]
sqs = [''.join(s) for s in list(itertools.product(sq,sq,sq))]
#sqs = [''.join(s) for s in list(sq)]
widths = ['0','1','NA']
heights = ['2','3','NA']

states = {}
for x in widths:
	for y in heights:
		for z in sqs:
			rand1 = random.uniform(0,1)
			rand2 = random.uniform(0,1)
			rand3 = random.uniform(0,1)
			rand4 = random.uniform(0,1)
			states[str((x,y,z))] = [rand1,rand2,rand3,rand4]
			#states[str((x,y,z))] = [0,0,0,0,0,0,0,0,0,0,0,0]

with open("c:/Users/jansa/MLGame/games/snake/ml/myqvaluesf2.json", "w") as f:
	json.dump(states, f)