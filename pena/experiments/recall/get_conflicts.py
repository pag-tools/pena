import re

'''
Generate a list of conflicts
'''

# FILENAME = 'RECALL-EXECUTION-SS.log'
FILENAME = 'RECALL-ND-PW.log'

CONFLICTS_FILENAME = 'RECALL-PW'

CONFLICTS = []

with open(FILENAME) as f:
    lines = f.read().split('\n')
    for line in lines:
        if 'Conflicting config' in line:
            regex = re.compile('\[(.*?)\]', re.IGNORECASE)
            word = regex.search(line).group().replace('[','').replace(']','')
            pair = word.split(',')
            pair[0], pair[1] = pair[0].strip(), pair[1].strip()
            pair.sort()
            if pair not in CONFLICTS:
                CONFLICTS.append(pair)

with open(CONFLICTS_FILENAME, 'w') as conflicts:
    CONFLICTS.sort()
    for conflict in CONFLICTS:
        conflicts.write("{}\n".format(conflict))

