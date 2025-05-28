import chess
import chess.engine
import time

from ai.minimax import MinimaxAI # Assuming MinimaxAI is in ai.minimax
from game.move_generator import evaluate_board # Assuming evaluate_board is in game.move_generator

# --- Configuration ---
STOCKFISH_PATH = "stockfish-windows-x86-64-avx2.exe" # Make sure this is in your project root or provide full path
MINIMAX_DEPTH = 4  # Depth for your Minimax AI
STOCKFISH_THINK_TIME = 0.5  # Seconds for Stockfish to think

# A list of FEN strings for testing
TEST_POSITIONS = {
    "Initial Position": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "Ruy Lopez Opening": "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3",
    "Complex Middlegame": "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
    "Simple Endgame (K+P vs K)": "7k/8/8/8/8/8/P7/K7 w - - 0 1",
    "Queen vs Rook Endgame": "k7/1q6/8/8/8/8/8/K5R1 w - - 0 1",
    "Black to Play Tactical Position": "2r2rk1/pp1b1pp1/1q2pn1p/3p4/3P4/P1NBP3/1P2NPPP/R2Q1RK1 b - - 0 15"
}

def get_minimax_analysis(board: chess.Board, depth: int):
    """Analyzes the position using your Minimax AI."""
    if board.is_game_over():
        return evaluate_board(board, board.turn), None

    # MinimaxAI's find_best_move internally sets ai_color based on board.turn
    ai = MinimaxAI(max_depth=depth) 
    
    # Get evaluation from the current player's perspective
    # Note: MinimaxAI's evaluate_board is used inside find_best_move.
    # For an independent evaluation score comparable to Stockfish, 
    # we call evaluate_board directly.
    current_player_eval = evaluate_board(board, board.turn)
    
    best_move = ai.find_best_move(board) # This also prints nodes evaluated
    
    return current_player_eval, best_move

def get_stockfish_analysis(board: chess.Board, think_time: float):
    """Analyzes the position using Stockfish."""
    try:
        with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
            result = engine.analyse(board, chess.engine.Limit(time=think_time))
            # Score is from the current player's perspective (relative)
            # Mate scores are converted to large centipawn values
            score = result["score"].relative.score(mate_score=100000) 
            pv = result.get("pv")
            best_move = pv[0] if pv else None
            return score, best_move
    except Exception as e:
        print(f"Stockfish Error: {e}")
        return None, None

def main():
    print("♔ Chess AI Master - Minimax vs Stockfish Evaluation ♔")
    print(f"Using Stockfish: {STOCKFISH_PATH}")
    print(f"Minimax Depth: {MINIMAX_DEPTH}")
    print(f"Stockfish Think Time: {STOCKFISH_THINK_TIME}s per position\n")

    for name, fen in TEST_POSITIONS.items():
        print(f"--- Testing Position: {name} ---")
        print(f"FEN: {fen}")
        
        board = chess.Board(fen)
        print(board)
        print(f"Turn: {'White' if board.turn == chess.WHITE else 'Black'}")

        # Minimax Analysis
        print("\nMinimax Analysis:")
        minimax_calc_start_time = time.time()
        # Hàm get_minimax_analysis vẫn được gọi để lấy nước đi của Minimax.
        # Điểm minimax_heuristic_score gốc từ evaluate_board() sẽ không được hiển thị trực tiếp nữa.
        _, minimax_chosen_move = get_minimax_analysis(board.copy(), MINIMAX_DEPTH)
        minimax_calc_time = time.time() - minimax_calc_start_time

        # Đánh giá thế cờ HIỆN TẠI (trước nước đi của Minimax) bằng Stockfish
        # Điểm này sẽ được hiển thị thay cho điểm heuristic của Minimax.
        stockfish_score_of_current_pos, _ = get_stockfish_analysis(board.copy(), STOCKFISH_THINK_TIME)

        if minimax_chosen_move:
            print(f"  Best Move (chosen by Minimax): {minimax_chosen_move.uci()}")
            if stockfish_score_of_current_pos is not None:
                print(f"  Stockfish Score (of this pos, cp): {stockfish_score_of_current_pos}")
            else:
                print(f"  Stockfish Score (of this pos, cp): N/A (Stockfish error)")
        else:
            # Nếu Minimax không tìm thấy nước đi (game over), hiển thị đánh giá của Stockfish cho thế cờ cuối cùng này.
            print("  No move found by Minimax (game is over).")
            if stockfish_score_of_current_pos is not None:
                print(f"  Stockfish Score (of terminal pos, cp): {stockfish_score_of_current_pos}")
            else:
                print(f"  Stockfish Score (of terminal pos, cp): N/A (Stockfish error)")
        
        print(f"  Minimax Calculation Time: {minimax_calc_time:.4f}s") # Chỉ tính thời gian Minimax tìm nước đi

        # Stockfish Analysis (phần này giữ nguyên cho mục đích so sánh nước đi Stockfish chọn)
        print("\nStockfish Analysis:")
        stockfish_analysis_start_time = time.time()
        stockfish_score_for_its_section, stockfish_chosen_move = get_stockfish_analysis(board.copy(), STOCKFISH_THINK_TIME)
        stockfish_analysis_time = time.time() - stockfish_analysis_start_time
        if stockfish_chosen_move:
            print(f"  Best Move (chosen by Stockfish): {stockfish_chosen_move.uci()}")
            print(f"  Stockfish Score (cp, from current player): {stockfish_score_for_its_section}")
        elif stockfish_score_for_its_section is not None: 
             print(f"  Score (cp, from current player): {stockfish_score_for_its_section}")
             print(f"  No best move suggested by Stockfish (likely game over or drawn position).")
        else:
            print("  Stockfish-only analysis failed.")
        print(f"  Stockfish Analysis Time: {stockfish_analysis_time:.4f}s")
        
        print("-" * 40 + "\n")

if __name__ == "__main__":
    main() 