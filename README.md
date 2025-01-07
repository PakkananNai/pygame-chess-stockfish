# Chess Bot with Pygame and Stockfish

This project is a chess game implemented using Pygame for the graphical interface and Stockfish for the AI opponent. The game allows a human player to play against the Stockfish engine, which is one of the strongest open-source chess engines available.

## Features

- **Graphical Interface**: The game uses Pygame to render the chessboard and pieces.
- **AI Opponent**: The game integrates the Stockfish engine to provide a challenging AI opponent.
- **Move Validation**: The game uses the `chess` library to handle move validation, including special moves like castling, en passant, and pawn promotion.
- **Game End Detection**: The game detects checkmate, stalemate, and draw conditions and displays the appropriate message.
- **Highlighting**: The game highlights the selected piece and possible moves.

## Requirements

- Python 3.6 or higher
- Pygame
- python-chess
- Stockfish chess engine

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/chess-bot.git
    cd chess-bot
    ```

2. **Install the required Python packages**:
    ```sh
    pip install pygame python-chess
    ```

3. **Download and install Stockfish**:
    - Go to the [Stockfish download page](https://stockfishchess.org/download/).
    - Download the appropriate version for your operating system. For Windows, you might download something like `stockfish_15_win_x64_avx2.zip`.
    - Extract the downloaded file to a known location on your computer. For example, you might extract it to `C:\stockfish`.

4. **Update the path to Stockfish in the code**:
    - Open [main.py](http://_vscodecontentref_/0) and update the path to the Stockfish executable:
    ```python
    engine = chess.engine.SimpleEngine.popen_uci("C:/stockfish/stockfish-windows-x86-64-avx2.exe")
    ```

## Running the Game

To run the game, execute the following command:
```sh
python main.py
