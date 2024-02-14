from regular_expression import *
class AbstractStateNode:
    abstract_state_count = 0
    def __init__(self):
        # self.state_id = id(self) % (10 ** 3)
        self.state_id = AbstractStateNode.abstract_state_count
        AbstractStateNode.abstract_state_count += 1
        self.destination_list = dict()
        self.destination_list["EPS"] = []
        self.is_final = False
        self.parent_list = dict()
        self.parent_list["EPS"] = []

    def __str__(self):
        return f"State {self.state_id}"

    def mark_final(self, flag: bool):
        self.is_final = flag

    def get_destination(self, letter: str):
        return self.destination_list[letter]

    def get_parent(self, letter: str):
        return self.parent_list[letter]

class NfaNode(AbstractStateNode):
    def __init__(self):
        super().__init__()

    def accept(self, visitor: Visitor):
        return visitor.visit(self)

class AbstractFA:
    def __init__(self, alphabet = None):
        if alphabet is not None:
            self.alphabet = alphabet
        else:
            self.alphabet = []
        self.start = NfaNode()
        self.states = []


class NFA(AbstractFA):
    def __init__(self):
        super().__init__()
        self.start = NfaNode()
        self.finish = NfaNode()
        self.finish.mark_final(flag=True)
        self.states.append(self.start)
        self.states.append(self.finish)

        self.edges_list = dict()
        self.edges_list["EPS"] = []

    def add_nodes(self, state_list: list): #TODO: добавлять рёбра вершины
        for state in state_list:
            if state not in self.states:
                self.states.append(state)
            # добавим рёбра от новой вершины
            # for letter in state.parent_list.keys():
            #     for parent in state.parent_list[letter]:
            #         self.add_edge(parent, state, letter)
            #
            # for letter in state.destination_list.keys():
            #     for dst in state.destination_list[letter]:
            #         self.add_edge(state, dst, letter)

    def add_edge(self, src: NfaNode, dst: NfaNode, letter: str):
        print(f"\nadd edge {src}--{letter}--{dst}")
        # добавим ноды
        if src not in self.states:
            self.add_nodes([src])
        if dst not in self.states:
            self.add_nodes([dst])

        # заполним семейное древо
        print(letter, self.alphabet)
        if letter not in self.alphabet:
            self.alphabet.append(letter)
            print(self.alphabet)
        if letter not in src.destination_list.keys():
            src.destination_list[letter] = []
        if letter not in dst.parent_list.keys():
            dst.parent_list[letter] = []
        # mb twice?
        if src not in dst.parent_list[letter]:
            dst.parent_list[letter].append(src)
        if dst not in src.destination_list[letter]:
            src.destination_list[letter].append(dst)

        # добавим переход
        if letter not in self.edges_list.keys():
            self.edges_list[letter] = []
        self.edges_list[letter].append([src, dst])

        print(f"Now alphabet {self.alphabet}; \t edges letters {self.edges_list.keys()}")
        self.print_edges()



    # def remove_edge(self, src: NfaNode, dst: NfaNode, letter: str):
    #     self.edges_list[letter].remove([src, dst])
    #     src.destination_list[letter].remove(dst)
    #     dst.parent_list[letter].remove(src)
    #
    # def remove_nodes(self, state_list: list):
    #     for state in state_list:
    #         for letter in state.parent_list.keys():
    #             for parent in state.parent_list[letter]:
    #                 self.remove_edge(parent, state, letter)
    #         for letter in state.destination_list.keys():
    #             for dst in state.destination_list[letter]:
    #                 self.remove_edge(state, dst, letter)
    #
    #         self.states.remove(state)

    def print(self):
        self.print_nodes()
        print(f"_____\n")
        self.print_edges()

    def print_nodes(self):
        print(f"{len(self.states)} states:")
        for state in self.states:
            mark = " -- FINAL" if state.is_final else " -- START" if state == self.start else ""
            print("\x1B[4m" + f"{state}" + "\x1B[0m" + mark)
            print(f"\t Parents = ")
            for letter in state.parent_list.keys():
                print(f"\t\t{letter}: ", end="")
                for parent in state.parent_list[letter]:
                    print(parent, end=" ")
                print()

            print(f"\t Children = ")
            for letter in state.destination_list.keys():
                print(f"\t\t{letter}: ", end=" ")
                for parent in state.destination_list[letter]:
                    print(parent, end=" ")
                print()

    def print_edges(self):
        print(f"EDGES: ")
        for letter in self.edges_list.keys():
            for src, dst in self.edges_list[letter]:
                print(f"\t {src}\t --{letter}--> \t{dst}")

    def process_state_epsilon_paths(self, state):
                

    def process_epsilon_paths(self):
        for state in self.states:
            self.process_state_epsilon_paths(state)
    def process_epsilon_letter_transition(self):
            pass
    def process_epsilon_transition(self):
        self.process_epsilon_paths()
        self.process_epsilon_letter_transition()
        self.process_epsilon_terminal_transition()
        self.remove_epsilon_trasitions()



    # def remove_epsilon_transition(self):
    #     while len(self.get_eps_transitions()) > 0:
    #         eps_transitions = self.get_eps_transitions()
    #
    #         for src, dst in eps_transitions:
    #             self.remove_edge(src, dst, "EPS")
    #
    #             if src == self.start:
    #                 # стягиваем к старту
    #                 for letter in dst.destination_list.keys():
    #                     for child in dst.destination_list[letter]:
    #                         self.add_edge(src, child, letter)
    #
    #             else:
    #                 # добавим все переходы в src к вершине dst (стягиваем граф к финишу)
    #                 for letter in src.parent_list.keys():
    #                     for parent in src.parent_list[letter]:
    #                         self.add_edge(parent, dst, letter)
    #
    #
    # def get_eps_transitions(self):
    #     eps_edges = []
    #     for src, dst in self.edges_list["EPS"]:
    #         eps_edges.append([src, dst])
    #
    #     return eps_edges
    #
    # def remove_unreachable_nodes(self):
    #     for state in self.states:
    #         if len(state.parent_list) == 0 and state != self.start:
    #             self.remove_nodes([state])
    def process_epsilon_letter_transition(self):
        pass


