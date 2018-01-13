from copy import deepcopy

"""
Board:
    . : empty square
    @ : player
    # : wall
    $ : box
    % : empty goal
    + : player on goal
    * : box on goal

Solution:
    The solution is stored in the LURD format:
    - where lowercase l, u, r and d represent a move in that (left, up, right, down) direction
    - capital LURD represents a push.
"""

moves = []
possible_moves = ["left", "up", "right", "down"]

boards = []
board_start = []


def init(path):
    global boards, board_start
    data = []
    with open(path, 'r') as f:
        for lines in f.readlines():
            lines = lines.replace('\n', '')
            line = []
            for character in lines:
                if character == ' ':
                    character = '.'
                line.append(character)
            data.append(line)
    board_start = data
    boards = [[[board_start], []]]


def solution(board):
    # check if the boxes ($) are on the locations of the goals (%)
    return location(board, "$") == location(board_start, "%")


def result(current_board):
    # print(current_board)
    print("We found a solution for your problem: \n")
    print_board(current_board[0][0])
    print_moves(current_board[1])
    print("Number of moves:", len(current_board[1]))


def print_moves(sol):
    # print the solution according to the LURD-format
    print(''.join(sol))


def print_board(board):
    # print the board
    for row in board:
        print(''.join(row))


def location(board, character):
    # print the location for a given character (ea. @ for player and $ for box)
    locations = [[ix, iy] for ix, row in enumerate(board) for iy, i in enumerate(row) if i == character]
    return locations


def direction_coordinates(x, y, move_position):
    # set the following 4 variables to the correct movements
    if move_position == "up":
        a = x - 1
        c = x - 2
        b = d = y
    elif move_position == "down":
        a = x + 1
        c = x + 2
        b = d = y
    elif move_position == "left":
        a = c = x
        b = y - 1
        d = y - 2
    else:
        # move_position == "right"
        a = c = x
        b = y + 1
        d = y + 2
    return a, b, c, d


def move_player(x, y, move_position, board):
    # TODO: Specify the deadlocks
    current_board = board[0][0]
    current_moves = board[1]
    location_start = location(current_board, "@")
    old_loc = [location_start[0][0], location_start[0][1]]
    a, b, c, d = direction_coordinates(x, y, move_position)
    if current_board[a][b] == "#" or current_board[a][b] == "$" and current_board[c][d] == "#" \
            or current_board[a][b] == "$" and current_board[c][d] == "$" or current_board[a][b] == "%":
        # if one of these conditions is true, it is an invalid move, so we pass the function
        pass
    elif current_board[a][b] == "$":
        current_board[a][b] = "@"
        current_board[c][d] = "$"
        current_board[old_loc[0]][old_loc[1]] = "."
        current_moves.append(str(move_position[0].upper()))
        boards.append([[current_board], current_moves])
    else:
        current_board[a][b] = "@"
        current_board[old_loc[0]][old_loc[1]] = "."
        current_moves.append(str(move_position[0]))
        boards.append([[current_board], current_moves])


# def test(board):
#     current_board = board[0][0]
#     if current_board[a][b] == "%":
#         pass
#     else:
#         current_board[old_loc[0]][old_loc[1]] = "."

def move(direction, board):
    location_player = location(board[0][0], "@")
    x = location_player[0][0]
    y = location_player[0][1]
    move_player(x, y, direction, board)


def breadthfirst(board):
    # take a direction, deepcopy board -> move(direction = possible move, board = current_board)
    # save board in list boards [x][0], save solution in list boards [x][1] (this happens in move-function)
    # test current_board[0][0] if current_board[0][0] is the solution -> print board, the moves and number of moves
    # else, take next direction, deepcopy board ...
    for possible_move in possible_moves:
        current_board = deepcopy(board)
        move(possible_move, current_board)
        print_board(current_board[0][0])
        if solution(current_board[0][0]):
            result(current_board)
            return True


def game():
    init('boards/5x5.txt')
    while boards:
        board = boards.pop(0)
        # check if the start board is already the solution
        if solution(board[0]):
            print("The start-board is already the solution")
        elif breadthfirst(board):
            boards.clear()
            # TODO: What if no solution is found?
            # print("We couldn't find a solution for your problem :(")


game()
