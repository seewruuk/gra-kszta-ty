class Player:
    """
    Reprezentuje gracza w grze, który może być człowiekiem lub AI.

    Attributes:
        symbol (str): Symbol przypisany do gracza ('X' lub 'O').
        is_ai (bool): Flaga określająca, czy gracz jest AI. Domyślnie False (gracz to człowiek).
        points (int): Liczba punktów zdobytych przez gracza w trakcie gry.
    """

    def __init__(self, symbol, is_ai=False):
        """
        Inicjalizuje nowego gracza.

        Args:
            symbol (str): Symbol przypisany do gracza ('X' lub 'O').
            is_ai (bool): Flaga określająca, czy gracz jest AI. Domyślnie False (gracz to człowiek).
        """
        self.symbol = symbol
        self.is_ai = is_ai
        self.points = 0
