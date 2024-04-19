import random

EMPTY = ' '
PLAYER_1 = '1'
PLAYER_2 = '2'
BOARD_SIZE = 5

# Initialize the board
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
board[0][0], board[0][BOARD_SIZE - 1], board[BOARD_SIZE - 1][0], board[BOARD_SIZE - 1][
    BOARD_SIZE - 1] = 'S', 'S', 'S', 'S'


player_1_score = 0
player_2_score = 0

def select_game_mode():
    print("Select game mode:")
    print("1. Human vs Human")
    print("2. Human vs AI")
    print("3. AI vs AI")
    choice = input("Enter your choice (1, 2 or 3): ")
    return choice


def print_scores():
    print(f"Player 1 Score: {player_1_score}")
    print(f"Player 2 Score: {player_2_score}")
    print()


def printBoardAndScores(board):
    # Print column labels
    print("   " + "   ".join(str(i) for i in range(BOARD_SIZE)))

    for i in range(BOARD_SIZE):
        print(" ━━━" * BOARD_SIZE)

        for j in range(BOARD_SIZE):
            print(f"┃ {board[i][j]} ", end='')

        print(f"┃ {i}")

    print(" ━━━" * BOARD_SIZE)
    print(f"   Player 1 Score: {player_1_score}     Player 2 Score: {player_2_score}")
    print()

