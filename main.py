"""
Gra 'Kształty'

Kacper Sewruk s23466
Michał Jastrzemski s26245
"""

import pygame
from game import Game
from player import Player

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
WINDOW_SIZE = 600  # Rozmiar okna (kwadratowe)
GRID_SIZE = 10  # Plansza 10x10
CELL_SIZE = WINDOW_SIZE // GRID_SIZE  # Wielkość jednego pola

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Ustawienia okna gry
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Gra - Kształty")


def draw_board(current_game):
    """
    Rysuje planszę gry na ekranie.

    Args:
        current_game (Game): Obiekt gry, który przechowuje stan planszy i graczy.
    """
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, BLACK, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            if current_game.board.board[row][col] == 'X':
                pygame.draw.circle(screen, RED, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 3)
            elif current_game.board.board[row][col] == 'O':
                pygame.draw.circle(screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 3)


def handle_mouse_click(current_game, x, y):
    """
    Obsługuje kliknięcia myszką i wykonuje ruch gracza lub AI.

    Args:
        current_game (Game): Obiekt gry, który przechowuje stan planszy i graczy.
        x (int): Pozycja X kliknięcia.
        y (int): Pozycja Y kliknięcia.
    """
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    if current_game.board.is_spot_available(row, col):
        current_game.board.place_symbol(current_game.current_player.symbol, row, col)

        points = current_game.board.check_for_win(current_game.current_player.symbol)
        if points > 0:
            print(f"{current_game.current_player.symbol} wins the round and earns {points} points!")
            current_game.current_player.points += points
            current_game.end_round()
        elif not any(' ' in row for row in current_game.board.board):
            print("The board is full! The round ends in a draw.")
            current_game.end_round()
        else:
            current_game.switch_player()

            # Sprawdzenie ruchu AI
            if current_game.current_player.is_ai:
                current_game.ai_move()
                points = current_game.board.check_for_win(current_game.current_player.symbol)
                if points > 0:
                    print(f"{current_game.current_player.symbol} wins the round and earns {points} points!")
                    current_game.current_player.points += points
                    current_game.end_round()
                elif not any(' ' in row for row in current_game.board.board):
                    print("The board is full! The round ends in a draw.")
                    current_game.end_round()
                else:
                    current_game.switch_player()


def choose_game_mode_with_keys():
    """
    Wyświetla ekran wyboru trybu gry i czeka na decyzję użytkownika.

    Returns:
        int: 1, jeśli użytkownik wybierze grę gracz vs gracz, 2 dla gracz vs AI.
    """
    choosing_mode = True
    mode = None
    while choosing_mode:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Press 1 for Player vs Player or 2 for Player vs AI", True, BLACK)
        screen.blit(text_surface, (20, WINDOW_SIZE // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = 1
                    choosing_mode = False
                elif event.key == pygame.K_2:
                    mode = 2
                    choosing_mode = False

    return mode


# Inicjalizacja gry
game = Game()

# Wybór trybu gry
mode = choose_game_mode_with_keys()

# Inicjalizacja graczy w zależności od wybranego trybu gry
if mode == 1:
    game.players.append(Player('X'))
    game.players.append(Player('O'))
elif mode == 2:
    game.players.append(Player('X'))
    game.players.append(Player('O', is_ai=True))
game.current_player = game.players[0]

# Główna pętla gry
running = True
while running:
    draw_board(game)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                handle_mouse_click(game, mouse_x, mouse_y)

# Zakończenie gry i wyjście
pygame.quit()
