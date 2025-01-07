import pygame
import chess
import chess.engine

# Set window size and colors
WINDOW_SIZE = 512
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT_COLOR = (186, 202, 68)

pygame_icon = pygame.image.load('images/white_pawn.png')
pygame.display.set_icon(pygame_icon)

# Load chess piece images
def load_images():
    pieces = {}
    pieces["P"] = pygame.image.load("images/white_pawn.png")
    pieces["N"] = pygame.image.load("images/white_knight.png")
    pieces["B"] = pygame.image.load("images/white_bishop.png")
    pieces["R"] = pygame.image.load("images/white_rook.png")
    pieces["Q"] = pygame.image.load("images/white_queen.png")
    pieces["K"] = pygame.image.load("images/white_king.png")
    
    pieces["p"] = pygame.image.load("images/black_pawn.png")
    pieces["n"] = pygame.image.load("images/black_knight.png")
    pieces["b"] = pygame.image.load("images/black_bishop.png")
    pieces["r"] = pygame.image.load("images/black_rook.png")
    pieces["q"] = pygame.image.load("images/black_queen.png")
    pieces["k"] = pygame.image.load("images/black_king.png")
    
    return pieces

# Function to draw the chessboard
def draw_board(screen, selected_square=None, legal_moves=[]):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    if selected_square is not None:
        row = 7 - chess.square_rank(selected_square)
        col = chess.square_file(selected_square)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    for move in legal_moves:
        row = 7 - chess.square_rank(move.to_square)
        col = chess.square_file(move.to_square)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to draw chess pieces on the board
def draw_pieces(screen, board, piece_images):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - chess.square_rank(square)
            col = chess.square_file(square)
            piece_image = piece_images[piece.symbol()]
            screen.blit(piece_image, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to convert chessboard position to game position
def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    x, y = mouse_pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    square = chess.square(col, 7 - row)
    return square

# Function to display text
def draw_text(screen, text, size, color, position):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Main function to run the game
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption('CHESS GAME')
    
    # Initialize the mixer for sound
    pygame.mixer.init()
    move_sound = pygame.mixer.Sound("soundtrack/move-self.mp3")
    capture_sound = pygame.mixer.Sound("soundtrack/capture.mp3")
    
    board = chess.Board()  # Chessboard
    clock = pygame.time.Clock()
    piece_images = load_images()  # Load chess piece images
    selected_square = None
    running = True
    game_over = False
    result_text = ""
    
    # Initialize the chess engine
    engine = chess.engine.SimpleEngine.popen_uci("C:/stockfish/stockfish-windows-x86-64-avx2.exe")
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # When clicking on a chess square
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                square = get_square_under_mouse()
                
                if selected_square is None:
                    # Select piece
                    if board.piece_at(square):
                        selected_square = square
                else:
                    # Move piece
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        if board.is_capture(move):
                            capture_sound.play()  # Play capture sound
                        else:
                            move_sound.play()  # Play move sound
                        board.push(move)
                        selected_square = None
                        
                        # Check game status
                        if board.is_checkmate():
                            game_over = True
                            result_text = "Checkmate! " + ("White wins!" if board.turn == chess.BLACK else "Black wins!")
                        elif board.is_stalemate():
                            game_over = True
                            result_text = "Stalemate!"
                        elif board.is_insufficient_material():
                            game_over = True
                            result_text = "Draw! Insufficient material!"
                        elif board.is_seventyfive_moves():
                            game_over = True
                            result_text = "Draw! 75-move rule!"
                        elif board.is_fivefold_repetition():
                            game_over = True
                            result_text = "Draw! Fivefold repetition!"
                        elif board.is_variant_draw():
                            game_over = True
                            result_text = "Draw!"
                        else:
                            # AI move
                            result = engine.play(board, chess.engine.Limit(time=2.0))
                            if board.is_capture(result.move):
                                capture_sound.play()  # Play capture sound for AI move
                            else:
                                move_sound.play()  # Play move sound for AI move
                            board.push(result.move)
                            
                            # Check game status after AI move
                            if board.is_checkmate():
                                game_over = True
                                result_text = "Checkmate! " + ("White wins!" if board.turn == chess.BLACK else "Black wins!")
                            elif board.is_stalemate():
                                game_over = True
                                result_text = "Stalemate!"
                            elif board.is_insufficient_material():
                                game_over = True
                                result_text = "Draw! Insufficient material!"
                            elif board.is_seventyfive_moves():
                                game_over = True
                                result_text = "Draw! 75-move rule!"
                            elif board.is_fivefold_repetition():
                                game_over = True
                                result_text = "Draw! Fivefold repetition!"
                            elif board.is_variant_draw():
                                game_over = True
                                result_text = "Draw!"
                    else:
                        selected_square = None
        
        # Draw chessboard
        legal_moves = [move for move in board.legal_moves if move.from_square == selected_square] if selected_square is not None else []
        draw_board(screen, selected_square, legal_moves)
        
        # Draw chess pieces on the board
        draw_pieces(screen, board, piece_images)
        
        # Display text when the game is over
        if game_over:
            draw_text(screen, result_text, 36, (255, 0, 0), (WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 - 20))
        
        # Update the screen
        pygame.display.flip()
        clock.tick(60)

    engine.quit()
    pygame.quit()

if __name__ == "__main__":
    main()
