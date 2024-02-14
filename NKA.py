class NKA:
    def __init__(self, start, finish_list, sz):
        self.start = start
        self.finish = finish_list
        self.all = []
        self.size = sz

    def DFS(self):
        self.DFS_(self.start)

    def get_node(self, ind):
        return self.all[ind]

    def DFS_(self, now):
        now.num = len(self.all)
        self.all.append(now)
        for i in range(self.size):
            if now.trans[i] is not None and now.trans[i].num == -1:
                self.DFS_(now.trans[i])

        for i in range(len(now.epsilon)):
            if now.epsilon[i] is not None and now.epsilon[i].num == -1:
                self.DFS_(now.epsilon[i])
