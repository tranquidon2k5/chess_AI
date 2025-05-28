import chess
from typing import Dict, List

# Piece values
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Piece-square tables for positional evaluation (Black's perspective)
PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    -50, -50, -50, -50, -50, -50, -50, -50,
    -10, -10, -20, -30, -30, -20, -10, -10,
    -5,  -5, -10, -25, -25, -10,  -5,  -5,
    0,   0,   0, -20, -20,   0,   0,   0,
    5,   5,  10,   0,   0,  10,   5,   5,
    5,  10,  10,  20,  20,  10,  10,   5,
    0,   0,   0,   0,   0,   0,   0,   0
]

KNIGHT_TABLE = [
    50, 40, 30, 30, 30, 30, 40, 50,
    40, 20,  0,  0,  0,  0, 20, 40,
    30,  0, -10, -15, -15, -10,  0, 30,
    30, -5, -15, -20, -20, -15, -5, 30,
    30,  0, -15, -20, -20, -15,  0, 30,
    30, -5, -10, -15, -15, -10, -5, 30,
    40, 20,  0, -5, -5,  0, 20, 40,
    50, 40, 30, 30, 30, 30, 40, 50
]

BISHOP_TABLE = [
    20, 10, 10, 10, 10, 10, 10, 20,
    10,  0,  0,  0,  0,  0,  0, 10,
    10,  0, -10, -10, -10, -10,  0, 10,
    10, -5, -5, -10, -10, -5, -5, 10,
    10,  0, -10, -10, -10, -10,  0, 10,
    10, -10, -10, -10, -10, -10, -10, 10,
    10, -5,  0,  0,  0,  0, -5, 10,
    20, 10, 10, 10, 10, 10, 10, 20
]

ROOK_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    -5, -10, -10, -10, -10, -10, -10, -5,
    5,   0,   0,   0,   0,   0,   0,  5,
    5,   0,   0,   0,   0,   0,   0,  5,
    5,   0,   0,   0,   0,   0,   0,  5,
    5,   0,   0,   0,   0,   0,   0,  5,
    5,   0,   0,   0,   0,   0,   0,  5,
    0,   0,   0, -5, -5,   0,   0,  0
]

QUEEN_TABLE = [
    20, 10, 10,  5,  5, 10, 10, 20,
    10,  0,  0,  0,  0,  0,  0, 10,
    10,  0, -5, -5, -5, -5,  0, 10,
    5,   0, -5, -5, -5, -5,  0,  5,
    0,   0, -5, -5, -5, -5,  0,  0,
    10, -5, -5, -5, -5, -5,  0, 10,
    10,  0, -5,  0,  0,  0,  0, 10,
    20, 10, 10,  5,  5, 10, 10, 20
]

KING_TABLE = [
    30, 40, 40, 50, 50, 40, 40, 30,
    30, 40, 40, 50, 50, 40, 40, 30,
    30, 40, 40, 50, 50, 40, 40, 30,
    30, 40, 40, 50, 50, 40, 40, 30,
    20, 30, 30, 40, 40, 30, 30, 20,
    10, 20, 20, 20, 20, 20, 20, 10,
    -20, -20,   0,   0,   0,   0, -20, -20,
    -20, -30, -10,   0,   0, -10, -30, -20
]

PIECE_TABLES = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE,
    chess.KING: KING_TABLE
}

def evaluate_board(board: chess.Board, for_color: chess.Color = None) -> float:
    """Evaluate the current board position from the specified color's perspective.
    If for_color is None, evaluates from the current player's perspective.
    Positive score means the specified color is in a better position.
    Negative score means the opponent is in a better position.
    """
    # Use current player's color if not specified
    if for_color is None:
        for_color = board.turn
    
    if board.is_checkmate():
        # If it's the specified color's turn and it's checkmate, they lose
        # If it's opponent's turn and it's checkmate, the specified color wins
        return -10000 if board.turn == for_color else 10000
    
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # Calculate score from the specified color's perspective
    score = 0
    
    # Material and positional evaluation
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = PIECE_VALUES[piece.piece_type]
            table = PIECE_TABLES[piece.piece_type]
            
            # Use appropriate table index based on piece color
            table_index = square if piece.color == chess.BLACK else chess.square_mirror(square)
            piece_score = value + table[table_index]
            
            # Add or subtract based on piece color relative to for_color
            if piece.color == for_color:
                score += piece_score
            else:
                score -= piece_score

    # Mobility evaluation
    # Calculate mobility for the current player
    mobility_score = len(list(board.legal_moves)) * 10
    
    # Add mobility bonus/penalty based on whose turn it is
    if board.turn == for_color:
        score += mobility_score 
    else:
        score -= mobility_score

    return score 