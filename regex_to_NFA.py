from regular_expression import *
# from automatons import *
from node import *
from NKA import *
from DKA import *

# nfa operations
def concat(fa_list: list):
    nfa = NFA()
    a, b = fa_list
    nfa.add_edge(nfa.start, a.start, "EPS")
    nfa.add_edge(a.finish, b.start, "EPS")
    nfa.add_edge(b.finish, nfa.finish, "EPS")
    a.finish.mark_final(flag=False)
    b.finish.mark_final(flag=False)

    nfa.add_nodes(a.states)
    nfa.add_nodes(b.states)

    return nfa

def closure(old_fa):
    nfa = NFA()
    nfa.add_edge(nfa.start, nfa.finish, "EPS")
    nfa.add_edge(nfa.start, old_fa.start, "EPS")
    nfa.add_edge(old_fa.finish, nfa.finish, "EPS")
    nfa.add_edge(old_fa.finish, old_fa.start, "EPS")
    old_fa.finish.mark_final(flag=False)

    nfa.add_nodes(old_fa.states)
    return nfa

def unite(fa_list: list):
    nfa = NFA()
    for a in fa_list:
        nfa.add_nodes(a.states)
        nfa.add_edge(nfa.start, a.start, "EPS")
        nfa.add_edge(a.finish, nfa.finish, "EPS")
        a.finish.mark_final(flag=False)

    return nfa


def handle_operations(regex: NonTerminalNode):
    fa_list = automatons_from_regexps([regex.left_exp, regex.right_exp])

    if regex.operation == RegexOperations.CLOSURE:
        return closure(fa_list[0])

    elif regex.operation == RegexOperations.UNITE:
        return unite(fa_list)

    elif regex.operation == RegexOperations.CONCAT:
        return concat(fa_list)


def automatons_from_regexps(regexp_list: list[AbstractRegexNode]):
    fa_list = []
    for reg in regexp_list:
        if reg is not None:
            nfa = regex_to_NFA(reg)
            fa_list.append(nfa)

    return fa_list


def regex_to_NFA(root, size):
    if isinstance(root, TerminalNode):
        right = Node(size)
        left = Node(size)
        left.add_let(int(root.letter), right)
        return (left, right)
    if root.operation == RegexOperations.UNITE:
        ans_l = regex_to_NFA(root.left, size)
        ans_r = regex_to_NFA(root.right, size)
        left = Node(size)
        right = Node(size)
        left.add_eps(ans_l[0])
        left.add_eps(ans_r[0])
        ans_l[1].add_eps(right)
        ans_r[1].add_eps(right)
        return (left, right)
    if root.operation == RegexOperations.CLOSURE:
        left = Node(size)
        right = Node(size)
        s = regex_to_NFA(root.left, size)
        left.add_eps(s[0])
        s[1].add_eps(s[0])
        s[1].add_eps(right)
        left.add_eps(right)
        return (left, right)
    if root.operation == RegexOperations.CONCAT:
        ans_l = regex_to_NFA(root.left, size)
        ans_r = regex_to_NFA(root.right, size)
        ans_l[1].add_eps(ans_r[0])
        return (left, right)
        # l.second->Add(r.first);
        # return {l.first, r.second};


def count(st0):
    dict2 = {}
    spec_s = {'+', '*', '.', '(', ')'}
    st = list(st0) 
    for i in range(len(st)):
        elem = st[i]
        if elem not in spec_s and elem not in dict2:
            dict2[elem] = len(dict2)
        if elem not in spec_s:
            st[i] = str(dict2[elem])
    ans = ""
    for elem in st:
        ans += elem
    return (dict2, ans)

