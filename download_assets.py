import os
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO

def download_chess_pieces():
    # Create assets directory if it doesn't exist
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    # Base URL for chess piece images
    base_url = "https://images.chesscomfiles.com/chess-themes/pieces/neo/150/"
    
    # Piece types and colors
    pieces = {
        'p': 'p',
        'n': 'n',
        'b': 'b',
        'r': 'r',
        'q': 'q',
        'k': 'k'
    }
    colors = {
        'w': 'w',
        'b': 'b'
    }
    
    # Download each piece
    for color_code in colors:
        for piece_code in pieces:
            filename = f"{color_code}{piece_code}.png"
            url = f"{base_url}{color_code}{piece_code}.png"
            
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    filepath = assets_dir / filename
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded {filename}")
                else:
                    print(f"Failed to download {filename}")
            except Exception as e:
                print(f"Error downloading {filename}: {e}")

if __name__ == "__main__":
    download_chess_pieces() 