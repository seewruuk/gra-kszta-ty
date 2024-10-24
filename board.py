"""
Moduł odpowiedzialny za logikę planszy do gry.
"""


class GameBoard:
    """
    Klasa reprezentująca planszę do gry.

    Attributes:
        size (int): Rozmiar planszy.
        board (list): Dwuwymiarowa lista reprezentująca pola planszy.
    """

    def __init__(self, size):
        """
        Inicjalizuje obiekt planszy o podanym rozmiarze.

        Args:
            size (int): Rozmiar planszy.
        """
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]

    def display_board(self):
        """
        Wyświetla planszę w konsoli w formacie tekstowym.
        """
        print("   " + "   ".join([str(i) for i in range(self.size)]))
        print("   " + "---" * self.size)

        for index, row in enumerate(self.board):
            print(f"{index} | " + " | ".join(row) + " |")
            print("   " + "---" * self.size)

    def is_spot_available(self, row, col):
        """
        Sprawdza, czy dane pole na planszy jest dostępne.

        Args:
            row (int): Wiersz planszy.
            col (int): Kolumna planszy.

        Returns:
            bool: True, jeśli pole jest dostępne, False w przeciwnym wypadku.
        """
        return self.board[row][col] == ' '

    def place_symbol(self, symbol, row, col):
        """
        Umieszcza symbol na planszy w podanym miejscu.

        Args:
            symbol (str): Symbol, który ma zostać umieszczony (np. 'X' lub 'O').
            row (int): Wiersz planszy.
            col (int): Kolumna planszy.
        """
        self.board[row][col] = symbol

    def get_available_positions(self):
        """
        Zwraca listę dostępnych pozycji na planszy.

        Returns:
            list: Lista krotek zawierających dostępne współrzędne (wiersz, kolumna).
        """
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == ' ']

    def check_t_shape(self, symbol):
        """
        Sprawdza, czy na planszy znajduje się kształt litery T utworzony z podanego symbolu.

        Args:
            symbol (str): Symbol, który ma być sprawdzony.

        Returns:
            bool: True, jeśli kształt T został znaleziony, False w przeciwnym wypadku.
        """
        for r in range(self.size - 2):
            for c in range(1, self.size - 1):
                if (self.board[r][c] == symbol and
                        self.board[r + 1][c - 1] == symbol and
                        self.board[r + 1][c] == symbol and
                        self.board[r + 1][c + 1] == symbol and
                        self.board[r + 2][c] == symbol):
                    return True
        return False

    def check_square_shape(self, symbol):
        """
        Sprawdza, czy na planszy znajduje się kwadrat 3x3 bez środkowego pola utworzony z podanego symbolu.

        Args:
            symbol (str): Symbol, który ma być sprawdzony.

        Returns:
            bool: True, jeśli kształt kwadratu został znaleziony, False w przeciwnym wypadku.
        """
        for r in range(self.size - 2):
            for c in range(self.size - 2):
                if (self.board[r][c] == symbol and
                        self.board[r][c + 2] == symbol and
                        self.board[r + 2][c] == symbol and
                        self.board[r + 2][c + 2] == symbol and
                        self.board[r][c + 1] == symbol and
                        self.board[r + 2][c + 1] == symbol and
                        self.board[r + 1][c] == symbol and
                        self.board[r + 1][c + 2] == symbol):
                    return True
        return False

    def check_line_shape(self, symbol):
        """
        Sprawdza, czy na planszy znajduje się linia 5 symboli w pionie lub poziomie.

        Args:
            symbol (str): Symbol, który ma być sprawdzony.

        Returns:
            bool: True, jeśli linia została znaleziona, False w przeciwnym wypadku.
        """
        for r in range(self.size):
            for c in range(self.size - 4):
                if all(self.board[r][c + i] == symbol for i in range(5)):
                    return True

        for c in range(self.size):
            for r in range(self.size - 4):
                if all(self.board[r + i][c] == symbol for i in range(5)):
                    return True

        return False

    def check_l_shape(self, symbol):
        """
        Sprawdza, czy na planszy znajduje się kształt litery L utworzony z podanego symbolu.

        Args:
            symbol (str): Symbol, który ma być sprawdzony.

        Returns:
            bool: True, jeśli kształt L został znaleziony, False w przeciwnym wypadku.
        """
        for r in range(self.size - 2):
            for c in range(self.size - 2):
                if (self.board[r][c] == symbol and
                        self.board[r + 1][c] == symbol and
                        self.board[r + 2][c] == symbol and
                        self.board[r + 2][c + 1] == symbol and
                        self.board[r + 2][c + 2] == symbol):
                    return True
        return False

    def check_for_win(self, symbol):
        """
        Sprawdza, czy któryś z kształtów (T, kwadrat, linia, L) utworzonych z danego symbolu został ułożony.

        Args:
            symbol (str): Symbol, który ma być sprawdzony.

        Returns:
            int: Liczba punktów za znaleziony kształt lub 0, jeśli kształt nie został znaleziony.
        """
        if self.check_t_shape(symbol):
            return 5  # Litera T
        elif self.check_square_shape(symbol):
            return 8  # Kwadrat
        elif self.check_line_shape(symbol):
            return 4  # Linia
        elif self.check_l_shape(symbol):
            return 5  # Litera L
        return 0  # Brak kształtu
