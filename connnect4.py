class Connect4:
    W = 7
    H = 6

    def __init__(self):
        self.init_board()
        self.full_board = (1 << (self.W * self.H)) - 1
        self.xy11 = self.xy2bit(1, 1)
        self.l_mask = self.full_board
        tmp = self.xy11
        while tmp:
            self.l_mask ^= tmp
            tmp >>= self.W
        self.l_mask &= self.full_board
        self.r_mask = self.full_board
        tmp = self.xy11 >> (self.W - 1)
        while tmp:
            self.r_mask ^= tmp
            tmp >>= self.W
        self.r_mask &= self.full_board

    def xy2bit(self, y, x):
        return (1 << (self.W - x)) << (self.W * (self.H - y))

    def print_board(self):
        tmp = self.xy11
        print(" 1  2  3  4  5  6  7 ")
        for y in range(self.H):
            for x in range(self.W):
                if tmp & self.black:
                    print("[o]", end="")
                elif tmp & self.white:
                    print("[x]", end="")
                else:
                    print("[ ]", end="")
                tmp >>= 1
            print()

    def debug_print_board(self, b):
        tmp = self.xy11
        print(" 1  2  3  4  5  6  7 ")
        for y in range(self.H):
            for x in range(self.W):
                if tmp & b:
                    print("[o]", end="")
                else:
                    print("[ ]", end="")
                tmp >>= 1
            print()

    def init_board(self):
        self.black = 0
        self.white = 0

    def put_xy(self, pos):
        result = pos
        b = self.black | self.white
        while (not (result >> self.W) & b) and (result >> self.W):
            result >>= self.W
        return result

    def put(self, pos, turn):
        if turn:
            self.black |= pos
        else:
            self.white |= pos

    def can_put(self, x):
        return not ((self.black | self.white) & (self.xy11 >> (x-1)))

    def putable_place(self):
        return (self.black | self.white) >> (self.W * (self.H - 1))

    def is_full(self):
        return not (self.full_board ^ (self.black | self.white))

    def horizon(self, pos, board):
        """ー"""
        result = 1
        p = pos
        b = board & self.r_mask
        while p:
            p = (p << 1) & b
            result <<= 1
        p = pos
        b = board & self.l_mask
        while p:
            p = (p >> 1) & b
            result <<= 1
        result >>= 1
        return result >> 4

    def vertical(self, pos, board):
        """｜"""
        result = 1
        p = pos
        while p:
            p = (p << self.W) & board
            result <<= 1
        p = pos
        while p:
            p = (p >> self.W) & board
            result <<= 1
        result >>= 1
        return result >> 4

    def right_down(self, pos, board):
        """＼"""
        result = 1
        p = pos
        b = board & self.r_mask
        s1 = self.W + 1
        while p:
            p = (p << s1) & b
            result <<= 1
        p = pos
        b = board & self.l_mask
        while p:
            p = (p >> s1) & b
            result <<= 1
        result >>= 1
        return result >> 4

    def right_up(self, pos, board):
        """／"""
        result = 1
        p = pos
        b = board & self.l_mask
        s1 = self.W - 1
        while p:
            p = (p << s1) & b
            result <<= 1
        p = pos
        b = board & self.r_mask
        while p:
            p = (p >> s1) & b
            result <<= 1
        result >>= 1
        return result >> 4

    def judge(self, pos, turn):
        b = self.black if turn else self.white
        print(self.horizon(pos, b), self.vertical(pos, b),
              self.right_down(pos, b), self.right_up(pos, b))
        return self.horizon(pos, b) or self.vertical(pos, b) or self.right_down(pos, b) or self.right_up(pos, b)

    def main_loop(self):
        turn = True
        while not self.is_full():
            self.print_board()
            pos = self.put_xy(self.xy11 >> (int(input()) - 1))
            self.put(pos, turn)
            if self.judge(pos, turn):
                break
            turn = not turn
        self.print_board()


c4 = Connect4()
c4.main_loop()
