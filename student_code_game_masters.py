from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        t1 = self.kb.kb_ask(parse_input("fact: (on ?X peg1)"))
        t1List = list()

        if not t1:
            pass
        else:
            for i in t1:
                app = str(i)
                t1List.append(int(app[-1]))

        t1List.sort()
        p1 = tuple(t1List)

        t2 = self.kb.kb_ask(parse_input("fact: (on ?X peg2)"))
        t2List = list()

        if not t2:
            pass
        else:
            for i in t2:
                app1 = str(i)
                t2List.append(int(app1[-1]))

        t2List.sort()
        p2 = tuple(t2List)

        t3 = self.kb.kb_ask(parse_input("fact: (on ?X peg3)"))
        t3List = list()

        if not t3:
            pass
        else:
            for i in t3:
                app2 = str(i)
                t3List.append(int(app2[-1]))

        t3List.sort()
        p3 = tuple(t3List)
        return (p1, p2, p3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        terms = movable_statement.terms
        moveDisk = terms[0].__str__()
        oldPeg = terms[1].__str__()
        newPeg = terms[2].__str__()

        # Retract old 'on' fact
        fact1 = Fact(Statement(['on', moveDisk, oldPeg]))
        self.kb.kb_retract(fact1)

        # Assert new 'on' fact
        fact2 = Fact(Statement(['on', moveDisk, newPeg]))

        # Find the disk under the moveDisk
        answer = self.kb.kb_ask(Fact(Statement(['onTopOf', moveDisk, '?X'])))
        if answer:  # If a disk is found under moveDisk
            diskUnder = answer[0].bindings_dict['?X']
            fact3 = Fact(Statement(['onTopOf', moveDisk, diskUnder]))
            self.kb.kb_retract(fact3)
            fact7 = Fact(Statement(['top', diskUnder, oldPeg]))
            self.kb.kb_assert(fact7)
        else:  # If there is no disk under the moveDisk
            fact3 = Fact(Statement(['empty', oldPeg]))
            self.kb.kb_assert(fact3)

        # If the new peg was empty, retract that fact
        check = self.kb.kb_ask(Fact(Statement(['empty', newPeg])))
        if check:
            fact4 = Fact(Statement(['empty', newPeg]))
            self.kb.kb_retract(fact4)
        else:
            answer = self.kb.kb_ask(Fact(Statement(['top', '?X', newPeg])))
            diskOnNewPeg = answer[0].bindings_dict['?X']
            fact10 = Fact(Statement(['onTopOf', moveDisk, diskOnNewPeg]))
            fact11 = Fact(Statement(['top', diskOnNewPeg, newPeg]))
            self.kb.kb_assert(fact10)
            self.kb.kb_retract(fact11)

        # Retract old fact of moveDisk being on the oldPeg and assert new fact of moveDisk on newPeg
        fact5 = Fact(Statement(['top', moveDisk, oldPeg]))
        self.kb.kb_retract(fact5)
        fact6 = Fact(Statement(['top', moveDisk, newPeg]))

        self.kb.kb_assert(fact2)
        self.kb.kb_assert(fact6)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        original = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        for counter in range(1, 9):
            answer = self.kb.kb_ask(Fact(Statement(["coord", "tile" + str(counter), "?X", "?Y"])))

            original[int(answer[0].bindings_dict['?Y'])][int(answer[0].bindings_dict['?X'])] = counter

        answer = self.kb.kb_ask(Fact(Statement(["coord", "empty", "?X", "?Y"])))
        original[int(answer[0].bindings_dict['?Y'])][int(answer[0].bindings_dict['?X'])] = -1

        finalTuple = tuple((tuple(original[0]), tuple(original[1]), tuple(original[2])))

        return finalTuple

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        # Essentially were swapping positions of the tile in the movable statement with the empty tile
        terms = movable_statement.terms
        fact1 = Fact(Statement(["coord", terms[0], terms[1], terms[2]]))
        fact2 = Fact(Statement(["coord", "empty", terms[3], terms[4]]))
        fact3 = Fact(Statement(["coord", terms[0], terms[3], terms[4]]))
        fact4 = Fact(Statement(["coord", "empty", terms[1], terms[2]]))

        self.kb.kb_retract(fact1)
        self.kb.kb_retract(fact2)
        self.kb.kb_assert(fact3)
        self.kb.kb_assert(fact4)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
