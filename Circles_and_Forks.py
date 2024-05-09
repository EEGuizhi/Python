# EEGuizhi
class circle_fork:
    def __init__(self, size = 3) -> None:
        self.table = [[' ' for c in range(size)] for r in range(size)]
        self.history = []
        self.size = size

    def check_win(self) -> bool:
        """ Check if someone has win the game """
        for r in range(self.size):
            win = True
            for c in range(self.size - 1):
                if self.table[r][c] != self.table[r][c+1] or self.table[r][c] == ' ':
                    win = False
                    break
            if win:
                return True
        for c in range(self.size):
            win = True
            for r in range(self.size - 1):
                if self.table[r][c] != self.table[r+1][c] or self.table[r][c] == ' ':
                    win = False
                    break
            if win:
                return True
        win = True
        for i in range(self.size - 1):
            if self.table[i][i] != self.table[i+1][i+1] or self.table[i][i] == ' ':
                win = False
        if win:
            return True
        win = True
        for i in range(self.size - 1):
            if self.table[i][self.size-1-i] != self.table[i+1][self.size-2-i] or self.table[i][self.size-1-i] == ' ':
                win = False
        if win:
            return True
        return False

    def update_table(self, turn: str) -> None:
        """ Updating game table """
        self.table[self.history[-1][0]][self.history[-1][1]] = turn
        if len(self.history) == self.size * 2:
            self.table[self.history[0][0]][self.history[0][1]] = ' '
            self.history.pop(0)

    def draw_table(self, row = 2, col = 10) -> None:
        """ Drawing game table """
        move_cursor(row=row, col=0)
        end_chars = '|' * (self.size - 1) + '\n'
        for r in range(self.size):
            print(' ' * col + "       |" * (self.size - 1))
            print(' ' * col, end='')
            for c in range(self.size):
                print(f"   {self.table[r][c]}   {end_chars[c]}", end='')
            print(' ' * col + "       |" * (self.size - 1))
            if r < self.size - 1:
                print(' ' * col + "-" * (8 * self.size - 1))

def move_cursor(row: int, col: int):
    """ Move the cursor on terminal to the given position (start from 1) """
    if type(row) != int or type(col) != int: raise TypeError("The type of `row` and `col` must be integer")
    if row < 0: raise ValueError(f"`row` can not be a negative number")
    if col < 0: raise ValueError(f"`col` can not be a negative number")
    print(f"\033[{row};{col}H", end='')


if __name__ == "__main__":
    # Initial
    game = circle_fork(size=5)

    # Game loop
    turn = 'X'
    game.draw_table()
    while not game.check_win():
        # Acting player
        if turn == 'O':
            turn = 'X'
        else:
            turn = 'O'

        # Give action
        while True:
            move_cursor(row = 4*game.size + 1, col = 0)
            print(" " * 100, end='\r')
            pos = input(f">> Is \"{turn}\"'s turn ! please input the position (x, y): ")
            pos = pos.replace('(', '').replace(')', '').replace(' ', '').split(',')
            try:
                pos = [int(pos[0]) - 1, int(pos[1]) - 1]
                if game.table[pos[0]][pos[1]] == ' ' and pos[0] >= 0 and pos[0] < game.size and pos[1] >= 0 and pos[1] < game.size:
                    break
            except:
                pass

        # Update game table
        game.history.append(pos)
        game.update_table(turn)
        game.draw_table()

    print(f">> Game over ! \"{turn}\" is winner !!" + " " * 50)