class DfaNode(AbstractStateNode):
    def __init__(self, old_nodes = None):
        super().__init__()
        if old_nodes is not None:
            for node in old_nodes:
                if node.is_final:
                    self.mark_final(flag=True)

    def accept(self, visitor: Visitor):
        return self.is_final


class DFA(AbstractFA):
    def __init__(self):
        super().__init__()
        self.start = DfaNode()
        self.trash = DfaNode()
        self.states.append(self.start)
        self.states.append(self.trash)

    def add_nodes(self, fa_list: list):
        for fa in fa_list:
            for state in fa.states:
                self.states.append(state)

    def add_edge(self, source: DfaNode, destination: DfaNode, letter: str):
        if letter not in self.alphabet:
            self.alphabet.append(letter)
        if source not in self.states:
            self.states.append(source)
        if destination not in self.states:
            self.states.append(source)
        if letter not in source.destination_list.keys():
            source.destination_list[letter] = []

        source.destination_list[letter] = destination

    def remove_unreachable_nodes(self):
        queue = [self.start]
        visited = [self.start]
        while len(queue) > 0:
            curr_state = queue.pop(0)
            for letter, neighbours in curr_state.destination_list.items():
                for state in neighbours:
                    if state not in visited:
                        queue.append(state)
                        visited.append(state)

        for state in self.states:
            if state not in visited:
                self.states.remove(state)

    def full_DFA(self):
        for state in self.states:
            for letter in self.alphabet:
                if letter not in state.destination_list.keys():
                    self.add_edge(state, self.trash, letter)

        for letter in self.alphabet:
            self.add_edge(self.trash, self.trash, letter)


    def built_min_dfa(self, states_list):
        new_state = DfaNode()
        self.states.append(new_state)
        if self.start in states_list:
            self.start = new_state

        for old_state in self.states:
            for key, value in old_state.destination_list.items():
                if value in states_list:
                    old_state.destination_list[key] = new_state

        for curr_state in states_list:
            for key, value in curr_state.destination_list.items():
                if value in states_list:
                    new_state.destination_list[key] = new_state
                else:
                    new_state.destination_list[key] = value

            if curr_state.is_final:
                new_state.mark_final(flag=True)
            if curr_state in self.states:
                self.states.remove(curr_state)


    def mimimize(self):
        equals = dict()
        for s1 in self.states:
            for s2 in self.states:
                if s1.destination_list == s2.destination_list \
                        and s1.is_final == s2.is_final \
                        and s1 != s2:

                    if id(s1) in equals.keys():
                        equals[id(s1)].add(s2)
                    elif id(s2) in equals.keys():
                        equals[id(s2)].add(s1)
                    else:
                        equals[id(s1)] = {s1, s2}
        # equal states done

        for key, states in equals.items():
            self.built_min_dfa(states)

    def print(self):
        print(f"{len(self.states)} states", end="")
        for state in self.states:
            print(f"\n\n{state}", end=" ")
            if state == self.start:
                print(" --- START", end="")
            elif state == self.trash:
                print(" --- TRASH", end="")

            print("\nTRANSITIONS:")
            for letter, dst in state.destination_list.items():
                print(f"\n{letter}", end=": ")
                for item in dst:
                    print(item, end=" ")