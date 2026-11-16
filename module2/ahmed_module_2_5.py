
board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def show_board():
    print()
    print(board[0], "|", board[1], "|", board[2])
    print("--+---+--")
    print(board[3], "|", board[4], "|", board[5])
    print("--+---+--")
    print(board[6], "|", board[7], "|", board[8])
    print()


def check_winner(player):
    wins = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for a, b, c in wins:
        if board[a] == board[b] == board[c] == player:
            return True

    return False


player = "X"

for turn in range(9):
    show_board()

    while True:
        choice = input("Player " + player + ", choose 1-9: ")

        if choice not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            print("Choose a number from 1 to 9")
            continue

        position = int(choice) - 1

        if board[position] == "X" or board[position] == "O":
            print("This place is already taken!")
            continue

        board[position] = player
        break

    if check_winner(player):
        show_board()
        print("Player", player, "wins!")
        break

    if player == "X":
        player = "O"
    else:
        player = "X"

else:
    show_board()
    print("It's a draw!")
