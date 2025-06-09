# AmazonQcli-Kids_2048-Game

A colorful, kid-friendly version of the classic 2048 game built with Python and Pygame.

![Kids 2048 Game Screenshot](screenshots/game.png)

## Features

- Kid-friendly interface with bright colors
- Light and dark theme options
- Interactive tutorial for new players
- Score tracking with best score saving
- Responsive UI with proper spacing and alignment

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Pygame 2.5.2 or higher

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/kids-2048.git
   cd kids-2048
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:
   ```bash
   python main.py
   ```

### Using GitHub Codespaces

This repository is fully configured for GitHub Codespaces. To get started:

1. Click the "Code" button on the repository page
2. Select "Open with Codespaces"
3. Click "New codespace"

The game will automatically start when the Codespace is ready. If it doesn't, you can run it manually:

```bash
python main.py
```

## How to Play

- Use arrow keys (Up, Down, Left, Right) to move all tiles in that direction
- When two tiles with the same number touch, they merge into one tile with the sum of their values
- The goal is to create a tile with the number 2048
- The game ends when there are no more valid moves

## Controls

- **Arrow Keys**: Move tiles
- **ESC**: Open/close settings or exit tutorial
- **Mouse**: Click on buttons for various actions

## Project Structure

```
kids_2048/
├── assets/
│   ├── fonts/
│   ├── images/
│   └── sounds/
├── utils/
│   ├── constants.py
│   ├── settings.py
│   └── tutorial.py
├── .devcontainer/
│   ├── devcontainer.json
│   ├── Dockerfile
│   └── docker-compose.yml
├── game.py
├── main.py
├── requirements.txt
└── README.md
```

## Development

### Code Style

This project follows the PEP 8 style guide. We use Black for code formatting and Flake8 for linting.

```bash
# Format code
black .

# Lint code
flake8
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original 2048 game by Gabriele Cirulli
- Pygame community for the excellent game development library
