import pygame
import chess
from typing import Optional
from gui.gui import ChessGUI
from game.board import ChessBoard
from ai.minimax import MinimaxAI

class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.gui = ChessGUI()
        self.ai = MinimaxAI(max_depth=2)
        self.running = True
        self.game_over = False

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                move = self.gui.handle_click(event.pos, self.board.board)
                if move is not None:
                    self.board.make_move(move)
                    if self.board.is_game_over():
                        self.game_over = True
                    else:
                        ai_move = self.ai.find_best_move(self.board.board)
                        if ai_move is not None:
                            self.board.make_move(ai_move)
                            if self.board.is_game_over():
                                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.board.reset()
                    self.game_over = False
                elif event.key == pygame.K_u:
                    if self.board.board.move_stack:
                        self.board.board.pop()
        return True

    def run(self):
        while self.running:
            self.running = self.handle_events()
            self.gui.draw_board(self.board.board)
        pygame.quit() 