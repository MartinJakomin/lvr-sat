# Testing file
import itertools

s = [[1,2,3],[4,5],[6,7]]

s2 = []
for element in itertools.product(*s):
    s2.append(element)

print s2