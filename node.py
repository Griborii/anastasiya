class Node:
    def __init__(self, size: int, ):
        self.error = False
        self.fin = -1
        self.epsilon = []
        self.trans = [None for _ in range(size)]
        self.size = size
        self.num = -1

    def __str__(self):
        return f"State {self.state_id}"

    def add_let(self, letter, node):
        if letter >= len(self.trans):
            steps = letter - len(self.trans) + 1
            for i in range(steps):
                self.trans.append(None)
        self.trans[letter] = node
        
    def add_eps(self, node):
        self.epsilon.append(node)


    def is_final(self):
        return self.fin >= 0

    def make_finish(self, finish):
        self.finish = finish

    def get_epsilon(self):
        return self.epsilon