def is_valid_move(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == EMPTY

def check_sos(row, col, symbol):
    if board[row][col] != symbol: #Check for SOS only if the played symbol is present
        return 0

    sos_count = 0
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    if symbol == 'O':
        for dr, dc in directions:
            before = (row - dr, col - dc)
            after = (row + dr, col + dc)
            if 0 <= before[0] < BOARD_SIZE and 0 <= before[1] < BOARD_SIZE and \
                    0 <= after[0] < BOARD_SIZE and 0 <= after[1] < BOARD_SIZE:
                if board[before[0]][before[1]] == 'S' and board[after[0]][after[1]] == 'S':
                    sos_count += 1
    elif symbol == 'S':
        for dr, dc in directions:
            mid = (row + dr, col + dc)
            end = (row + 2 * dr, col + 2 * dc)
            before_before = (row - 2 * dr, col - 2 * dc)
            before = (row - dr, col - dc)

            #Check if mid and end are within bounds for S-O-S
            if 0 <= mid[0] < BOARD_SIZE and 0 <= mid[1] < BOARD_SIZE and \
                    0 <= end[0] < BOARD_SIZE and 0 <= end[1] < BOARD_SIZE:
                if board[mid[0]][mid[1]] == 'O' and board[end[0]][end[1]] == 'S':
                    sos_count += 1

            #Check if before_before and before are within bounds for S-O-S
            if 0 <= before_before[0] < BOARD_SIZE and 0 <= before_before[1] < BOARD_SIZE and \
                    0 <= before[0] < BOARD_SIZE and 0 <= before[1] < BOARD_SIZE:
                if board[before_before[0]][before_before[1]] == 'S' and board[before[0]][before[1]] == 'O':
                    sos_count += 1

    return sos_count


#Function to get valid moves on the board
def get_valid_moves():
    return [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if is_valid_move(row, col)]

#Function to make a move on the board
def make_move(move, player_symbol, current_player):
    global player_1_score, player_2_score

    row, col = move
    board[row][col] = player_symbol

    sos_count = check_sos(row, col, player_symbol)
    if sos_count > 0:
        print(f"Player {current_player} created SOS! Player gets {sos_count} point(s).")
        if current_player == PLAYER_1:
            player_1_score += sos_count
        else:
            player_2_score += sos_count



# Function to play the game between two human players
def play_human_vs_human():
    current_player = PLAYER_1

    while True:
        printBoardAndScores(board)

        player_symbol = input(f"Player {current_player}, choose 'S' or 'O': ").upper()
        while player_symbol not in ['S', 'O']:
            print("Invalid choice. Please choose 'S' or 'O'.")
            player_symbol = input(f"Player {current_player}, choose 'S' or 'O': ").upper()

        print(f"Player {current_player}'s turn:")
        row = int(input("Enter row (0-4): "))
        col = int(input("Enter column (0-4): "))

        while not is_valid_move(row, col):
            print("Invalid move. Try again.")
            row = int(input("Enter row (0-4): "))
            col = int(input("Enter column (0-4): "))

        make_move((row, col), player_symbol, current_player)

        if len(get_valid_moves()) == 0:
            print("Game over!")
            printBoardAndScores(board)
            break

        current_player = PLAYER_2 if current_player == PLAYER_1 else PLAYER_1
def h1(board, player):
    score = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY:
                #Calculate potential SOS for 'S' move
                board[row][col] = 'S'
                score += check_sos(row, col, 'S')
                board[row][col] = EMPTY

                #Calculate potential SOS for 'O' move
                board[row][col] = 'O'
                score += check_sos(row, col, 'O')
                board[row][col] = EMPTY

                #Checking the 'OSO' pattern
                if ((col + 2 < BOARD_SIZE and board[row][col + 1] == 'S' and board[row][col + 2] == 'O') or
                        (col - 2 >= 0 and board[row][col - 1] == 'S' and board[row][col - 2] == 'O')):
                    score += 0

                #Checking the proximity to the centre of the board
                if abs(row - BOARD_SIZE // 2) <= 1 and abs(col - BOARD_SIZE // 2) <= 1:
                    score += 0

                #Preventing the possibility of the opposing player making an 'SOS'
                if (check_sos(row, col, 'S') > 0 or check_sos(row, col, 'O') > 0):
                    score += 0



    return score if player == PLAYER_2 else -score

def h2(board, player):
    score = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY:
                # 'S' hamlesi için potansiyel SOS hesapla
                board[row][col] = 'S'
                score += check_sos(row, col, 'S')
                board[row][col] = EMPTY

                # 'O' hamlesi için potansiyel SOS hesapla
                board[row][col] = 'O'
                score += check_sos(row, col, 'O')
                board[row][col] = EMPTY


    return score if player == PLAYER_2 else -score
def make_temporary_move(board, move, symbol):
    row, col = move
    board[row][col] = symbol
def undo_temporary_move(board, move):
    row, col = move
    board[row][col] = EMPTY

def minimax(board, depth, alpha, beta, maximizingPlayer, eval_function):
    if depth == 0 or len(get_valid_moves()) == 0:
        return eval_function(board, PLAYER_2 if maximizingPlayer else PLAYER_1)

    if maximizingPlayer:
        maxEval = float('-inf')
        for move in get_valid_moves():
            make_temporary_move(board, move, 'S')
            eval = minimax(board, depth - 1, alpha, beta, False, eval_function)
            undo_temporary_move(board, move)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')
        for move in get_valid_moves():
            make_temporary_move(board, move, 'O')
            eval = minimax(board, depth - 1, alpha, beta, True, eval_function)
            undo_temporary_move(board, move)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval



def play_human_vs_ai():
    current_player = PLAYER_1

    while True:
        printBoardAndScores(board)

        if current_player == PLAYER_1:  #Human player
            player_symbol = input(f"Player {current_player}, choose 'S' or 'O': ").upper()
            while player_symbol not in ['S', 'O']:
                print("Invalid choice. Please choose 'S' or 'O'.")
                player_symbol = input(f"Player {current_player}, choose 'S' or 'O': ").upper()

            row = int(input("Enter row (0-4): "))
            col = int(input("Enter column (0-4): "))

            while not is_valid_move(row, col):
                print("Invalid move. Try again.")
                row = int(input("Enter row (0-4): "))
                col = int(input("Enter column (0-4): "))

            make_move((row, col), player_symbol, current_player)



        else:  #AI player
            best_move = None
            best_value = float('-inf')

            for move in get_valid_moves():

                for symbol in ['S', 'O']:
                    make_temporary_move(board, move, symbol)

                    move_value = minimax(board, 4, float('-inf'), float('inf'), False, lambda b, p=PLAYER_2: h1(b, p))
                    undo_temporary_move(board, move)

                    if move_value > best_value:
                        best_value = move_value
                        best_move = move
                        ai_symbol = symbol

            print(f"AI (Player 2) chooses {ai_symbol} at ({best_move[0]}, {best_move[1]})")
            make_move(best_move, ai_symbol, PLAYER_2)

        if len(get_valid_moves()) == 0:
            print("Game over!")
            printBoardAndScores(board)
            break

        current_player = PLAYER_2 if current_player == PLAYER_1 else PLAYER_1

        print_scores()

def play_ai_vs_ai():
    #current_player = PLAYER_1

    ai1_first_move = random.choice(get_valid_moves())
    ai1_symbol = random.choice(['S', 'O'])
    make_move(ai1_first_move, ai1_symbol, PLAYER_1)
    print(f"AI 1 (Player 1) chooses {ai1_symbol} at ({ai1_first_move[0]}, {ai1_first_move[1]})")
    current_player = PLAYER_2

    while True:
        printBoardAndScores(board)

        if current_player == PLAYER_1:
            best_move = None
            best_value = float('-inf')

            for move in get_valid_moves():
                for symbol in ['S', 'O']:
                    make_temporary_move(board, move, symbol)
                    move_value = minimax(board, 4, float('-inf'), float('inf'), False, lambda b, p=PLAYER_1: h1(b, p))
                    undo_temporary_move(board, move)

                    if move_value > best_value:
                        best_value = move_value
                        best_move = move
                        ai_symbol = symbol

            print(f"AI 1 (Player 1) chooses {ai_symbol} at ({best_move[0]}, {best_move[1]})")
            make_move(best_move, ai_symbol, PLAYER_1)

        else:
            best_move = None
            best_value = float('-inf')

            for move in get_valid_moves():
                for symbol in ['S', 'O']:
                    make_temporary_move(board, move, symbol)
                    move_value = minimax(board, 4, float('-inf'), float('inf'), False, lambda b, p=PLAYER_2: h2(b, p))
                    undo_temporary_move(board, move)

                    if move_value > best_value:
                        best_value = move_value
                        best_move = move
                        ai_symbol = symbol

            print(f"AI 2 (Player 2) chooses {ai_symbol} at ({best_move[0]}, {best_move[1]})")
            make_move(best_move, ai_symbol, PLAYER_2)

        if len(get_valid_moves()) == 0:
            print("Game over!")
            printBoardAndScores(board)
            break

        current_player = PLAYER_2 if current_player == PLAYER_1 else PLAYER_1

        print_scores()
def main():
    choice = select_game_mode()
    if choice == '1':
        play_human_vs_human()
    elif choice == '2':
        play_human_vs_ai()
    elif choice == '3':
        play_ai_vs_ai()
    else:
        print("Invalid choice. Please enter 1, 2 or 3.")

if __name__ == "__main__":
    main()