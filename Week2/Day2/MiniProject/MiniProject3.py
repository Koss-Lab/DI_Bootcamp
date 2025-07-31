#MiniProject3.py

def display_board(board):
    print("\nTIC TAC TOE")
    print("*************")
    print(f"* {board[0]} | {board[1]} | {board[2]} *")
    print("*---|---|---*")
    print(f"* {board[3]} | {board[4]} | {board[5]} *")
    print("*---|---|---*")
    print(f"* {board[6]} | {board[7]} | {board[8]} *")
    print("*************\n")


def player_input(player, board):
    while True:
        try:
            row = int(input(f"Player {player}'s turn...\nEnter row: ")) - 1
            column = int(input(f"Enter column: ")) - 1
            if 0 <= row <= 2 and 0 <= column <= 2:
                if board[row * 3 + column] == ' ':
                    board[row * 3 + column] = player
                    break
                else:
                    print("This position is already taken. Try again.")
            else:
                print("Invalid input. Please enter values between 1 and 3 for both row and column.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


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
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    return None


def play():
    board = [' '] * 9
    current_player = 'X'
    winner = None
    turn_count = 0

    while turn_count < 9 and winner is None:
        display_board(board)
        player_input(current_player, board)
        winner = check_win(board)
        if winner:
            display_board(board)
            print(f"Player {winner} wins!")
            break
        current_player = 'O' if current_player == 'X' else 'X'
        turn_count += 1

    if winner is None:
        display_board(board)
        print("It's a tie!")


play()
