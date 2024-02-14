class Node:
    def __init__(self, size: int, ):
        self.error = False
        self.finish = -1
        self.epsilon = []
        self.trans = []
        self.size = size

    def addd(self, letter, node):
        if letter >= len(self.trans):
            steps = letter - len(self.trans) + 1
            for i in range(steps):
                self.trans.append(None)
        self.trans[letter] = node

    def is_final(self):
        return self.finish >= 0

    def make_finish(self, finish):
        self.finish = finish

    def get_epsilon(self):
        return self.epsilon























    def eps_closure_1(self, closure, node):
        closure.append(node.num)
        for child in node.epsilon:
            closure.append(child.num)
            self.eps_closure_1(closure, child)

    def eps_closure_2(self, nfa, indexes):
        closure = []
        for i in indexes:
            self.eps_closure_1(closure, nfa.get_node)
        return closure



    def put_final(self, nfa, input_set):
        closure = self.eps_closure_2(nfa, input_set)
        for num in closure:
            curr_node = nfa.get_node(num)
            if curr_node.is_finish:
                finish = curr_node.finish
                self.finish.append(self.states[-1])
        return finish


    def create_node(self, nfa, input_set):
        new_node = DfaNode(self.dict_size)
        self.nfa_map[input_set] = len(self.states)
        new_node.num = len(self.states)
        self.states.append(new_node)
        new_node.make_finish(put_final(nfa, input_set))