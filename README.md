# Snake Game

A classic Snake game built with Python and Pygame, playable both on desktop and in the browser via WebAssembly.

## Play Online

Play the game directly in your browser at: `https://<username>.github.io/SnakeGame/`

## How to Play

1. Enter your name on the title screen (or press Space for default name)
2. Press **Space** to start the game
3. Use **Arrow Keys** to control the snake:
   - ↑ Move Up
   - ↓ Move Down
   - ← Move Left
   - → Move Right
4. Eat the red food to grow and score points
5. Avoid hitting the walls or yourself!

## Run Locally

### Prerequisites
- Python 3.8+
- Pygame

### Installation

```bash
pip install -r requirements.txt
python main.py
```

### Test Web Build Locally

```bash
pip install pygbag
pygbag .
```

Then open `http://localhost:8000` in your browser.

## Project Structure

```
SnakeGame/
├── main.py              # Main game entry point
├── src/
│   ├── __init__.py
│   ├── snake.py         # Snake class
│   ├── food.py          # Food class
│   └── gameboard.py     # Gameboard class
├── assets/
│   ├── snakescreen.png  # Title screen image
│   ├── Snakesong.ogg    # Background music (web)
│   └── Snakesong.wav    # Background music (desktop)
└── Highscores.txt       # Local high scores
```

## Credits

Created by Luis Tallavo

## License

This project is open source and available for educational purposes.
