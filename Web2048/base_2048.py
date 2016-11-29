import random, copy, multiprocessing


def simulate(paramqueue, resultqueue):
    try:
        while 1:
            startboard, direction, history = paramqueue.get()
            moved, board = Board._move(direction, startboard)
            if moved:
                Board._spawn(board)
                history.append(None)
            else:
                history.append(direction)
            if len(history) >= 4:
                if None in history:
                    reward = 0
                else:
                    reward = Board.reward(board)
                resultqueue.put((reward,history))
            else:
                for dir in ["w", "a", "s", "d"]:
                    paramqueue.put((board, dir, history))
    except KeyboardInterrupt:
        pass


class Board:
    def __init__(self, repl=None):
        self._board = [[0 for x in range(4)] for y in range(4)]
        self.moved = False
        self.last_moves = []
        self.paramqueue = multiprocessing.Queue()
        self.resultqueue = multiprocessing.Queue()
        self.ps = [multiprocessing.Process(target=simulate, args=(self.paramqueue,self.resultqueue,)) for i in range(20)]
        for p in self.ps:
            p.start()
        if repl and repl.__class__ == Board:
            self._board = self.boardcopy(repl._board)

    @staticmethod
    def _remaining(board):
        return sum([sum([x == 0 for x in y]) for y in board])

    def remaining(self):
        return self._remaining(self._board)

    def valid(self):
        if self.remaining() > 0:
            return True
        for x in range(4):
            last = self._board[x][0]
            for y in range(1,4):
                current = self._board[x][y]
                if current == last:
                    return True
                last = current
        for y in range(4):
            last = self._board[0][y]
            for x in range(1,4):
                current = self._board[x][y]
                if current == last:
                    return True
                last = current
        return False

    @staticmethod
    def _spawn(board):
        options = Board._remaining(board)
        selection = random.randint(0,options-1)
        for y in board:
            for i,x in enumerate(y):
                if x == 0:
                    selection -= 1
                    if selection < 0:
                        y[i] = random.randint(1,2)
                        return

    def spawn(self):
        return self._spawn(self._board)

    @staticmethod
    def _move(direction, board):
        bounds = {"s": {"y": xrange(2, -1, -1), "x": xrange(0,  4,  1)},
                  "w": {"y": xrange(1,  4,  1), "x": xrange(0,  4,  1)},
                  "d": {"y": xrange(0,  4,  1), "x": xrange(2, -1, -1)},
                  "a": {"y": xrange(0,  4,  1), "x": xrange(1,  4,  1)}}
        if direction not in bounds:
            return False, board
        moved = False
        for y in bounds[direction]["y"]:
            for x in bounds[direction]["x"]:
                val = board[y][x]
                if val > 0:
                    bounds2 = {"s": {"prop": xrange(y + 1,  4,  1)},
                               "w": {"prop": xrange(y - 1, -1, -1)},
                               "d": {"prop": xrange(x + 1,  4,  1)},
                               "a": {"prop": xrange(x - 1, -1, -1)}}
                    if direction == "s" or direction == "w":
                        y1 = y
                        for y2 in bounds2[direction]["prop"]:
                            val2 = board[y2][x]
                            if val2 == val:
                                val += 1
                                board[y1][x] = 0
                                board[y2][x] = val
                                moved = True
                                break
                            if val2 == 0:
                                board[y1][x] = 0
                                board[y2][x] = val
                                y1 = y2
                                moved = True
                            else:
                                break
                    else:
                        x1 = x
                        for x2 in bounds2[direction]["prop"]:
                            val2 = board[y][x2]
                            if val2 == val:
                                val += 1
                                board[y][x1] = 0
                                board[y][x2] = val
                                moved = True
                                break
                            if val2 == 0:
                                board[y][x1] = 0
                                board[y][x2] = val
                                x1 = x2
                                moved = True
                            else:
                                break
        return moved, board

    def move(self, direction):
        if not self.valid():
            return False
        return self._move(direction, self._board)[0]

    @staticmethod
    def boardcopy(board):
        return [copy.deepcopy(i) for i in board]

    def step(self, direction):
        if self.move(direction):
            self.spawn()

    def display(self):
        for y in self._board:
            for x in y:
                print chr(x+ord('a')) + " ",
            print

    def display_full(self):
        maxdigits = len(str(2**max([max(l) for l in self._board])))
        for y in self._board:
            for x in y:
                if x == 0:
                    val = "0"
                else:
                    val = str(2**x)
                print val + (maxdigits - len(val)) * " ",
            print

    @staticmethod
    def reward(board):
        total = 0
        for column in board:
            for p in column:
                total += 2**p
        return total



    def auto(self):
        for dir in ["w","a","s","d"]:
            self.paramqueue.put((self._board,dir,[]))

        best = 0
        besthistory = None
        for i in range(256):
            r, history = self.resultqueue.get()
            # print "Got reward #%s with reward %s" % (i, r)
            if r >= best:
                best = r
                besthistory = history
        direction = besthistory[0]

        if not self.moved and len(self.last_moves) == 2 and self.last_moves[0] == self.last_moves[1]:
            direction = random.choice(["w","a","s","d"])

        self.last_moves.append(direction)
        if len(self.last_moves) > 2:
            self.last_moves.pop(0)
        print direction
        self.step(direction)


if __name__ == "__main__":
    b = Board()
    last = True
    while b.remaining():
        if last:
            b.spawn()
        b.display_full()
        direction = raw_input()
        last = b.move(direction)
