import random
from board import GameBoard
from player import Player
import pygame


class Game:
    """
    Reprezentuje grę, w której gracze rywalizują ze sobą w układaniu symboli na planszy.

    Attributes:
        round_number (int): Numer aktualnej rundy.
        board (GameBoard): Obiekt planszy do gry.
        players (list): Lista graczy biorących udział w grze.
        current_player (Player): Aktualnie wykonujący ruch gracz.
    """

    def __init__(self):
        """
        Inicjalizuje nową grę, ustawia planszę i przygotowuje listę graczy.
        """
        self.round_number = 1
        self.board = GameBoard(10)
        self.players = []
        self.current_player = None

    def choose_game_mode(self):
        """
        Wybiera tryb gry: gracz vs gracz lub gracz vs AI.
        Dodaje odpowiednich graczy do gry.
        """
        choice = input("Choose game mode:\n1. Play vs Player\n2. Play vs AI\n")
        if choice == '1':
            self.players.append(Player('X'))
            self.players.append(Player('O'))
        elif choice == '2':
            self.players.append(Player('X'))
            self.players.append(Player('O', is_ai=True))
        else:
            print("Invalid choice, defaulting to Player vs Player.")
            self.players.append(Player('X'))
            self.players.append(Player('O'))

        self.current_player = random.choice(self.players)
        print(f"{self.current_player.symbol} starts the game!")

    def next_round(self):
        """
        Zwiększa numer rundy o 1.
        """
        self.round_number += 1

    def check_for_round_end(self):
        """
        Sprawdza, czy runda się zakończyła poprzez wygraną lub zapełnienie planszy.

        Returns:
            bool: True, jeśli runda się zakończyła (ktoś wygrał lub plansza jest pełna), False w przeciwnym razie.
        """
        if self.board.check_for_win(self.current_player.symbol):
            print(f"{self.current_player.symbol} wins the round!")
            self.current_player.points += 1
            return True
        elif not any(' ' in row for row in self.board.board):
            print("The board is full! The round ends in a draw.")
            return True
        return False

    def play_round(self):
        """
        Rozgrywa jedną rundę gry, obsługuje tury graczy i sprawdza warunki zakończenia rundy.
        """
        self.board.display_board()
        while True:
            self.player_turn()
            self.board.display_board()
            if self.check_for_round_end():
                break
            self.switch_player()

    def play_game(self):
        """
        Rozgrywa pełną grę składającą się z 3 rund.
        Inicjalizuje wybór trybu gry, a następnie przeprowadza kolejne rundy.
        """
        self.choose_game_mode()
        self.current_player = random.choice(self.players)
        print(f"{self.current_player.symbol} starts the game!")

        while self.round_number <= 3:
            print(f"Starting round {self.round_number}!")
            self.play_round()
            if self.round_number < 3:
                self.next_round()
            else:
                self.end_game()

    def switch_player(self):
        """
        Zmienia aktualnego gracza na następnego w kolejności.
        """
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]

    def end_game(self):
        """
        Sumuje wyniki po 3 rundach, ogłasza zwycięzcę i kończy grę.
        """
        player_1_points = self.players[0].points
        player_2_points = self.players[1].points

        print(f"Final score: Player 1: {player_1_points} points, Player 2: {player_2_points} points.")
        if player_1_points > player_2_points:
            print("Player 1 wins the game!")
        elif player_2_points > player_1_points:
            print("Player 2 wins the game!")
        else:
            print("It's a draw!")

        pygame.quit()
        exit()

    def end_round(self):
        """
        Zakończenie rundy i reset planszy lub zakończenie gry po 3 rundach.
        """
        self.round_number += 1
        if self.round_number > 3:
            self.end_game()
        else:
            self.board = GameBoard(10)
            print(f"Starting round {self.round_number}!")

    def player_turn(self):
        """
        Obsługuje ruch aktualnego gracza lub AI.
        """
        if self.current_player.is_ai:
            print("AI's turn...")
            self.ai_move()
        else:
            print(f"{self.current_player.symbol}'s turn.")
            while True:
                try:
                    row, col = map(int, input("Enter row and column (e.g., 1 1): ").split())
                    if self.board.is_spot_available(row, col):
                        self.board.place_symbol(self.current_player.symbol, row, col)
                        break
                    else:
                        print("That spot is already taken. Try again.")
                except (ValueError, IndexError):
                    print("Invalid input. Please enter two numbers separated by a space, e.g., '1 1'.")

    def ai_move(self):
        """
        Logika ruchu AI - wybiera losowe wolne miejsce na planszy.
        """
        available_positions = self.board.get_available_positions()
        if available_positions:
            row, col = random.choice(available_positions)
            self.board.place_symbol(self.current_player.symbol, row, col)
            print(f"AI placed {self.current_player.symbol} at ({row}, {col})")
