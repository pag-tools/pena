import re

'''
Generate a file with conflicts and their unexpected values
'''

FILENAME = 'PRECISION-EXECUTION-FINAL.log'

UNEXPECTED_FILENAME = 'UNEXPECTED-FINAL'

with open(FILENAME) as f:
    lines = f.read().split('\n')
    with open(UNEXPECTED_FILENAME, 'w') as unexpected:
        for line in lines:
            if 'Conflicting config' in line:
                regex = re.compile('\[(.*?)\]', re.IGNORECASE)
                word = regex.search(line).group().replace('[','').replace(']','')
                pair = word.split(',')
                p1,p2 = pair[0].strip(), pair[1].strip()
                unexpected.write("\n['{}','{}']\n".format(p1, p2))
            elif 'Unexpected' in line:
                unexpected.write('{}\n'.format(line))
            else:
                continue


