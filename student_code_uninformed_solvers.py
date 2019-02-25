from solver import *
from queue import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True
        else:
            moves = self.gm.getMovables()
            if moves:
                for mo in moves:
                    depth = self.currentState.depth
                    self.gm.makeMove(mo)
                    nextState = GameState(self.gm.getGameState(), depth + 1, mo)
                    nextState.parent = self.currentState
                    self.gm.reverseMove(mo)
                    if nextState not in self.visited:
                        self.currentState.children.append(nextState)

            while True:
                if self.currentState.state == self.victoryCondition:
                    return True
                nextS = self.currentState.nextChildToVisit

                if nextS < len(self.currentState.children):
                    self.currentState.nextChildToVisit = self.currentState.nextChildToVisit + 1
                    self.gm.makeMove(self.currentState.children[nextS].requiredMovable)
                    self.currentState = self.currentState.children[nextS]
                    self.visited[self.currentState] = True
                    return self.currentState.state == self.victoryCondition
                else:
                    self.currentState = self.currentState.parent

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    q = Queue()
    moveCount = 0

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        visit = self.visited
        moveSet = self.gm.getMovables()

        if self.currentState.state == self.victoryCondition:

            if self.q != self.q.empty():
                while not self.q.empty():
                    self.q.get()
            return True

        if moveSet:
            for i in moveSet:
                self.gm.makeMove(i)
                child = GameState(self.gm.getGameState(), 0, i)
                self.currentState.children.append(child)
                child.parent = self.currentState
                self.gm.reverseMove(i)

        for x in self.currentState.children:
            if x not in visit:
                self.q.put(x)

        while not self.q.empty():

            child = self.q.get()

            if child not in visit:
                visit[child] = True
                curr = self.currentState
                b = []

                while curr.requiredMovable:
                    b.append(curr.requiredMovable)
                    curr = curr.parent
                curr = child
                br = []

                while curr.requiredMovable:
                    br.append(curr.requiredMovable)
                    curr = curr.parent
                br = reversed(br)

                for y in b:
                    self.gm.reverseMove(y)

                for z in br:
                    self.gm.makeMove(z)

                self.currentState.depth = self.moveCount
                self.moveCount += 1
                self.currentState = child
                break

        return False