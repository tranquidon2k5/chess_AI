import chess
import chess.engine
import time
from ai.minimax import MinimaxAI # Đảm bảo đường dẫn này chính xác

# --- Cấu hình --- 
STOCKFISH_PATH = "stockfish-windows-x86-64-avx2.exe" # Đường dẫn tới file Stockfish
MINIMAX_BOT_DEPTH = 5  # Độ sâu tìm kiếm cho Minimax Bot của bạn

# Các mức Elo của Stockfish để thi đấu
# Bạn có thể thay đổi hoặc thêm các mức Elo khác vào danh sách này
STOCKFISH_ELO_LEVELS_TO_TEST = [1000, 1300, 1500, 1800, 2000]

STOCKFISH_MOVE_THINK_TIME = 0.2  # Thời gian (giây) Stockfish suy nghĩ cho mỗi nước đi
                               # Tăng thời gian này có thể làm Stockfish mạnh hơn một chút ở Elo thấp

def initialize_stockfish_engine(elo: int) -> chess.engine.SimpleEngine:
    """Khởi tạo một instance của Stockfish engine với Elo được chỉ định."""
    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        # Đặt giới hạn sức mạnh cho Stockfish
        engine.configure({"UCI_LimitStrength": True, "UCI_Elo": elo})
        # Một số engine có thể cần "isready" hoặc "ucinewgame" sau khi configure
        # nhưng với SimpleEngine và cấu hình trực tiếp thường là đủ.
        # print(f"Stockfish engine initialized and configured to Elo: {elo}")
        return engine
    except Exception as e:
        print(f"Lỗi khi khởi tạo Stockfish ở Elo {elo}: {e}")
        # Tùy chọn: có thể throw lỗi ở đây để dừng nếu Stockfish không khởi tạo được
        # raise
        return None # Hoặc trả về None để bỏ qua match này

def play_match(minimax_ai: MinimaxAI, stockfish_engine: chess.engine.SimpleEngine,
               stockfish_elo: int, bot_plays_as_color: chess.Color):
    """Thi đấu một ván cờ giữa Minimax AI và Stockfish."""
    board = chess.Board()
    game_turn_counter = 0

    bot_player_name = f"Minimax Bot (Depth {minimax_ai.max_depth})"
    stockfish_player_name = f"Stockfish (Elo {stockfish_elo})"

    bot_color_str = "Trắng" if bot_plays_as_color == chess.WHITE else "Đen"
    stockfish_color_str = "Đen" if bot_plays_as_color == chess.WHITE else "Trắng"

    print(f"\n--- Ván mới: {bot_player_name} ({bot_color_str}) vs {stockfish_player_name} ({stockfish_color_str}) ---")

    while not board.is_game_over():
        game_turn_counter += 1
        current_player_color_str = "Trắng" if board.turn == chess.WHITE else "Đen"
        print(f"\nLượt {game_turn_counter} ({current_player_color_str} đi)")
        print(board)
        print("-" * 30)

        chosen_move = None
        if board.turn == bot_plays_as_color:
            print(f"{bot_player_name} đang suy nghĩ...")
            # MinimaxAI.find_best_move sẽ tự động cập nhật ai_color dựa trên board.turn
            # và cũng in ra số node đã duyệt.
            chosen_move = minimax_ai.find_best_move(board)
            if chosen_move:
                print(f"{bot_player_name} đi: {chosen_move.uci()}")
        else:
            print(f"{stockfish_player_name} đang suy nghĩ...")
            try:
                result = stockfish_engine.play(board, chess.engine.Limit(time=STOCKFISH_MOVE_THINK_TIME))
                chosen_move = result.move
                if chosen_move:
                    print(f"{stockfish_player_name} đi: {chosen_move.uci()}")
            except chess.engine.EngineTerminatedError:
                print(f"Lỗi: Stockfish engine đã bị tắt đột ngột.")
                break # Kết thúc ván nếu engine lỗi
            except Exception as e:
                print(f"Lỗi từ Stockfish trong khi chơi: {e}")
                break 

        if chosen_move:
            board.push(chosen_move)
        else:
            print("Không có nước đi nào được thực hiện, kết thúc ván đấu (lỗi hoặc game over)." )
            break
        
        time.sleep(0.05) # Delay nhỏ để dễ theo dõi output

    print("\n--- Kết thúc ván đấu ---")
    print(board) # In bàn cờ cuối cùng
    game_outcome = board.outcome()
    if game_outcome:
        print(f"Kết quả: {game_outcome.result()} ({game_outcome.termination.name})")
        # Xác định người thắng dựa trên màu của bot và kết quả
        if game_outcome.winner == bot_plays_as_color:
            print(f"===> {bot_player_name} THẮNG! <===")
        elif game_outcome.winner is not None: # Stockfish thắng
            print(f"===> {stockfish_player_name} THẮNG! <===")
        else: # Hòa
            print(f"===> Ván đấu HÒA! <===")

    else:
        # Trường hợp này ít khi xảy ra nếu board.is_game_over() là true
        print(f"Kết quả: {board.result()} (Không rõ lý do kết thúc)")
    
    # Quan trọng: đóng engine Stockfish sau mỗi ván để giải phóng tài nguyên
    if stockfish_engine:
        stockfish_engine.quit()

def main():
    print("♔ Chess AI Master - Bot vs Stockfish (Thi đấu theo Elo) ♔")
    print(f"Bot Minimax sẽ sử dụng độ sâu: {MINIMAX_BOT_DEPTH}")
    print(f"Stockfish sẽ có {STOCKFISH_MOVE_THINK_TIME}s cho mỗi nước đi.\n")
    
    # Tạo một instance của MinimaxAI. Nó sẽ được tái sử dụng.
    # find_best_move sẽ cập nhật ai_color dựa trên board.turn mỗi khi được gọi.
    minimax_player_instance = MinimaxAI(max_depth=MINIMAX_BOT_DEPTH)

    for elo_level in STOCKFISH_ELO_LEVELS_TO_TEST:
        print(f"\n{'='*40}")
        print(f" Chuẩn bị thi đấu với Stockfish Elo {elo_level}")
        print(f"{'='*40}")
        
        # Bot chơi quân Trắng
        stockfish_engine_for_bot_white = initialize_stockfish_engine(elo_level)
        if stockfish_engine_for_bot_white:
            play_match(minimax_player_instance, stockfish_engine_for_bot_white, elo_level, chess.WHITE)
        else:
            print(f"Bỏ qua ván đấu Bot (Trắng) vs Stockfish Elo {elo_level} do lỗi khởi tạo engine.")

        time.sleep(1) # Dừng một chút giữa các ván

        # Bot chơi quân Đen
        stockfish_engine_for_bot_black = initialize_stockfish_engine(elo_level)
        if stockfish_engine_for_bot_black:
            play_match(minimax_player_instance, stockfish_engine_for_bot_black, elo_level, chess.BLACK)
        else:
            print(f"Bỏ qua ván đấu Bot (Đen) vs Stockfish Elo {elo_level} do lỗi khởi tạo engine.")

    print("\nTất cả các ván đấu đã hoàn thành.")

if __name__ == "__main__":
    main() 