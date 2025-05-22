import chess
from typing import Optional, List, Tuple

class ChessBoard:
    def __init__(self):
        self.board = chess.Board()
        self.selected_square: Optional[chess.Square] = None
        self.valid_moves: List[chess.Move] = []

    def get_piece_at(self, square: chess.Square) -> Optional[chess.Piece]:
        """Get the piece at a given square."""
        return self.board.piece_at(square)

    def is_valid_move(self, move: chess.Move) -> bool:
        """Check if a move is legal."""
        return move in self.board.legal_moves

    def make_move(self, move: chess.Move) -> bool:
        """Make a move if it's legal."""
        if self.is_valid_move(move):
            self.board.push(move)
            return True
        return False

    def get_valid_moves(self, square: chess.Square) -> List[chess.Move]:
        """Get all valid moves for a piece at the given square."""
        return [move for move in self.board.legal_moves if move.from_square == square]

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.board.is_game_over()

    def get_game_result(self) -> Optional[str]:
        """Get the game result if the game is over."""
        if not self.is_game_over():
            return None
        
        if self.board.is_checkmate():
            return "Checkmate"
        elif self.board.is_stalemate():
            return "Stalemate"
        elif self.board.is_insufficient_material():
            return "Insufficient Material"
        elif self.board.is_fifty_moves():
            return "Fifty-move Rule"
        elif self.board.is_repetition():
            return "Threefold Repetition"
        return None

    def get_board_state(self) -> str:
        """Get the current board state in FEN notation."""
        return self.board.fen()

    def reset(self):
        """Reset the board to the initial position."""
        self.board = chess.Board()
        self.selected_square = None
        self.valid_moves = [] 