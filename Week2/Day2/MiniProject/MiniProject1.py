#MiniProject1.py

# Tic Tac Toe - Mini Project

def display_board(board):
    print("  0   1   2")
    for i, row in enumerate(board):
        print(i, " | ".join(row))
        if i < 2:
            print("  " + "---+---+---")

def player_input(board, player):
    while True:
        try:
            move = input(f"Player {player}, enter your move (row col): ").split()
            if len(move) != 2:
                print("Enter two numbers separated by a space: row and column.")
                continue
            row, col = map(int, move)
            if not (0 <= row < 3 and 0 <= col < 3):
                print("Invalid position. Choose row and column between 0 and 2.")
                continue
            if board[row][col] != " ":
                print("This cell is already taken. Try again.")
                continue
            return row, col
        except ValueError:
            print("Please enter valid numbers.")

def check_win(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_tie(board):
    return all(cell != " " for row in board for cell in row)

def play():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    while True:
        display_board(board)
        row, col = player_input(board, current_player)
        board[row][col] = current_player
        if check_win(board, current_player):
            display_board(board)
            print(f"🎉 Player {current_player} wins! 🎉")
            break
        if check_tie(board):
            display_board(board)
            print("It's a tie!")
            break
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    play()
