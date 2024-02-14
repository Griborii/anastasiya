class NKA:
    def __init__(self, start, finish_list, sz):
        self.start = start
        self.finish = finish_list
        self.all = []
        self.size = sz

    def print(self):
        # print("finish_list:")
        # for fin in self.finish_list:
        #     print(fin)

        for i in range(len(self.all)):
            now = self.all[i]
            print("node:", i)
            for j in range(self.size):
                if now.trans[j] is not None:
                    print("(", j, "->", now.trans[j].num, ")")
            for j in range(len(now.epsilon)):
                print("(", "E", "->", now.epsilon[j].num, ")")

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
