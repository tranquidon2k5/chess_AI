import pygame
import chess
from typing import Optional
from gui.gui import ChessGUI
from game.board import ChessBoard
from ai.minimax import MinimaxAI

class ChessGame:
    def __init__(self, ai_color: chess.Color = chess.BLACK):
        self.board = ChessBoard()
        self.gui = ChessGUI()
        self.ai = MinimaxAI(max_depth=2, ai_color=ai_color)
        self.ai_color = ai_color
        self.running = True
        self.game_over = False

    def set_ai_color(self, color: chess.Color):
        """Set which color the AI plays."""
        self.ai_color = color
        self.ai.set_ai_color(color)

    def is_ai_turn(self) -> bool:
        """Check if it's the AI's turn to move."""
        return self.board.board.turn == self.ai_color

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                # Only handle human moves when it's not AI's turn
                if not self.is_ai_turn():
                    move = self.gui.handle_click(event.pos, self.board.board)
                    if move is not None:
                        self.board.make_move(move)
                        if self.board.is_game_over():
                            self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.board.reset()
                    self.game_over = False
                elif event.key == pygame.K_u:
                    if self.board.board.move_stack:
                        self.board.board.pop()
                elif event.key == pygame.K_w:
                    # Switch AI to white
                    self.set_ai_color(chess.WHITE)
                    self.board.reset()
                    self.game_over = False
                elif event.key == pygame.K_b:
                    # Switch AI to black
                    self.set_ai_color(chess.BLACK)
                    self.board.reset()
                    self.game_over = False
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True

    def update(self):
        """Update game state, including AI moves."""
        if not self.game_over and self.is_ai_turn():
            ai_move = self.ai.find_best_move(self.board.board)
            if ai_move is not None:
                self.board.make_move(ai_move)
                if self.board.is_game_over():
                    self.game_over = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.running = self.handle_events()
            self.update()
            self.gui.draw_board(self.board.board)
            clock.tick(60)  # Limit to 60 FPS
        pygame.quit() 