import pygame
import chess
from typing import Optional, Tuple, List
import os

class ChessGUI:
    def __init__(self, width: int = 800, height: int = 800):
        self.width = width
        self.height = height
        self.square_size = width // 8
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Chess AI Game")
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_SQUARE = (240, 217, 181)
        self.DARK_SQUARE = (181, 136, 99)
        self.HIGHLIGHT = (124, 252, 0, 128)
        self.MOVE_HIGHLIGHT = (106, 168, 79, 128)
        # Load piece images
        self.piece_images = {}
        self._load_piece_images()
        # Selection state
        self.selected_square: Optional[chess.Square] = None
        self.valid_moves: List[chess.Move] = []

    def _load_piece_images(self):
        pieces = ['p', 'n', 'b', 'r', 'q', 'k']
        colors = ['w', 'b']
        for color in colors:
            for piece in pieces:
                image_path = os.path.join('assets', f'{color}{piece}.png')
                try:
                    image = pygame.image.load(image_path)
                    image = pygame.transform.scale(image, (self.square_size, self.square_size))
                    self.piece_images[f'{color}{piece}'] = image
                except pygame.error:
                    print(f"Warning: Could not load image {image_path}")

    def draw_board(self, board: chess.Board):
        for row in range(8):
            for col in range(8):
                x = col * self.square_size
                y = row * self.square_size
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))
        # Draw highlights
        if self.selected_square is not None:
            row = chess.square_rank(self.selected_square)
            col = chess.square_file(self.selected_square)
            x = col * self.square_size
            y = (7 - row) * self.square_size
            s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            s.fill(self.HIGHLIGHT)
            self.screen.blit(s, (x, y))
            for move in self.valid_moves:
                if move.from_square == self.selected_square:
                    row = chess.square_rank(move.to_square)
                    col = chess.square_file(move.to_square)
                    x = col * self.square_size
                    y = (7 - row) * self.square_size
                    s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                    s.fill(self.MOVE_HIGHLIGHT)
                    self.screen.blit(s, (x, y))
        # Draw pieces
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                row = chess.square_rank(square)
                col = chess.square_file(square)
                x = col * self.square_size
                y = (7 - row) * self.square_size
                piece_key = f"{'w' if piece.color == chess.WHITE else 'b'}{piece.symbol().lower()}"
                if piece_key in self.piece_images:
                    self.screen.blit(self.piece_images[piece_key], (x, y))
        pygame.display.flip()

    def get_square_from_pos(self, pos: Tuple[int, int]) -> Optional[chess.Square]:
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            col = x // self.square_size
            row = 7 - (y // self.square_size)
            return chess.square(col, row)
        return None

    def handle_click(self, pos: Tuple[int, int], board: chess.Board) -> Optional[chess.Move]:
        square = self.get_square_from_pos(pos)
        if square is None:
            self.selected_square = None
            self.valid_moves = []
            return None
        if self.selected_square is None:
            piece = board.piece_at(square)
            if piece is not None and piece.color == board.turn:
                self.selected_square = square
                self.valid_moves = [move for move in board.legal_moves if move.from_square == square]
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.valid_moves:
                self.selected_square = None
                self.valid_moves = []
                return move
            else:
                piece = board.piece_at(square)
                if piece is not None and piece.color == board.turn:
                    self.selected_square = square
                    self.valid_moves = [move for move in board.legal_moves if move.from_square == square]
                else:
                    self.selected_square = None
                    self.valid_moves = []
        return None 