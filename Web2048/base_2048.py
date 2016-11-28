import random, copy


class Board:
    def __init__(self, repl=None):
        self._board = [[0 for x in range(4)] for y in range(4)]
        if repl and repl.__class__ == Board:
            self._board = copy.deepcopy(repl._board)

    def remaining(self):
        return sum([sum([x == 0 for x in y]) for y in self._board])

    def valid(self):
        if self.remaining() > 0:
            return True
        for x in range(4):
            last = self._board[x][0]
            for y in range(1,4):
                current = self._board[x][y]
                if current == last:
                    return True
        for y in range(4):
            last = self._board[0][y]
            for x in range(1,4):
                current = self._board[x][y]
                if current == last:
                    return True
        return False

    def spawn(self):
        options = self.remaining()
        selection = random.randint(0,options-1)
        for y in self._board:
            for i,x in enumerate(y):
                if x == 0:
                    selection -= 1
                    if selection < 0:
                        y[i] = random.randint(1,2)
                        return


    def move(self, direction):
        if not self.valid():
            return False
        bounds = {"s": {"y": xrange(2, -1, -1), "x": xrange(0,  4,  1)},
                  "w": {"y": xrange(1,  4,  1), "x": xrange(0,  4,  1)},
                  "d": {"y": xrange(0,  4,  1), "x": xrange(2, -1, -1)},
                  "a": {"y": xrange(0,  4,  1), "x": xrange(1,  4,  1)}}
        moved = False
        if direction not in bounds:
            return moved
        for y in bounds[direction]["y"]:
            for x in bounds[direction]["x"]:
                val = self._board[y][x]
                if val > 0:
                    bounds2 = {"s": {"prop": xrange(y + 1,  4,  1)},
                               "w": {"prop": xrange(y - 1, -1, -1)},
                               "d": {"prop": xrange(x + 1,  4,  1)},
                               "a": {"prop": xrange(x - 1, -1, -1)}}
                    if direction == "s" or direction == "w":
                        y1 = y
                        for y2 in bounds2[direction]["prop"]:
                            val2 = self._board[y2][x]
                            if val2 == val:
                                val += 1
                                self._board[y1][x] = 0
                                self._board[y2][x] = val
                                moved = True
                                break
                            if val2 == 0:
                                self._board[y1][x] = 0
                                self._board[y2][x] = val
                                y1 = y2
                                moved = True
                            else:
                                break
                    else:
                        x1 = x
                        for x2 in bounds2[direction]["prop"]:
                            val2 = self._board[y][x2]
                            if val2 == val:
                                val += 1
                                self._board[y][x1] = 0
                                self._board[y][x2] = val
                                moved = True
                                break
                            if val2 == 0:
                                self._board[y][x1] = 0
                                self._board[y][x2] = val
                                x1 = x2
                                moved = True
                            else:
                                break
        return moved

    def step(self, direction):
        if self.move(direction):
            self.spawn()
        # return self.valid()

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

    def auto(self):
        p = random.random()
        if p < 0.8:
            direction = "s"
        elif p < 0.9:
            direction = "d"
        elif p < 0.99:
            direction = "a"
        else:
            direction = "w"
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
