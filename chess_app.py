import pygame
import chess
from typing import Optional, Dict, Any
import sys
import threading
import time

from gui.ui_manager import UIManager, GameMode, AIDifficulty
from gui.game_gui import GameGUI
from game.board import ChessBoard
from ai.minimax import MinimaxAI

class ChessApp:
    def __init__(self):
        pygame.init()
        
        # Initialize managers
        self.ui_manager = UIManager()
        self.game_gui = None
        
        # Game state
        self.board = None
        self.ai_white = None
        self.ai_black = None
        self.current_game_mode = None
        self.game_running = False
        self.ai_thinking = False
        
        # Settings
        self.settings = self.ui_manager.get_settings()
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        self.running = True
        
    def start_new_game(self, mode: GameMode):
        """Start a new game with the specified mode."""
        self.current_game_mode = mode
        self.board = ChessBoard()
        self.game_gui = GameGUI()
        self.game_running = True
        self.ai_thinking = False
        
        # Initialize AI based on mode and settings
        ai_depth = self.settings["ai_difficulty"].value[1]
        
        if mode == GameMode.PLAY_VS_AI:
            if self.settings["player_color"] == chess.WHITE:
                # Player is white, AI is black
                self.ai_white = None
                self.ai_black = MinimaxAI(max_depth=ai_depth, ai_color=chess.BLACK)
            else:
                # Player is black, AI is white
                self.ai_white = MinimaxAI(max_depth=ai_depth, ai_color=chess.WHITE)
                self.ai_black = None
        elif mode == GameMode.AI_VS_AI:
            # Both sides are AI
            self.ai_white = MinimaxAI(max_depth=ai_depth, ai_color=chess.WHITE)
            self.ai_black = MinimaxAI(max_depth=ai_depth, ai_color=chess.BLACK)
        else:  # PLAY_VS_PLAYER
            # No AI
            self.ai_white = None
            self.ai_black = None
        
        # Set initial status
        if mode == GameMode.PLAY_VS_AI:
            if self.is_ai_turn():
                self.game_gui.set_status("AI is thinking...", thinking=True)
                self._start_ai_move()
            else:
                self.game_gui.set_status("Your turn")
        elif mode == GameMode.AI_VS_AI:
            self.game_gui.set_status("AI vs AI - Watching game")
            self._start_ai_move()
        else:
            self.game_gui.set_status("White to move")
        
        # Switch to game mode
        self.ui_manager.set_mode(GameMode.GAME)
    
    def is_ai_turn(self) -> bool:
        """Check if it's the AI's turn."""
        if not self.board:
            return False
        
        current_turn = self.board.board.turn
        if current_turn == chess.WHITE:
            return self.ai_white is not None
        else:
            return self.ai_black is not None
    
    def get_current_ai(self) -> Optional[MinimaxAI]:
        """Get the AI for the current turn."""
        if not self.board:
            return None
        
        current_turn = self.board.board.turn
        if current_turn == chess.WHITE:
            return self.ai_white
        else:
            return self.ai_black
    
    def _start_ai_move(self):
        """Start AI move calculation in a separate thread."""
        if self.ai_thinking or not self.is_ai_turn():
            return
        
        self.ai_thinking = True
        ai = self.get_current_ai()
        if ai:
            # Start AI calculation in background thread
            thread = threading.Thread(target=self._calculate_ai_move, args=(ai,))
            thread.daemon = True
            thread.start()
    
    def _calculate_ai_move(self, ai: MinimaxAI):
        """Calculate AI move in background thread."""
        try:
            move = ai.find_best_move(self.board.board)
            if move and self.game_running:
                # Schedule move to be applied in main thread
                self._pending_ai_move = move
        except Exception as e:
            print(f"AI calculation error: {e}")
        finally:
            self.ai_thinking = False
    
    def _apply_pending_ai_move(self):
        """Apply pending AI move if available."""
        if hasattr(self, '_pending_ai_move') and self._pending_ai_move:
            move = self._pending_ai_move
            self._pending_ai_move = None
            
            # Apply the move
            self.board.make_move(move)
            self.game_gui.set_last_move(move)
            
            # Update status
            if self.board.is_game_over():
                result = self.game_gui.get_game_result(self.board.board)
                self.game_gui.set_status(f"Game Over: {result}")
                self.game_running = False
            elif self.current_game_mode == GameMode.AI_VS_AI:
                # Continue with next AI move
                self._start_ai_move()
            elif self.is_ai_turn():
                self.game_gui.set_status("AI is thinking...", thinking=True)
                self._start_ai_move()
            else:
                self.game_gui.set_status("Your turn")
    
    def handle_game_click(self, pos):
        """Handle clicks during game mode."""
        if not self.game_gui or not self.board:
            return
        
        # Check for button clicks first
        button_action = self.game_gui.handle_button_click(pos)
        if button_action:
            self._handle_game_action(button_action)
            return
        
        # Handle board clicks only if it's human's turn and game is running
        if (self.game_running and not self.ai_thinking and 
            (not self.is_ai_turn() or self.current_game_mode == GameMode.PLAY_VS_PLAYER)):
            
            move = self.game_gui.handle_board_click(pos, self.board.board)
            if move:
                # Human made a move
                self.board.make_move(move)
                self.game_gui.set_last_move(move)
                
                # Update status
                if self.board.is_game_over():
                    result = self.game_gui.get_game_result(self.board.board)
                    self.game_gui.set_status(f"Game Over: {result}")
                    self.game_running = False
                elif self.is_ai_turn():
                    self.game_gui.set_status("AI is thinking...", thinking=True)
                    self._start_ai_move()
                else:
                    # Next human turn or vs player mode
                    turn_color = "White" if self.board.board.turn == chess.WHITE else "Black"
                    self.game_gui.set_status(f"{turn_color} to move")
    
    def _handle_game_action(self, action: str):
        """Handle game control actions."""
        if action == "new_game":
            if self.current_game_mode:
                self.start_new_game(self.current_game_mode)
        elif action == "undo":
            if self.board and self.board.board.move_stack:
                # Undo last move(s)
                if self.current_game_mode == GameMode.PLAY_VS_AI:
                    # Undo both player and AI moves
                    if len(self.board.board.move_stack) >= 2:
                        self.board.board.pop()  # Undo AI move
                        self.board.board.pop()  # Undo player move
                    elif len(self.board.board.move_stack) == 1:
                        self.board.board.pop()  # Undo single move
                else:
                    # Just undo last move
                    self.board.board.pop()
                
                # Update last move highlight
                if self.board.board.move_stack:
                    self.game_gui.set_last_move(self.board.board.move_stack[-1])
                else:
                    self.game_gui.set_last_move(None)
                
                # Update status
                if self.is_ai_turn() and self.current_game_mode != GameMode.PLAY_VS_PLAYER:
                    self.game_gui.set_status("AI is thinking...", thinking=True)
                    self._start_ai_move()
                else:
                    turn_color = "White" if self.board.board.turn == chess.WHITE else "Black"
                    self.game_gui.set_status(f"{turn_color} to move")
        elif action == "hint":
            if (self.board and not self.ai_thinking and 
                not self.is_ai_turn() and self.current_game_mode == GameMode.PLAY_VS_AI):
                # Get hint from AI
                ai_depth = max(2, self.settings["ai_difficulty"].value[1] - 1)
                hint_ai = MinimaxAI(max_depth=ai_depth, ai_color=self.board.board.turn)
                hint_move = hint_ai.find_best_move(self.board.board)
                if hint_move:
                    self.game_gui.set_status(f"Hint: {hint_move}")
        elif action == "settings":
            self.ui_manager.set_mode(GameMode.SETTINGS)
        elif action == "main_menu":
            self.ui_manager.set_mode(GameMode.MENU)
            self.game_running = False
    
    def handle_events(self):
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            current_mode = self.ui_manager.get_current_mode()
            
            if current_mode == GameMode.GAME:
                # Game mode - handle game-specific events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_game_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.ui_manager.set_mode(GameMode.MENU)
                        self.game_running = False
                    elif event.key == pygame.K_n:
                        if self.current_game_mode:
                            self.start_new_game(self.current_game_mode)
                    elif event.key == pygame.K_u:
                        self._handle_game_action("undo")
                    elif event.key == pygame.K_h:
                        self._handle_game_action("hint")
            else:
                # Menu/Settings mode - handle UI events
                result = self.ui_manager.handle_event(event)
                if result is None:
                    self.running = False
                elif result == GameMode.PLAY_VS_AI:
                    self.start_new_game(GameMode.PLAY_VS_AI)
                elif result == GameMode.PLAY_VS_PLAYER:
                    self.start_new_game(GameMode.PLAY_VS_PLAYER)
                elif result == GameMode.AI_VS_AI:
                    self.start_new_game(GameMode.AI_VS_AI)
    
    def update(self):
        """Update game state."""
        # Apply pending AI moves
        if hasattr(self, '_pending_ai_move'):
            self._apply_pending_ai_move()
        
        # Update settings
        self.settings = self.ui_manager.get_settings()
    
    def draw(self):
        """Draw the current screen."""
        current_mode = self.ui_manager.get_current_mode()
        
        if current_mode == GameMode.GAME and self.game_gui and self.board:
            # Draw game screen
            mode_name = {
                GameMode.PLAY_VS_AI: "vs AI",
                GameMode.PLAY_VS_PLAYER: "vs Player", 
                GameMode.AI_VS_AI: "AI vs AI"
            }.get(self.current_game_mode, "Game")
            
            difficulty_name = self.settings["ai_difficulty"].value[0]
            
            self.game_gui.draw(
                self.board.board,
                game_mode=mode_name,
                ai_difficulty=difficulty_name
            )
        else:
            # Draw UI screens
            self.ui_manager.draw()
    
    def run(self):
        """Main game loop."""
        print("♔ Chess AI Master ♔")
        print("Welcome to Chess AI Master!")
        print("Use the menu to select game mode or press ESC to exit.")
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

def main():
    """Main entry point."""
    app = ChessApp()
    app.run()

if __name__ == "__main__":
    main() 