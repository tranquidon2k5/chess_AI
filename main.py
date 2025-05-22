import pygame
from game.game import ChessGame

def main():
    # Initialize pygame
    pygame.init()
    
    # Create and run the game
    game = ChessGame()
    game.run()

if __name__ == "__main__":
    main() 