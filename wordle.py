# CODE YOUR OWN WORDLE IN 60 SECONDS
# import your modules
import random
from tkinter import CENTER
import pygame
import words
pygame.init()

# create screen, fonts, colors, game variables
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
gray = (128, 128, 128)
WIDTH = 500
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Wordle Game - By Amisha')
level = 1
win = 0
loss = 0
turn = 0
c = 1
board = [["L", "E", "V", "E", "L"],
         [" ", " ", str(level), " ", " "],
         [" ", " ", " ", " ", " "],
         ["P", "R", "E", "S", "S"],
         [" ", " ", "A", " ", " "],
         [" ", "K", "E", "Y", " "]]

fps = 60
timer = pygame.time.Clock()
huge_font = pygame.font.Font('freesansbold.ttf', 56)
secret_word = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
print(secret_word)
game_over = False
letters = 0
turn_active = True

# create routine for drawing the board


def draw_board():
    global win
    global loss
    global turn
    global board
    global c
    for col in range(0, 5):
        for row in range(0, 6):
            if win == 1:
                pygame.draw.rect(
                    screen, white, [col * 100 + 12, row * 100 + 12, 75, 75], 3, 5)
                piece_text = huge_font.render(board[row][col], True, green)
                screen.blit(piece_text, (col * 100 + 30, row * 100 + 25))
            elif loss == 1:
                pygame.draw.rect(
                    screen, white, [col * 100 + 12, row * 100 + 12, 75, 75], 3, 5)
                piece_text = huge_font.render(board[row][col], True, red)
                screen.blit(piece_text, (col * 100 + 30, row * 100 + 25))
            else:
                pygame.draw.rect(
                    screen, white, [col * 100 + 12, row * 100 + 12, 75, 75], 3, 5)
                piece_text = huge_font.render(board[row][col], True, gray)
                screen.blit(piece_text, (col * 100 + 30, row * 100 + 25))
    if win == 0 and loss == 0 and c == 0:
        pygame.draw.rect(
            screen, green, [5, turn * 100 + 5, WIDTH - 10, 90], 3, 5)

# create routine for checking letters


def check_words():
    global turn
    global board
    global secret_word

    for col in range(0, 5):
        for row in range(0, 6):
            if secret_word != "" and secret_word[col] == board[row][col] and turn > row:
                pygame.draw.rect(
                    screen, green, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 5)
            elif secret_word != "" and board[row][col] in secret_word and turn > row:
                pygame.draw.rect(screen, yellow, [
                    col * 100 + 12, row * 100 + 12, 75, 75], 0, 5)


def valid_word():
    global board
    ltr = ""
    for y in range(0, 6):
        # ltr = ""
        for x in range(0, 5):
            if board[y][x] == " ":
                break
            else:
                ltr += board[y][x]
    ltr = ltr[-5:]
    if ltr not in words.WORDS:
        return False
    else:
        check_words()
        draw_board()
        return True

# set up your main game loop


running = True
while running:
    timer.tick(fps)
    screen.fill(black)
    check_words()
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
# add player controls for letter entry, backspacing, checking guesses and restarting

        if event.type == pygame.TEXTINPUT and turn_active and not game_over:
            if c == 1:
                board = [[" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "]]
                c = 0
            entry = event.__getattribute__('text')
            if entry != " ":
                entry = entry.upper()
                board[turn][letters] = entry
                letters += 1
        if event.type == pygame.KEYDOWN:
            if c == 1:
                board = [[" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "]]
                c = 0
                continue
            if event.key == pygame.K_BACKSPACE and letters > 0:
                board[turn][letters - 1] = ' '
                letters -= 1
            if event.key == pygame.K_RETURN and not game_over:
                if valid_word() == False:
                    for z in range(0, 5):
                        board[turn][letters - 1] = ' '
                        letters -= 1
                else:
                    turn += 1
                    letters = 0
            if event.key == pygame.K_RETURN and game_over:
                loss = 0
                win = 0
                turn = 0
                letters = 0
                game_over = False
                secret_word = words.WORDS[random.randint(
                    0, len(words.WORDS) - 1)]
                # print(secret_word)
                board = [[" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "]]

        # control turn active based on letters
        if letters == 5:
            turn_active = False
        if letters < 5:
            turn_active = True

        # check if guess is correct, add game over conditions

        for row in range(0, 6):
            guess = board[row][0] + board[row][1] + \
                board[row][2] + board[row][3] + board[row][4]
            if guess == secret_word and row < turn:
                game_over = True

        if turn == 6:
            loss = 1
            game_over = True
            board = [["O", "O", "P", "S", "!"],
                     [" ", "Y", "O", "U", " "],
                     ["L", "O", "S", "T", "!"],
                     [" ", "I", "T", "-", " "],
                     [" ", "W", "A", "S", " "],
                     [secret_word[0], secret_word[1], secret_word[2], secret_word[3], secret_word[4]]]
            secret_word = ""
            winner_text = huge_font.render('     LOSER!', True, red)
            turn = 7

        if game_over and turn < 6:
            win = 1
            board = [[" ", "Y", "O", "U", " "],
                     ["A", "C", "E", "D", "!"],
                     ["L", "E", "V", "E", "L"],
                     [" ", " ", str(level), " ", " "],
                     ["P", "R", "E", "S", "S"],
                     ["E", "N", "T", "E", "R"], ]
            level += 1
            secret_word = ""
            winner_text = huge_font.render('     WINNER!', True, green)
            screen.blit(winner_text, (40, 610))
            turn = 7

    pygame.display.flip()
pygame.quit()
