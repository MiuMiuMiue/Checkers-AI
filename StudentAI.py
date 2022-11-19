from random import randint
from BoardClasses import Move
from BoardClasses import Board
import copy
import math
import time

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

# class StudentAI():
#     """Just to try if this works."""
#     def __init__(self,col,row,p):
#         self.col = col
#         self.row = row
#         self.p = p
#         self.board = Board(col,row,p)
#         self.board.initialize_game()
#         self.color = ''
#         self.opponent = {1:2,2:1}
#         self.color = 2
#         self.colorDict = {1: "B", 2: "W"}
#
#     def get_move(self, move):
#         if len(move) != 0:
#             self.board.make_move(move, self.opponent[self.color])
#         else:
#             self.color = 1
#         move, score = self.maxValue(self.color, 4)
#         self.board.make_move(move, self.color)
#         return move
#
#
#     def maxValue(self, curColor, depth) -> (Move, int):
#         if depth == 0 or self.isFinished():
#             return None, self.evaluation()
#         else:
#             bestScore = float('-inf')
#             bestMove = None
#             moveList = self.board.get_all_possible_moves(curColor)
#             for piece in moveList:
#                 for move in piece:
#                     self.board.make_move(move, curColor)
#                     newMove, score = self.minValue(self.opponent[curColor], depth - 1)
#                     if score > bestScore:
#                         bestMove = move
#                         bestScore = score
#                     self.board.undo()
#
#             return bestMove, bestScore
#
#     def minValue(self, curColor, depth) -> (Move, int):
#         if depth == 0 or self.isFinished():
#             return None, self.evaluation()
#         else:
#             bestScore = float('inf')
#             bestMove = None
#             moveList = self.board.get_all_possible_moves(curColor)
#             for piece in moveList:
#                 for move in piece:
#                     self.board.make_move(move, curColor)
#                     newMove, score = self.maxValue(self.opponent[curColor], depth - 1)
#                     if score < bestScore:
#                         bestMove = move
#                         bestScore = score
#                     self.board.undo()
#
#             return bestMove, bestScore
#
#     def evaluation(self):
#         whiteScore = 0
#         blackScore = 0
#         if self.isFinished():
#             c = None
#             for i in range(self.row):
#                 for j in range(self.col):
#                     checker = self.board.board[i][j]
#                     if checker.color != '.':
#                         c = checker.color
#                         if c == "W":
#                             whiteScore += 10
#                         elif c == "B":
#                             blackScore += 10
#             if self.color == 1 and c == "B":
#                 return blackScore
#             elif self.color == 1 and c == "W":
#                 return -1 * whiteScore
#             elif self.color == 2 and c == "W":
#                 return whiteScore
#             elif self.color == 2 and c == "B":
#                 return -1 * blackScore
#         else:
#             kingWeight = 1.2
#             result = 0
#             blackKing = 0
#             blackNormal = 0
#             whiteKing = 0
#             whiteNormal = 0
#
#             for i in range(self.row):
#                 for j in range(self.col):
#                     checker = self.board.board[i][j]
#                     if checker.color == "W":
#                         if checker.is_king == False:
#                             whiteNormal += 1
#                         elif checker.is_king == True:
#                             whiteKing += 1
#                     elif checker.color == "B":
#                         if checker.is_king == False:
#                             blackNormal += 1
#                         elif checker.is_king == True:
#                             blackKing += 1
#             if self.color == 1:
#                 result = blackKing * kingWeight + blackNormal - whiteKing * kingWeight - whiteNormal
#             elif self.color == 2:
#                 result = whiteKing * kingWeight + whiteNormal - blackKing * kingWeight - blackNormal
#
#             return result
#
#     def isFinished(self):
#         if self.board.white_count == 0 or self.board.black_count == 0:
#             return True
#
#         return False

