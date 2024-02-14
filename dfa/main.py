from regex_to_NFA import *


str0 = input()
dict2, str0 = count(str0)
root = Build(str0)
ans = regex_to_NFA(root, 2)
ans[1].fin = 0
nka = NKA(ans[0], ans[1], 2)
nka.DFS()
dka = DKA(nka, dict2)
dka.print()