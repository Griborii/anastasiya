from node import *

def hash_set(st):
    return hash(tuple(st))

class DKA:
    def __init__(self, nfa, dict1):
        self.nfa = nfa
        self.size = len(dict1)
        self.nfa_map = {}
        self.states = []
        self.finish_list = []
        self.dct = dict1
        self.build_DFA(nfa)


    def print(self):
        print("dict: ", self.dct)
        
        for i in range(len(self.states)):
            now = self.states[i]
            print("node:", i)
            for j in range(self.size):
                if now.trans[j] is not None:
                    print("(", j, "->", now.trans[j].num, ")")

        print("finish_list:")
        for fin in self.finish_list:
            print(fin)

    def eps_closure_1(self, closure, node):
        closure.add(node.num)
        for child in node.epsilon:
            if child.num not in closure:
                closure.add(child.num)
                self.eps_closure_1(closure, child)
            closure.add(child.num)
            self.eps_closure_1(closure, child)

    def eps_closure_2(self, nfa, indexes):
        closure = set()
        for index in indexes:
            self.eps_closure_1(closure, nfa.get_node(index))
        return closure

    def put_final(self, nfa, set_from):
        finish = -1
        closure = self.eps_closure_2(nfa, set_from)
        for num in closure:
            curr_node = nfa.get_node(num)
            if curr_node.is_final():
                finish = curr_node.fin
                self.finish_list.append(len(self.states) - 1)
        return finish

    def create_node(self, nfa, set_from):
        new_node = Node(self.size)
        self.nfa_map[hash(tuple(set_from))] = len(self.states)
        new_node.num = len(self.states)
        self.states.append(new_node)
        new_node.make_finish(self.put_final(nfa, set_from))
        closure = self.eps_closure_2(nfa, set_from)
        if len(set_from):
            new_node.err = True
            self.trash = new_node

    def get_node(self, set_from):
        node_ind = self.nfa_map[hash_set(set_from)]
        return self.states[node_ind]

    def create_trans(self, set_from, set_to, let):
        from_node = self.get_node(set_from)
        to_node = self.get_node(set_to)
        from_node.add_let(let, to_node)

    def set_not_processed(self, set_from):
        return hash_set(set_from) not in self.nfa_map

    def build_DFA(self, nfa):
        queue = []
        first_set = set()
        first_set.add(nfa.start.num)
        self.create_node(nfa, first_set)
        self.start = self.states[0]
        queue.append(first_set)
        while len(queue) > 0:
            curr_set = queue.pop(0)
            closure = self.eps_closure_2(nfa, curr_set)
            for letter in range(self.size):
                next_set = set()
                for ind in closure:
                    curr_node = nfa.get_node(ind)
                    to_node = curr_node.trans[letter]
                    if to_node is not None:
                        next_set.add(to_node.num)
                if self.set_not_processed(next_set):
                    self.create_node(nfa, next_set)
                    queue.append(next_set)
                self.create_trans(curr_set, next_set, letter)