class StudentAI():
    """Just to try if this works."""
    class Node:
        def __init__(self, board, move, color, parent, c):
            self.board = board
            self.move = move
            self.childs = []
            self.pSimulation = 0
            self.simulation = 0
            self.wins = 0
            self.color = color
            self.parent = parent
            self.c = c

        def getUCT(self):
            if self.simulation == 0:
                return float("inf")
            return self.wins / self.simulation + self.c * math.sqrt(math.log(self.pSimulation) / self.simulation)

        def getMaxChild(self):
            return max(self.childs, key=lambda x: x.getUCT())

        def isLeafNode(self):
            return self.childs == []

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        self.colorDict = {1: "B", 2: "W"}

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        self.root = self.Node(self.board, None, self.color, None, 0.5)
        self.expand(self.root)
        t_end = time.time() + 2
        while time.time() < t_end:
            node = self.root

            while not node.isLeafNode():
                node = node.getMaxChild()

            if node.simulation == 0:
                result = self.runSimulation(node)
                self.backPropogate(node, result)
            elif node.simulation == 1:
                self.expand(node)
                if node.childs == []:
                    result = self.runSimulation(node)
                    self.backPropogate(node, result)
                else:
                    node = node.getMaxChild()
                    result = self.runSimulation(node)
                    self.backPropogate(node, result)
            self.unifySimulationNum()

        move = self.root.getMaxChild().move
        self.board.make_move(move, self.color)

        queue = [self.root, "1"]
        count = 0
        while queue:
            node = queue[0]
            queue = queue[1:]
            if node == "1":
                print("=======================================================================================")
                if queue:
                    queue.append("1")
            else:
                print("Wins:", node.wins, "Simulation:", node.simulation, "Parent Simulation", node.pSimulation)
                print("Color: ", node.color)
                if count > 0:
                    print("UCT Values:", node.getUCT())
                for child in node.childs:
                    queue.append(child)
            count += 1

        return move

    def expand(self, node):
        for piece in node.board.get_all_possible_moves(node.color):
            for move in piece:
                tempNode = self.Node(copy.deepcopy(node.board), move, self.opponent[node.color], node, 0.5)
                tempNode.board.make_move(move, node.color)
                node.childs.append(tempNode)

    def backPropogate(self, curNode, result):
        node = curNode
        while node.parent:
            if node.parent.color == result:
                node.simulation += 1
                node.wins += 1
            else:
                node.simulation += 1
            node = node.parent

    def unifySimulationNum(self):
        total = 0
        for child in self.root.childs:
            total += child.simulation
        self.root.simulation = total

        queue = [self.root]
        while queue:
            node = queue[0]
            queue = queue[1:]
            if node.parent == None:
                for child in node.childs:
                    queue.append(child)
            else:
                node.pSimulation = node.parent.simulation
                for child in node.childs:
                    queue.append(child)

    def runSimulation(self, node):
        board = copy.deepcopy(node.board)
        curColor = node.color
        while self.isFinished(board) == False:
            moves = board.get_all_possible_moves(curColor)
            if moves == []:
                if board.black_count > board.white_count:
                    return 1
                else:
                    return 2
            index = randint(0, len(moves) - 1)
            inner_index = randint(0, len(moves[index]) - 1)
            move = moves[index][inner_index]
            board.make_move(move, curColor)
            curColor = self.opponent[curColor]
        if board.white_count == 0:
            return 1
        else:
            return 2

    def isFinished(self, board):
        if board.white_count == 0 or board.black_count == 0:
            return True

        return False


if __name__ == "__main__":
    from Checker import Checker

    # board = Board(8, 8, 3)
    # s = StudentAI(8, 8, 3)
    # board.show_board()
    # board.board[4][3] = Checker("W", [4, 3])
    # board.board[5][2] = Checker("W", [5, 2])
    # board.board[5][4] = Checker("W", [5, 4])
    # board.board[5][0] = Checker("W", [5, 0])
    # board.board[6][1] = Checker("W", [6, 1])
    # board.board[7][0] = Checker("W", [7, 0])
    # board.board[7][2] = Checker("W", [7, 2])
    # board.board[6][7] = Checker("W", [6, 7])
    # board.board[3][4] = Checker("B", [3, 4])
    # board.board[2][7] = Checker("B", [2, 7])
    # s.board = board
    # s.board.show_board()
    # board.show_board()
    # print(s.get_move([]))


    # board = Board(8, 8, 3)
    # board.initialize_game()
    # board.show_board()
    # s = StudentAI(8, 8, 3)
    # print(s.get_move([]))
