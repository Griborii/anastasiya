from regular_expression import *
from automatons import *
from regex_to_NFA import *
from NFA_to_DFA import *


def test_minimal_dfa_from_regex():
    a = TerminalNode('a')
    b = TerminalNode('b')
    aub = NonTerminalNode(a, b, RegexOperations.UNITE)
    ab = NonTerminalNode(a, b, RegexOperations.CONCAT)
    a_cl = NonTerminalNode(a, None, RegexOperations.CLOSURE)
    aub_cl = NonTerminalNode(aub, None, RegexOperations.CLOSURE)

    nfa = regex_to_NFA(aub_cl)
    print(f"\n_____________________________________________________________\n\n\nNFA for {aub_cl}")
    nfa.print()

    # примем, что НКА верный
    nfa.remove_epsilon_transition()
    print(f"\n_____________________________________________________________\n\n\nafter eps_edges remove".upper())
    nfa.print()

    nfa.remove_unreachable_nodes()
    print(f"\n_____________________________________________________________\n\n\nafter unreachable_nodes remove".upper())
    nfa.print()

test_minimal_dfa_from_regex()