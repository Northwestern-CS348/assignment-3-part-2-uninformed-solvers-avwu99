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
        self.kb.kb_assert(fact2)

        # Find the disk under the moveDisk
        answer = self.kb.kb_ask(Fact(Statement(["onTopOf", moveDisk, '?X'])))
        if answer:  # If a disk is found under moveDisk
            diskUnder = answer[0].bindings_dict['?X']
            fact3 = Fact(Statement(['onTopOf', moveDisk, diskUnder]))
            self.kb.kb_retract(fact3)
            fact7 = Fact(Statement(['top', diskUnder, oldPeg]))
        else: # If there is no disk under the moveDisk
            fact3 = Fact(Statement(['empty', oldPeg]))
            self.kb.kb_assert(fact3)

        # If the new peg was empty, retract that fact
        check = parse_input("fact: (empty %s)" %newPeg)
        if check:
            fact4 = Fact(Statement(['empty', newPeg]))
            self.kb.kb_retract(fact4)

        # Retract old fact of moveDisk being on the oldPeg and assert new fact of moveDisk on newPeg
        fact5 = Fact(Statement(['top', moveDisk, oldPeg]))
        self.kb.kb_retract(fact5)
        fact6 = Fact(Statement(['top', moveDisk, newPeg]))
        self.kb.kb_assert(fact6)

        # Retract old onTop fact of disk currently on the newPeg and assert new fact of moveDisk onTop of newPeg
        answer = self.kb.kb_ask(Fact(Statement(['onTopOf', '?X', newPeg])))
        if answer:  # If there is currently a disk on top of the newPeg
            diskReplace = answer[0].bindings_dict['?X']
            fact8 = Fact(Statement(['onTop', diskReplace, newPeg]))
            self.kb.kb_retract(fact8)
            fact9 = Fact(Statement(['onTopOf', moveDisk, diskReplace]))
            self.kb.kb_assert(fact9)

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
        tile_dict = {"tile1": 1, "tile2": 2, "tile3": 3, "tile4": 4, "tile5": 5, "tile6": 6, "tile7": 7, "tile8": 8,
                     "empty": -1}
        x_dict = {"pos1": 0, "pos2": 1, "pos3": 2}

        row1 = self.kb.kb_ask(Fact(Statement(["coordinate", '?tile', '?X', "pos1"])))
        rowList1= [0,0,0]
        for i in row1:
            val = i.bindings_dict['?tile']
            x = i.bindings_dict['?X']
            translateTile = tile_dict[val]  # tile value
            translateX = x_dict[x]
            rowList1[translateX] = translateTile

        t1 = tuple(rowList1)

        row2 = self.kb.kb_ask(Fact(Statement(["coordinate", '?tile', '?X', "pos2"])))
        rowList2 = [0,0,0]
        for j in row2:
            val = j.bindings_dict['?tile']
            x = j.bindings_dict['?X']
            translateTile = tile_dict[val]
            translateX = x_dict[x]
            rowList2[translateX] = translateTile

        t2 = tuple(rowList2)

        row3 = self.kb.kb_ask(Fact(Statement(["coordinate", '?tile', '?X', "pos3"])))
        rowList3 = [0,0,0]
        for k in row3:
            val = k.bindings_dict['?tile']
            x = k.bindings_dict['?X']
            translateTile = tile_dict[val]
            translateX = x_dict[x]
            rowList3[translateX] = translateTile

        t3 = tuple(rowList3)

        print(row3)
        print(t1, t2, t3)
        return (t1, t2, t3)


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
        tile = terms[0].__str__()
        oldX = terms[1].__str__()
        oldY = terms[2].__str__()
        newX = terms[3].__str__()
        newY = terms[4].__str__()

        # Retract old coordinates of the moving tile
        fact1 = Fact(Statement(['coordinate', tile, oldX, oldY]))

        # Assert new coordinates of the moving tile
        fact2 = Fact(Statement(['coordinate', tile, newX, newY]))

        # Do the same with the empty tile
        fact3 = Fact(Statement(['coordinate', 'empty', newX, newY]))

        fact4 = Fact(Statement(['coordinate', 'empty', oldX, oldY]))

        self.kb.kb_retract(fact1)
        self.kb.kb_retract(fact3)
        self.kb.kb_assert(fact2)
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
