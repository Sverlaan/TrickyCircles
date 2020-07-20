from create_level import Level


class Solver:

    def __init__(self, level):
        """
        Initializes a Solver-object for solving Levels.

        :param level: Level-object that needs to be solved
        """
        # Using strings instead of lists to represent order of circles
        self.level_seq = "".join(str(x) for x in level.circles)
        self.answer = "".join(str(x) for x in level.answer)

        self.seen = set()   # Keeps track of already explored Level-states
        self.queue = []
        
    def solve(self):
        """
        Solves the Level in the current state.

        :return: minimum number of moves required;
                 sequence of actions that lead to a solution
        """
        self.seen.clear()
        self.queue.clear()

        sequence = self.level_seq
        # Create Node with sequence-name and empty action-seq
        root = Node(sequence, "")
        root.d = 0

        res = self.breadth_first_search(root)
        n_moves = res.d
        moves = res.actions

        return n_moves, moves

    def breadth_first_search(self, root):
        """
        Executes the Breadth-First-Search algorithm to find a solution.

        :param root: starting Node, representing current Level that gets solved
        :return: first Node corresponding to solution
        """
        if root.name == self.answer:
            return root

        self.queue.append(root)
        self.seen.add(root.name)

        while len(self.queue) > 0:  # Terminates when queue is empty
            u = self.queue.pop(0)

            # Explores the three sub-states
            children = u.perform_actions()
            for seq, move in children:
                if seq not in self.seen:    # Only proceed when unexplored seq
                    v = Node(seq, u.actions + move)  # Create child-Node
                    v.d = u.d + 1

                    if seq == self.answer:  # Terminate when correct order is found
                        return v

                    self.queue.append(v)
                    self.seen.add(v.name)

        return None


class Node:

    def __init__(self, seq, actions):
        """
        Initializes a Node-object, representing a Level-state.

        :param seq: string representing order of circles
        :param actions: string representing actions executed to get to this state
        """
        self.name = seq
        self.actions = actions
        self.d = -1     # Distance in the implicit graph

    def perform_actions(self):
        """
        Executes all three possible actions needed to generate
        the next states in a way to explore all possibilities.

        :return: 3 tuples containing the new order-sequence and corresponding action
        """
        name_list = [char for char in self.name]

        a = Level(name_list)
        a.click_a()
        seq_a = "".join(str(x) for x in a.circles)

        b = Level(name_list)
        b.click_b()
        seq_b = "".join(str(x) for x in b.circles)

        x = Level(name_list)
        x.click_x()
        seq_x = "".join(str(x) for x in x.circles)

        return (seq_a, 'a'), (seq_b, 'b'), (seq_x, 'x')
