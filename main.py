import pygame
import pickle
from time import sleep
from clientSocket import ClientSocket

connection = ClientSocket()
click_coord = None

# def init that contains all the initialization of the gui of the chess
pygame.init()
width = 1000
height = 900
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('CHESS1')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 0)
timer = pygame.time.Clock()
fps = 60

pieces_list = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
               'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']

white_pieces = pieces_list.copy()
black_pieces = pieces_list.copy()

opponent_pieces_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                             (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

player_pieces_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                           (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_pieces_white = []
captured_pieces_black = []
valid_moves = []

while connection.player_role == -1:
    sleep(1)

if connection.player_role == "0":
    white_locations, black_locations = player_pieces_locations, opponent_pieces_locations
else:
    black_locations, white_locations = player_pieces_locations, opponent_pieces_locations

turn_step = 0
selection = 100

black_rook = pygame.image.load('sprites/b.rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))

black_knight = pygame.image.load('sprites/b.knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))

black_bishop = pygame.image.load('sprites/b.bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))

black_king = pygame.image.load('sprites/shhh.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))

black_queen = pygame.image.load('sprites/b.queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))

black_pawn = pygame.image.load('sprites/b.pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))

white_rook = pygame.image.load('sprites/w.rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))

white_knight = pygame.image.load('sprites/w.knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))

white_bishop = pygame.image.load('sprites/w.bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))

white_king = pygame.image.load('sprites/w.king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))

white_queen = pygame.image.load('sprites/w.queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))

white_pawn = pygame.image.load('sprites/w.pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]

black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

counter = 0
winner = ''
game_over = False


def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 800, width, 100])
        pygame.draw.rect(screen, 'blue', [0, 800, width, 100], 5)
        pygame.draw.rect(screen, 'blue', [800, 0, 200, height], 5)
        status_text = ['White: Choose a piece to play', 'White: Choose his destination',
                       'Black: Choose a piece to play', 'Black: Choose his destination']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        screen.blit(medium_font.render('GIVE UP', True, 'black'), (810, 830))


def draw_opponent_pieces(pieces, locations, pawn_image, pieces_images):
    for i in range(len(pieces)):
        index = piece_list.index(pieces[i])
        if pieces[i] == 'pawn':
            screen.blit(pawn_image, (locations[i][0] * 100 + 22, locations[i][1] * 100 + 30))
        else:
            screen.blit(pieces_images[index], (locations[i][0] * 100 + 10, locations[i][1] * 100 + 10))
        # if turn_step < 2:
        #     if selection == i:
        #         pygame.draw.rect(screen, 'red',
        #                          (locations[i][0] * 100 - 1, locations[i][1] * 100 - 1, 100, 100), 2)


def draw_player_pieces(pieces, locations, pawn_image, pieces_images):
    for i in range(len(pieces)):
        index = piece_list.index(pieces[i])
        if pieces[i] == 'pawn':
            screen.blit(pawn_image, (locations[i][0] * 100 + 22, locations[i][1] * 100 + 30))
        else:
            screen.blit(pieces_images[index], (locations[i][0] * 100 + 10, locations[i][1] * 100 + 10))

        if selection == i:
                pygame.draw.rect(screen, 'blue', (locations[i][0] * 100 + 1, locations[i][1] * 100 + 1,
                                                  100, 100), 2)


def draw_pieces():
    # draws the pieces based on role
    if connection.player_role == "0":
        draw_player_pieces(white_pieces, white_locations, white_pawn, white_images)
        draw_opponent_pieces(black_pieces, black_locations, black_pawn, black_images)
    else:
        draw_player_pieces(black_pieces, black_locations, black_pawn, black_images)
        draw_opponent_pieces(white_pieces, white_locations, white_pawn, white_images)


def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):

        piece_location = locations[i]  # This line is causing the error
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(piece_location, turn)
        elif piece == 'rook':
            moves_list = check_rook(piece_location, turn)
        elif piece == 'knight':
            moves_list = check_knight(piece_location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(piece_location, turn)
        elif piece == 'queen':
            moves_list = check_queen(piece_location, turn)
        elif piece == 'king':
            moves_list = check_king(piece_location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list


def check_king(position, color):
    moves_list = []
    if color == 'white':

        friends_list = white_locations
    else:
        friends_list = black_locations

    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)

    return moves_list


def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations
    for i in range(4):
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= (position[0] + (chain * x)) <= 7 and 0 <= (position[1] + (chain * y)) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations
    for i in range(4):
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= (position[0] + (chain * x)) <= 7 and 0 <= (position[1] + (chain * y)) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


def check_pawn(position, color):
    moves_list = []
    if connection.player_role == "0":
        print('I AM WHITE ')
        if color == 'black':
            if (position[0], position[1] + 1) not in white_locations and \
                    (position[0], position[1] + 1) not in black_locations and position[1] < 7:
                moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in white_locations and \
                    (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
            if (position[0] + 1, position[1] + 1) in black_locations:
                moves_list.append((position[0] + 1, position[1] + 1))
            if (position[0] - 1, position[1] + 1) in black_locations:
                moves_list.append((position[0] - 1, position[1] + 1))

        if color == 'white':
            if (position[0], position[1] - 1) not in white_locations and \
                    (position[0], position[1] - 1) not in black_locations and position[1] > 0:
                moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
            if (position[0] + 1, position[1] - 1) in white_locations:
                moves_list.append((position[0] + 1, position[1] - 1))
            if (position[0] - 1, position[1] - 1) in white_locations:
                moves_list.append((position[0] - 1, position[1] - 1))
    else:

        print('I AM black ')

        if color == 'white':
            if (position[0], position[1] + 1) not in white_locations and \
                    (position[0], position[1] + 1) not in black_locations and position[1] < 7:
                moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in white_locations and \
                    (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
            if (position[0] + 1, position[1] + 1) in black_locations:
                moves_list.append((position[0] + 1, position[1] + 1))
            if (position[0] - 1, position[1] + 1) in black_locations:
                moves_list.append((position[0] - 1, position[1] + 1))

        if color == 'black':
            if (position[0], position[1] - 1) not in white_locations and \
                    (position[0], position[1] - 1) not in black_locations and position[1] > 0:
                moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
            if (position[0] + 1, position[1] - 1) in white_locations:
                moves_list.append((position[0] + 1, position[1] - 1))
            if (position[0] - 1, position[1] - 1) in white_locations:
                moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


def check_knight(position, color):
    moves_list = []
    if color == 'white':
        friends_list = white_locations
    else:
        friends_list = black_locations

    # Define the target list outside the loop
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]

    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    # אופציה ב
    # for target in targets:
    #     new_position = (position[0] + target[0], position[1] + target[1])
    #     # Check if the new position is within the bounds of the chessboard
    #     if 0 <= new_position[0] <= 7 and 0 <= new_position[1] <= 7:
    #         # Check if the new position is not occupied by a friend
    #         if new_position not in friends_list:
    #             moves_list.append(new_position)

    return moves_list


def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)


def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))

    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))


def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                              white_locations[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                               black_locations[king_index][1] * 100 + 1, 100, 100], 5)


def draw_game_over():
    pygame.draw.rect(screen, 'black', (200, 200, 400, 70))
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f' press ENTER to restart!', True, 'white'), (210, 240))


# gets a move and returns the mirror of it
def mirrorMove(move):
    new_move = []
    for coord in move:
        new_move.append(mirrorCoord(coord))

    return new_move


# gets coord and returns a mirror of it, for example for (0, 0) will return (7, 7), (1, 0) -> (6, 7)
# (3, 3) -> (4, 4), (4, 3) -> (3, 4), (1, 2) -> (6, 5)
def mirrorCoord(coord):
    new_coord = (coord[0], 7 - coord[1])
    return new_coord


# t = threading.Thread(target=receiver, daemon=True)
# t.start()

black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')

# the game engine
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()

    # selection 100 is default - means nothing is happening - nothing is clicked yet?
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    socketstep = []

    # got new move from server
    if connection.new_move[0] == 1:
        if connection.player_role != "0":
            # gets the new move from server, needs to render to board accordingly to new move and change its status
            # back to -1
            move = connection.new_move[1]
            print('got new move:%s' % move)
            moves = move.split("), (")
            move_from, move_to = moves[0], moves[1]

            move_from_coord = (int(move_from.split(", ")[0].split("(")[1]), int(move_from.split(", ")[1]))
            selection = white_locations.index(move_from_coord)
            if turn_step == 0:
                turn_step = 1

            move_to_coord = (int(move_to.split(", ")[0]), int(move_to.split(", ")[1].split(")")[0]))
            # change whites coordinates
            white_locations[selection] = move_to_coord
            print("white move to", move_to_coord)
            socketstep.append(move_to_coord)

            # remove eaten black piece
            if move_to_coord in black_locations:
                black_piece = black_locations.index(move_to_coord)
                captured_pieces_white.append(black_pieces[black_piece])
                if black_pieces[black_piece] == 'king':
                    winner = 'white'
                black_pieces.pop(black_piece)
                black_locations.pop(black_piece)

            # data = pickle.dumps(socketstep)
            # connection.__send__(data)
            # print(pickle.loads(data))
            # print("move sent to server")

            black_options = check_options(black_pieces, black_locations, 'black')
            white_options = check_options(white_pieces, white_locations, 'white')
            turn_step = 2

            # connection.__send__(f"({turn_step},{click_coord[0]},{click_coord[1]})".encode())
            selection = 100
            valid_moves = []
            connection.new_move[0] = -1
        else:
            print('new move')
            print(connection.new_move)

            # gets the new move from server, needs to render to board accordingly
            # to new move and change its status back to -1
            move = connection.new_move[1]
            print('got new move:%s' % move)
            moves = move.split("), (")
            move_from, move_to = moves[0], moves[1]

            move_from_coord = (int(move_from.split(", ")[0].split("(")[1]), int(move_from.split(", ")[1]))
            selection = black_locations.index(move_from_coord)
            if turn_step == 2:
                turn_step = 3

            move_to_coord = (int(move_to.split(", ")[0]), int(move_to.split(", ")[1].split(")")[0]))
            # change black coordinates
            black_locations[selection] = move_to_coord
            print("black move to", move_to_coord)
            socketstep.append(move_to_coord)

            # remove eaten white piece
            if move_to_coord in white_locations:
                white_piece = white_locations.index(move_to_coord)
                captured_pieces_black.append(white_pieces[white_piece])
                if white_pieces[white_piece] == 'king':
                    winner = 'white'
                white_pieces.pop(white_piece)
                white_locations.pop(white_piece)

            # data = pickle.dumps(socketstep)
            # connection.__send__(data)
            # print(pickle.loads(data))
            # print("move sent to server")

            black_options = check_options(black_pieces, black_locations, 'black')
            white_options = check_options(white_pieces, white_locations, 'white')
            turn_step = 0

            # connection.__send__(f"({turn_step},{click_coord[0]},{click_coord[1]})".encode())
            selection = 100
            valid_moves = []
            connection.new_move[0] = -1

    # the actual handling of the players move
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            prev_click_coord = (-1, -1)
            if click_coord:
                prev_click_coord = click_coord
                socketstep.append(prev_click_coord)
            click_coord = (x_coord, y_coord)
            # connection.__send__(f"({turn_step},{click_coord[0]},{click_coord[1]})".encode())

            # white move
            if turn_step <= 1:
                # if the players role is black, he just waits for a message from the server
                if connection.player_role != "0":
                    while connection.new_move[0] == -1:
                        sleep(1)

                    # gets the new move from server, needs to render to board accordingly to new move and change its
                    # status back to -1
                    move = connection.new_move[1]
                    print('got new move:%s' % move)
                    moves = move.split("), (")
                    move_from, move_to = moves[0], moves[1]

                    move_from_coord = (int(move_from.split(", ")[0].split("(")[1]), int(move_from.split(", ")[1]))
                    selection = white_locations.index(move_from_coord)
                    print("white", prev_click_coord)
                    if turn_step == 0:
                        turn_step = 1

                    move_to_coord = (int(move_to.split(", ")[0]), int(move_to.split(", ")[1].split(")")[0]))
                    # change whites coordinates
                    white_locations[selection] = move_to_coord
                    print("white move to", move_to_coord)
                    socketstep.append(move_to_coord)

                    # remove eaten black piece
                    if move_to_coord in black_locations:
                        black_piece = black_locations.index(move_to_coord)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)

                    # data = pickle.dumps(socketstep)
                    # connection.__send__(data)
                    # print(pickle.loads(data))
                    # print("move sent to server")

                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2

                    # connection.__send__(f"({turn_step},{click_coord[0]},{click_coord[1]})".encode())
                    selection = 100
                    valid_moves = []
                    connection.new_move[0] = -1

                else:
                    if click_coord == (8, 8) or click_coord == (9, 8):
                        winner = 'black'
                    if click_coord in white_locations:
                        # white
                        selection = white_locations.index(click_coord)
                        print("white", prev_click_coord)
                        if turn_step == 0:
                            turn_step = 1

                    if click_coord in valid_moves and selection != 100:
                        # change whites coordinates
                        white_locations[selection] = click_coord
                        print("white move to", click_coord)
                        socketstep.append(click_coord)

                        # remove eaten black piece
                        if click_coord in black_locations:
                            black_piece = black_locations.index(click_coord)
                            captured_pieces_white.append(black_pieces[black_piece])
                            if black_pieces[black_piece] == 'king':
                                winner = 'white'
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)

                        print('white step:')
                        print(socketstep)
                        # data = pickle.dumps(socketstep)
                        data = pickle.dumps(mirrorMove(socketstep))

                        # connection.__send__(pickle.dumps([(1, 0), (2, 0)]))
                        connection.__send__(data)
                        print(pickle.loads(data))
                        print("move sent to server")

                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 2

                        # connection.__send__(f"({turn_step},{click_coord[0]},{click_coord[1]})".encode())
                        selection = 100
                        valid_moves = []
                        break

            # black move
            if turn_step > 1:

                # if the players role is white, he just waits for a message from the server
                if connection.player_role == "0":
                    while connection.new_move[0] == -1:
                        sleep(1)

                    print('new move')
                    print(connection.new_move)

                    # gets the new move from server, needs to render to board accordingly
                    # to new move and change its status back to -1
                    move = connection.new_move[1]
                    print('got new move:%s' % move)
                    moves = move.split("), (")
                    move_from, move_to = moves[0], moves[1]

                    move_from_coord = (int(move_from.split(", ")[0].split("(")[1]), int(move_from.split(", ")[1]))
                    selection = black_locations.index(move_from_coord)
                    print("black", prev_click_coord)
                    if turn_step == 2:
                        turn_step = 3

                    move_to_coord = (int(move_to.split(", ")[0]), int(move_to.split(", ")[1].split(")")[0]))
                    # change black coordinates
                    black_locations[selection] = move_to_coord
                    print("black move to", move_to_coord)
                    socketstep.append(move_to_coord)

                    # remove eaten white piece
                    if move_to_coord in white_locations:
                        white_piece = white_locations.index(move_to_coord)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'white'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)

                    # data = pickle.dumps(socketstep)
                    # connection.__send__(data)
                    # print(pickle.loads(data))
                    # print("move sent to server")

                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0

                    # connection.__send__(f"({turn_step},{click_coord[0]},{click_coord[1]})".encode())
                    selection = 100
                    valid_moves = []
                    connection.new_move[0] = -1
                else:
                    if click_coord == (8, 8) or click_coord == (9, 8):
                        winner = 'white'
                    if click_coord in black_locations:
                        # black
                        selection = black_locations.index(click_coord)
                        print("black try:", click_coord)

                        if turn_step == 2:
                            turn_step = 3
                    if click_coord in valid_moves and selection != 100:
                        # black
                        black_locations[selection] = click_coord
                        print("black move to", click_coord)
                        socketstep.append(click_coord)

                        if click_coord in white_locations:

                            white_piece = white_locations.index(click_coord)
                            captured_pieces_black.append(white_pieces[white_piece])
                            if white_pieces[white_piece] == 'king':
                                winner = 'black'
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)

                        print('black step:')
                        print(socketstep)
                        data = pickle.dumps(mirrorMove(socketstep))
                        # data = pickle.dumps(socketstep)
                        connection.__send__(data)
                        print(pickle.loads(data))
                        print("move sent to server")

                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 0
                        selection = 100
                        valid_moves = []

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''

                white_pieces = pieces_list.copy()
                black_pieces = pieces_list.copy()

                if connection.player_role == "0":
                    white_locations, black_locations = player_pieces_locations, opponent_pieces_locations
                else:
                    black_locations, white_locations = player_pieces_locations, opponent_pieces_locations

                # white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                #                 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                # white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                #                    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                # black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                #                 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                # black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                #                    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6),
                #                    (6, 6), (7, 6)]

                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()
pygame.quit()
connection.__close__()
