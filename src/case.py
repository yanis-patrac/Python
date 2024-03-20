class Case:
    def __init__(self, is_mine=False):
        self.is_mine = is_mine
        self.is_revealed = False
        self.is_flagged = False
        self.is_questioned = False
        self.adjacent_mines = 0