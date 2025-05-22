import chess
from typing import Tuple, Optional, List
import random
from game.move_generator import evaluate_board

class MinimaxAI:
    def __init__(self, max_depth: int = 4):
        self.max_depth = max_depth
        self.nodes_evaluated = 0

    def find_best_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Find the best move using minimax with alpha-beta pruning."""
        if board.is_game_over():
            return None

        self.nodes_evaluated = 0
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        # Get all legal moves and order them
        legal_moves = list(board.legal_moves)
        ordered_moves = self._order_moves(board, legal_moves)

        # Evaluate each move
        for move in ordered_moves:
            board.push(move)
            value = self._minimax(board, self.max_depth - 1, alpha, beta, False)
            board.pop()

            if value > best_value:
                best_value = value
                best_move = move

        print(f"Nodes evaluated: {self.nodes_evaluated}")
        return best_move

    def _order_moves(self, board: chess.Board, moves: List[chess.Move]) -> List[chess.Move]:
        """Order moves to improve alpha-beta pruning efficiency."""
        move_scores = []
        for move in moves:
            score = 0
            # Prioritize captures
            if board.is_capture(move):
                score += 10
                # Prioritize captures of higher value pieces
                captured_piece = board.piece_at(move.to_square)
                if captured_piece:
                    score += captured_piece.piece_type * 2
            # Prioritize checks
            board.push(move)
            if board.is_check():
                score += 5
            board.pop()
            move_scores.append((move, score))
        
        # Sort moves by score in descending order
        move_scores.sort(key=lambda x: x[1], reverse=True)
        return [move for move, _ in move_scores]

    def _minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, 
                 maximizing_player: bool) -> float:
        """Recursive minimax implementation with alpha-beta pruning."""
        self.nodes_evaluated += 1
        
        if depth == 0 or board.is_game_over():
            return evaluate_board(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in self._order_moves(board, list(board.legal_moves)):
                board.push(move)
                eval = self._minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self._order_moves(board, list(board.legal_moves)):
                board.push(move)
                eval = self._minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval 