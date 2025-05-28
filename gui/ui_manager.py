import pygame
import chess
from typing import Optional, List, Callable, Dict, Any
from enum import Enum
import json
import os

class GameMode(Enum):
    MENU = "menu"
    PLAY_VS_AI = "play_vs_ai"
    PLAY_VS_PLAYER = "play_vs_player"
    AI_VS_AI = "ai_vs_ai"
    SETTINGS = "settings"
    GAME = "game"

class AIDifficulty(Enum):
    EASY = ("Easy",1)
    MEDIUM = ("Medium", 2)
    HARD = ("Hard", 3)
    EXPERT = ("Expert", 4)

class UIButton:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 color: tuple = (52, 152, 219), hover_color: tuple = (74, 144, 226),
                 text_color: tuple = (255, 255, 255), font_size: int = 24,
                 action: Optional[Callable] = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.action = action
        self.hovered = False
        self.font = pygame.font.Font(None, font_size)
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()
                return True
        return False
    
    def draw(self, screen: pygame.Surface):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class UIManager:
    def __init__(self, width: int = 1200, height: int = 800):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("♔ Chess AI Master ♔")
        
        # Colors based on the provided design
        self.bg_color = (45, 52, 54)  # Dark background
        self.primary_color = (52, 152, 219)  # Blue
        self.secondary_color = (74, 144, 226)  # Lighter blue
        self.accent_color = (230, 126, 34)  # Orange
        self.text_color = (255, 255, 255)  # White
        self.gray_color = (99, 110, 114)  # Gray
        
        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.button_font = pygame.font.Font(None, 28)
        
        # Game state
        self.current_mode = GameMode.MENU
        self.settings = self._load_settings()
        
        # UI elements
        self.buttons: Dict[str, List[UIButton]] = {}
        self._create_ui_elements()
        
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file or create default settings."""
        default_settings = {
            "ai_difficulty": AIDifficulty.HARD,
            "player_color": chess.WHITE,
            "ai_color": chess.BLACK,
            "sound_enabled": True,
            "animations_enabled": True
        }
        
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    loaded_settings = json.load(f)
                    # Convert string difficulty back to enum
                    if "ai_difficulty" in loaded_settings:
                        difficulty_name = loaded_settings["ai_difficulty"]
                        for diff in AIDifficulty:
                            if diff.name == difficulty_name:
                                loaded_settings["ai_difficulty"] = diff
                                break
                    default_settings.update(loaded_settings)
        except Exception as e:
            print(f"Could not load settings: {e}")
        
        return default_settings
    
    def _save_settings(self):
        """Save current settings to file."""
        try:
            settings_to_save = self.settings.copy()
            # Convert enum to string for JSON serialization
            settings_to_save["ai_difficulty"] = self.settings["ai_difficulty"].name
            with open("settings.json", "w") as f:
                json.dump(settings_to_save, f, indent=2)
        except Exception as e:
            print(f"Could not save settings: {e}")
    
    def _create_ui_elements(self):
        """Create all UI elements for different screens."""
        center_x = self.width // 2
        
        # Main Menu buttons
        self.buttons[GameMode.MENU.value] = [
            UIButton(center_x - 150, 300, 300, 60, "Play vs AI", 
                    action=lambda: self.set_mode(GameMode.PLAY_VS_AI)),
            UIButton(center_x - 150, 380, 300, 60, "Play vs Player", 
                    action=lambda: self.set_mode(GameMode.PLAY_VS_PLAYER)),
            UIButton(center_x - 150, 460, 300, 60, "AI vs AI", 
                    action=lambda: self.set_mode(GameMode.AI_VS_AI)),
            UIButton(center_x - 150, 540, 300, 60, "Settings", 
                    action=lambda: self.set_mode(GameMode.SETTINGS))
        ]
        
        # Settings buttons
        self.buttons[GameMode.SETTINGS.value] = [
            # AI Difficulty buttons
            UIButton(200, 250, 120, 50, "Easy", 
                    color=self.gray_color if self.settings["ai_difficulty"] != AIDifficulty.EASY else self.accent_color,
                    action=lambda: self.set_ai_difficulty(AIDifficulty.EASY)),
            UIButton(340, 250, 120, 50, "Medium", 
                    color=self.gray_color if self.settings["ai_difficulty"] != AIDifficulty.MEDIUM else self.accent_color,
                    action=lambda: self.set_ai_difficulty(AIDifficulty.MEDIUM)),
            UIButton(480, 250, 120, 50, "Hard", 
                    color=self.gray_color if self.settings["ai_difficulty"] != AIDifficulty.HARD else self.accent_color,
                    action=lambda: self.set_ai_difficulty(AIDifficulty.HARD)),
            UIButton(620, 250, 120, 50, "Expert", 
                    color=self.gray_color if self.settings["ai_difficulty"] != AIDifficulty.EXPERT else self.accent_color,
                    action=lambda: self.set_ai_difficulty(AIDifficulty.EXPERT)),
            
            # Choose side buttons
            UIButton(200, 380, 150, 50, "Play White", 
                    color=self.primary_color if self.settings["player_color"] == chess.WHITE else self.gray_color,
                    action=lambda: self.set_player_color(chess.WHITE)),
            UIButton(370, 380, 150, 50, "Play Black", 
                    color=self.gray_color if self.settings["player_color"] == chess.WHITE else self.primary_color,
                    action=lambda: self.set_player_color(chess.BLACK)),
            
            # Back button
            UIButton(center_x - 150, 600, 300, 60, "Back", 
                    action=lambda: self.set_mode(GameMode.MENU))
        ]
    
    def set_mode(self, mode: GameMode):
        """Change the current UI mode."""
        self.current_mode = mode
        if mode == GameMode.SETTINGS:
            self._update_settings_buttons()
    
    def set_ai_difficulty(self, difficulty: AIDifficulty):
        """Set AI difficulty and update UI."""
        self.settings["ai_difficulty"] = difficulty
        self._save_settings()
        self._update_settings_buttons()
    
    def set_player_color(self, color: chess.Color):
        """Set player color and update AI color accordingly."""
        self.settings["player_color"] = color
        self.settings["ai_color"] = not color
        self._save_settings()
        self._update_settings_buttons()
    
    def _update_settings_buttons(self):
        """Update settings buttons appearance based on current settings."""
        settings_buttons = self.buttons[GameMode.SETTINGS.value]
        
        # Update difficulty buttons
        difficulty_buttons = settings_buttons[0:4]
        for i, difficulty in enumerate(AIDifficulty):
            if i < len(difficulty_buttons):
                if self.settings["ai_difficulty"] == difficulty:
                    difficulty_buttons[i].color = self.accent_color
                else:
                    difficulty_buttons[i].color = self.gray_color
        
        # Update color buttons
        white_button, black_button = settings_buttons[4:6]
        if self.settings["player_color"] == chess.WHITE:
            white_button.color = self.primary_color
            black_button.color = self.gray_color
        else:
            white_button.color = self.gray_color
            black_button.color = self.primary_color
    
    def handle_event(self, event: pygame.event.Event) -> Optional[GameMode]:
        """Handle UI events and return mode change if any."""
        current_buttons = self.buttons.get(self.current_mode.value, [])
        
        for button in current_buttons:
            if button.handle_event(event):
                return self.current_mode
        
        # Handle keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.current_mode == GameMode.SETTINGS:
                    self.set_mode(GameMode.MENU)
                elif self.current_mode == GameMode.MENU:
                    return None  # Exit game
        
        return self.current_mode
    
    def draw_main_menu(self):
        """Draw the main menu screen."""
        self.screen.fill(self.bg_color)
        
        # Title
        title_text = self.title_font.render("Chess AI Master", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.subtitle_font.render("Experience the Art of Chess", True, self.gray_color)
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw buttons
        for button in self.buttons[GameMode.MENU.value]:
            button.draw(self.screen)
    
    def draw_settings(self):
        """Draw the settings screen."""
        self.screen.fill(self.bg_color)
        
        # Title
        title_text = self.title_font.render("Settings", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # AI Difficulty section
        diff_title = self.subtitle_font.render("AI Difficulty", True, self.text_color)
        self.screen.blit(diff_title, (200, 200))
        
        # Choose Your Side section
        side_title = self.subtitle_font.render("Choose Your Side", True, self.text_color)
        self.screen.blit(side_title, (200, 330))
        
        # Draw buttons
        for button in self.buttons[GameMode.SETTINGS.value]:
            button.draw(self.screen)
    
    def draw(self):
        """Draw the current screen."""
        if self.current_mode == GameMode.MENU:
            self.draw_main_menu()
        elif self.current_mode == GameMode.SETTINGS:
            self.draw_settings()
        # Add other modes as needed
        
        pygame.display.flip()
    
    def get_current_mode(self) -> GameMode:
        """Get the current UI mode."""
        return self.current_mode
    
    def get_settings(self) -> Dict[str, Any]:
        """Get current settings."""
        return self.settings.copy() 