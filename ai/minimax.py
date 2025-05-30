import chess
from typing import Tuple, Optional, List
import random
from game.move_generator import evaluate_board

class MinimaxAI:
    def __init__(self, max_depth: int = 4, ai_color: chess.Color = chess.BLACK):
        self.max_depth = max_depth
        self.ai_color = ai_color
        self.nodes_evaluated = 0

    def set_ai_color(self, color: chess.Color):
        """Set the AI's color."""
        self.ai_color = color

    def find_best_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Find the best move using minimax with alpha-beta pruning."""
        if board.is_game_over():
            return None

        # Update AI color based on whose turn it is
        self.ai_color = board.turn
        
        self.nodes_evaluated = 0
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        # Get all legal moves and order them
        legal_moves = list(board.legal_moves)
        ordered_moves = self._order_moves(board, legal_moves)

        # Evaluate each move from AI's perspective
        for move in ordered_moves:
            # Create a copy of the board for this search branch
            board_copy = board.copy()
            board_copy.push(move)
            # AI is maximizing player, opponent is minimizing
            value = self._minimax(board_copy, self.max_depth - 1, alpha, beta, False, self.ai_color)
            # No board.pop() needed on the original board, as we used a copy

            if value > best_value:
                best_value = value
                best_move = move
                alpha = max(alpha, value)

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
            # Prioritize checks by simulating the move on a temporary copy
            temp_board_for_check = board.copy()
            temp_board_for_check.push(move)
            if temp_board_for_check.is_check():
                score += 5
            # No pop needed for temp_board_for_check
            move_scores.append((move, score))
        
        # Sort moves by score in descending order
        move_scores.sort(key=lambda x: x[1], reverse=True)
        return [move for move, _ in move_scores]

    def _minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, 
                 maximizing_player: bool, ai_color: chess.Color) -> float:
        """Recursive minimax implementation with alpha-beta pruning."""
        self.nodes_evaluated += 1
        
        if depth == 0 or board.is_game_over():
            return evaluate_board(board, ai_color)

        if maximizing_player:
            max_eval = float('-inf')
            for move in self._order_moves(board, list(board.legal_moves)):
                board.push(move)
                eval = self._minimax(board, depth - 1, alpha, beta, False, ai_color)
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
                eval = self._minimax(board, depth - 1, alpha, beta, True, ai_color)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval 