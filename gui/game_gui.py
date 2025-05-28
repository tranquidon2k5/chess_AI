import pygame
import chess
from typing import Optional, Tuple, List
import os
from gui.ui_manager import UIButton

class GameGUI:
    def __init__(self, width: int = 1200, height: int = 800):
        self.width = width
        self.height = height
        self.board_size = 600  # Size of the chess board
        self.board_offset_x = 50
        self.board_offset_y = (height - self.board_size) // 2
        self.square_size = self.board_size // 8
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("♔ Chess AI Master - Game ♔")
        
        # Colors
        self.bg_color = (45, 52, 54)
        self.panel_color = (55, 65, 69)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_SQUARE = (240, 217, 181)
        self.DARK_SQUARE = (181, 136, 99)
        self.HIGHLIGHT = (124, 252, 0, 128)
        self.MOVE_HIGHLIGHT = (106, 168, 79, 128)
        self.LAST_MOVE_HIGHLIGHT = (255, 255, 0, 100)
        
        # UI colors
        self.primary_color = (52, 152, 219)
        self.success_color = (46, 204, 113)
        self.danger_color = (231, 76, 60)
        self.warning_color = (230, 126, 34)
        self.text_color = (255, 255, 255)
        self.gray_color = (99, 110, 114)
        
        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 24)
        self.status_font = pygame.font.Font(None, 20)
        
        # Load piece images
        self.piece_images = {}
        self._load_piece_images()
        
        # Game state
        self.selected_square: Optional[chess.Square] = None
        self.valid_moves: List[chess.Move] = []
        self.last_move: Optional[chess.Move] = None
        self.game_status = "Ready to play"
        self.thinking = False
        
        # Control buttons
        self._create_control_buttons()
        
    def _load_piece_images(self):
        """Load chess piece images."""
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
    
    def _create_control_buttons(self):
        """Create control buttons for the game."""
        button_width = 120
        button_height = 40
        button_spacing = 10
        panel_x = self.board_offset_x + self.board_size + 30
        
        self.control_buttons = [
            UIButton(panel_x, 200, button_width, button_height, "New Game", 
                    color=self.success_color, font_size=20),
            UIButton(panel_x, 250, button_width, button_height, "Undo Move", 
                    color=self.warning_color, font_size=20),
            UIButton(panel_x, 300, button_width, button_height, "Hint", 
                    color=self.primary_color, font_size=20),
            UIButton(panel_x, 350, button_width, button_height, "Settings", 
                    color=self.danger_color, font_size=20),
        ]
    
    def draw_board_background(self):
        """Draw the chess board background."""
        board_rect = pygame.Rect(self.board_offset_x - 5, self.board_offset_y - 5, 
                                self.board_size + 10, self.board_size + 10)
        pygame.draw.rect(self.screen, self.BLACK, board_rect)
        
        for row in range(8):
            for col in range(8):
                x = self.board_offset_x + col * self.square_size
                y = self.board_offset_y + row * self.square_size
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))
    
    def draw_coordinates(self):
        """Draw file and rank labels."""
        # Files (a-h)
        for i in range(8):
            file_letter = chr(ord('a') + i)
            x = self.board_offset_x + i * self.square_size + self.square_size // 2
            y = self.board_offset_y + self.board_size + 15
            text = self.status_font.render(file_letter, True, self.text_color)
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)
        
        # Ranks (1-8)
        for i in range(8):
            rank_number = str(8 - i)
            x = self.board_offset_x - 20
            y = self.board_offset_y + i * self.square_size + self.square_size // 2
            text = self.status_font.render(rank_number, True, self.text_color)
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)
    
    def draw_highlights(self, board: chess.Board):
        """Draw square highlights."""
        # Last move highlight
        if self.last_move:
            for square in [self.last_move.from_square, self.last_move.to_square]:
                row = 7 - chess.square_rank(square)
                col = chess.square_file(square)
                x = self.board_offset_x + col * self.square_size
                y = self.board_offset_y + row * self.square_size
                s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                s.fill(self.LAST_MOVE_HIGHLIGHT)
                self.screen.blit(s, (x, y))
        
        # Selected square highlight
        if self.selected_square is not None:
            row = 7 - chess.square_rank(self.selected_square)
            col = chess.square_file(self.selected_square)
            x = self.board_offset_x + col * self.square_size
            y = self.board_offset_y + row * self.square_size
            s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            s.fill(self.HIGHLIGHT)
            self.screen.blit(s, (x, y))
            
            # Valid move highlights
            for move in self.valid_moves:
                if move.from_square == self.selected_square:
                    row = 7 - chess.square_rank(move.to_square)
                    col = chess.square_file(move.to_square)
                    x = self.board_offset_x + col * self.square_size
                    y = self.board_offset_y + row * self.square_size
                    s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                    s.fill(self.MOVE_HIGHLIGHT)
                    self.screen.blit(s, (x, y))
    
    def draw_pieces(self, board: chess.Board):
        """Draw chess pieces on the board."""
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                row = 7 - chess.square_rank(square)
                col = chess.square_file(square)
                x = self.board_offset_x + col * self.square_size
                y = self.board_offset_y + row * self.square_size
                piece_key = f"{'w' if piece.color == chess.WHITE else 'b'}{piece.symbol().lower()}"
                if piece_key in self.piece_images:
                    self.screen.blit(self.piece_images[piece_key], (x, y))
    
    def draw_side_panel(self, board: chess.Board, game_mode: str = "vs AI", ai_difficulty: str = "Hard"):
        """Draw the side panel with game information and controls."""
        panel_x = self.board_offset_x + self.board_size + 30
        panel_width = self.width - panel_x - 30
        
        # Panel background
        panel_rect = pygame.Rect(panel_x - 10, 50, panel_width, self.height - 100)
        pygame.draw.rect(self.screen, self.panel_color, panel_rect, border_radius=10)
        
        # Game info
        y_offset = 70
        
        # Game mode
        mode_text = self.title_font.render(f"Mode: {game_mode}", True, self.text_color)
        self.screen.blit(mode_text, (panel_x, y_offset))
        y_offset += 40
        
        # AI difficulty (if applicable)
        if "AI" in game_mode:
            diff_text = self.button_font.render(f"AI Difficulty: {ai_difficulty}", True, self.gray_color)
            self.screen.blit(diff_text, (panel_x, y_offset))
            y_offset += 30
        
        # Current turn
        turn_color = "White" if board.turn == chess.WHITE else "Black"
        turn_text = self.button_font.render(f"Turn: {turn_color}", True, self.text_color)
        self.screen.blit(turn_text, (panel_x, y_offset))
        y_offset += 30
        
        # Game status
        status_color = self.warning_color if self.thinking else self.text_color
        status_text = self.status_font.render(self.game_status, True, status_color)
        self.screen.blit(status_text, (panel_x, y_offset))
        
        # Control buttons
        for button in self.control_buttons:
            button.draw(self.screen)
        
        # Move history (simplified)
        history_y = 400
        history_title = self.button_font.render("Move History", True, self.text_color)
        self.screen.blit(history_title, (panel_x, history_y))
        
        # Show last few moves
        moves = list(board.move_stack)
        start_idx = max(0, len(moves) - 10)
        for i, move in enumerate(moves[start_idx:]):
            move_num = (start_idx + i) // 2 + 1
            move_text = f"{move_num}. {move}" if (start_idx + i) % 2 == 0 else f"{move}"
            text = self.status_font.render(move_text, True, self.gray_color)
            self.screen.blit(text, (panel_x, history_y + 30 + i * 20))
    
    def draw_game_over_overlay(self, result: str):
        """Draw game over overlay."""
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.title_font.render("Game Over", True, self.text_color)
        result_text = self.button_font.render(result, True, self.text_color)
        
        game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        result_rect = result_text.get_rect(center=(self.width // 2, self.height // 2))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(result_text, result_rect)
    
    def draw(self, board: chess.Board, **kwargs):
        """Draw the complete game interface."""
        # Clear screen
        self.screen.fill(self.bg_color)
        
        # Draw board
        self.draw_board_background()
        self.draw_coordinates()
        self.draw_highlights(board)
        self.draw_pieces(board)
        
        # Draw side panel
        self.draw_side_panel(board, **kwargs)
        
        # Draw game over overlay if needed
        if board.is_game_over():
            result = self.get_game_result(board)
            self.draw_game_over_overlay(result)
        
        pygame.display.flip()
    
    def get_game_result(self, board: chess.Board) -> str:
        """Get human-readable game result."""
        if board.is_checkmate():
            winner = "Black" if board.turn == chess.WHITE else "White"
            return f"{winner} wins by checkmate!"
        elif board.is_stalemate():
            return "Draw by stalemate"
        elif board.is_insufficient_material():
            return "Draw by insufficient material"
        elif board.is_seventyfive_moves():
            return "Draw by 75-move rule"
        elif board.is_fivefold_repetition():
            return "Draw by repetition"
        else:
            return "Game over"
    
    def get_square_from_pos(self, pos: Tuple[int, int]) -> Optional[chess.Square]:
        """Convert screen position to chess square."""
        x, y = pos
        # Check if click is within board bounds
        if (self.board_offset_x <= x < self.board_offset_x + self.board_size and
            self.board_offset_y <= y < self.board_offset_y + self.board_size):
            col = (x - self.board_offset_x) // self.square_size
            row = 7 - ((y - self.board_offset_y) // self.square_size)
            return chess.square(col, row)
        return None
    
    def handle_board_click(self, pos: Tuple[int, int], board: chess.Board) -> Optional[chess.Move]:
        """Handle clicks on the chess board."""
        square = self.get_square_from_pos(pos)
        if square is None:
            self.selected_square = None
            self.valid_moves = []
            return None
        
        if self.selected_square is None:
            # Select piece
            piece = board.piece_at(square)
            if piece is not None and piece.color == board.turn:
                self.selected_square = square
                self.valid_moves = [move for move in board.legal_moves if move.from_square == square]
        else:
            # Try to make move
            move = chess.Move(self.selected_square, square)
            # Check for promotion
            if move in board.legal_moves:
                self.selected_square = None
                self.valid_moves = []
                return move
            else:
                # Check if we're selecting a new piece
                piece = board.piece_at(square)
                if piece is not None and piece.color == board.turn:
                    self.selected_square = square
                    self.valid_moves = [move for move in board.legal_moves if move.from_square == square]
                else:
                    self.selected_square = None
                    self.valid_moves = []
        return None
    
    def handle_button_click(self, pos: Tuple[int, int]) -> Optional[str]:
        """Handle clicks on control buttons."""
        for i, button in enumerate(self.control_buttons):
            if button.rect.collidepoint(pos):
                if i == 0:
                    return "new_game"
                elif i == 1:
                    return "undo"
                elif i == 2:
                    return "hint"
                elif i == 3:
                    return "settings"
                elif i == 4:
                    return "main_menu"
        return None
    
    def set_status(self, status: str, thinking: bool = False):
        """Set the game status message."""
        self.game_status = status
        self.thinking = thinking
    
    def set_last_move(self, move: Optional[chess.Move]):
        """Set the last move for highlighting."""
        self.last_move = move 