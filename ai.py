"""
Moduł AI odpowiedzialny za implementację logiki przeciwnika komputerowego w grze.
"""

import random


def ai_move(board, symbol):
    """
    Prosta logika ruchu AI - wybiera losowe wolne miejsce na planszy.

    Args:
        board (GameBoard): Obiekt planszy do gry.
        symbol (str): Symbol przypisany do AI (np. 'O').

    Returns:
        tuple: Współrzędne (wiersz, kolumna) wybranego ruchu AI.
    """
    available_positions = board.get_available_positions()
    if available_positions:
        return random.choice(available_positions)
    return None


def minimax(board, depth, is_maximizing, ai_symbol, player_symbol):
    """
    Implementacja algorytmu Minimax dla ruchów AI, aby zoptymalizować ruchy.

    Args:
        board (GameBoard): Obiekt planszy do gry.
        depth (int): Głębokość rekurencji (poziom symulacji ruchów).
        is_maximizing (bool): Flaga wskazująca, czy obecna symulacja maksymalizuje wynik AI.
        ai_symbol (str): Symbol AI (np. 'O').
        player_symbol (str): Symbol gracza (np. 'X').

    Returns:
        int: Wynik symulowanego ruchu (wartość punktowa).
    """
    # Sprawdzamy, czy AI wygrało
    if board.check_for_win(ai_symbol):
        return 10 - depth
    # Sprawdzamy, czy gracz wygrał
    elif board.check_for_win(player_symbol):
        return depth - 10
    # Sprawdzamy, czy jest remis
    elif not any(' ' in row for row in board.board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row, col in board.get_available_positions():
            board.place_symbol(ai_symbol, row, col)
            score = minimax(board, depth + 1, False, ai_symbol, player_symbol)
            board.place_symbol(' ', row, col)  # Cofamy ruch
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row, col in board.get_available_positions():
            board.place_symbol(player_symbol, row, col)
            score = minimax(board, depth + 1, True, ai_symbol, player_symbol)
            board.place_symbol(' ', row, col)  # Cofamy ruch
            best_score = min(score, best_score)
        return best_score


def get_best_move(board, ai_symbol, player_symbol):
    """
    Znajduje najlepszy ruch dla AI przy użyciu algorytmu Minimax.

    Args:
        board (GameBoard): Obiekt planszy do gry.
        ai_symbol (str): Symbol AI (np. 'O').
        player_symbol (str): Symbol gracza (np. 'X').

    Returns:
        tuple: Współrzędne (wiersz, kolumna) najlepszego ruchu AI.
    """
    best_score = -float('inf')
    best_move = None
    for row, col in board.get_available_positions():
        board.place_symbol(ai_symbol, row, col)
        score = minimax(board, 0, False, ai_symbol, player_symbol)
        board.place_symbol(' ', row, col)  # Cofamy ruch
        if score > best_score:
            best_score = score
            best_move = (row, col)
    return best_move
