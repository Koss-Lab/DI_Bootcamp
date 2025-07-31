#MiniProject3.py

def display_board(board):
    print("---------")
    for i in range(3):
        print(f"| {board[i * 3]} | {board[i * 3 + 1]} | {board[i * 3 + 2]} |")
        print("---------")


def player_input(player, board):
    while True:
        try:
            position = int(input(f"Player {player}, choose a position (1-9): ")) - 1
            if position < 0 or position >= 9:
                print("Invalid position. Please choose a number between 1 and 9.")
            elif board[position] != ' ':
                print("This position is already taken. Try again.")
            else:
                board[position] = player
                break
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")


def check_win(board):
    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != ' ':
            return board[combo[0]]
    return None


def play():
    board = [' '] * 9
    current_player = 'X'
    turns = 0

    while turns < 9:
        display_board(board)
        player_input(current_player, board)

        winner = check_win(board)
        if winner:
            display_board(board)
            print(f"Player {winner} wins!")
            break

        current_player = 'O' if current_player == 'X' else 'X'
        turns += 1

    if winner is None:
        display_board(board)
        print("It's a tie!")


play()

