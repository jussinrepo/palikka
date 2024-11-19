# PALIKKA

Palikka is a classic puzzle. The game was created in collaboration between a human developer and Claude 3.5 Sonnet, an AI language model by Anthropic.

![image](https://github.com/user-attachments/assets/94ca8b48-4f84-4b84-80ee-45b0dc7de82b)

## Description

Palikka (Finnish for "block") is a falling-block puzzle game where players stack colored blocks in columns. The game combines mechanics from classic games like Columns and Tetris, but with its own unique gameplay elements. Heh... actually this game is exactly like Columns, the game I loved to play as a kid. But for some reason Claude decided to write those previous sentences that way ;D

### Features

- Three-block vertical pieces with different colors
- Match three or more same-colored blocks horizontally, vertically, or diagonally
- Combo system for chain reactions
- Progressive difficulty with speed increase between levels
- Extra colors for extra challenge
- Optional starting debris for extra extra challenge
- Colorful block graphics and soothing backgrounds
- Score tracking and level progression
- Graceful piece placement system

## How to Play

- Use LEFT and RIGHT arrow keys to move the falling piece
- UP arrow key rotates the colors in the piece
- DOWN arrow key accelerates the fall
- P key pauses the game
- C key toggles block styles
- B key toggles background style
- ESC key returns to menu

### Scoring

- Basic matches: 3 points
- Four blocks matched: 5 points
- Larger matches: 10+ points
- Combos multiply your score
- Level increases every 100 points

## Installation

1. Ensure you have Python 3.x installed
2. Install Pygame:
```bash
pip install pygame
```
3. Clone this repository
4. Run the game:
```bash
python palikka.py
```

## Development Story

Palikka was developed through an interesting collaboration between a human developer and Claude 3.5 Sonnet. The initial concept came from wanting to recreate the beloved classic from my the authors childhood: Coloris/Columns. Claude assisted with game mechanics implementation, code structure suggestions, and debugging throughout the development process.

The game evolved through multiple iterations, with both human and AI contributing ideas and solutions. This collaborative approach led to interesting features like the combo system and the flexible block/background display options.

## Requirements

- Python 3.x
- Pygame library

## License

MIT License

Copyright (c) 2024 Jussi Sivonen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Credits

- Game Design and Programming: Jussi Sivonen
- AI Collaboration: Claude 3.5 Sonnet (Anthropic)
- PNG Graphics: DALL-E 3 (OpenAI) and Jussi
- Background Images: DALL-E 3 (OpenAI) and Jussi

## Contributing

Feel free to fork this project and submit pull requests with improvements or bug fixes. You can also open issues for bugs or feature requests.
