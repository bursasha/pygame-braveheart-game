# Brave Heart Game 🛡️❤️

## Project Structure: 📁
- `game/`: Contains all the game-related files and assets.
    - `audio/`: Holds game audio files.
    - `creatures/`: Logic and attributes for game creatures.
    - `graphics/`: Contains graphical assets.
    - `layouts/`: Contains layout CSV files.
    - `level/`: Manages level-specific logic.
    - `tests/`: Contains test scripts.
    - `ui/`: User interface components.
    - `utils/`: Utility scripts.
    - `weapons/`: Weapon logic and attributes.
    - `main.py`: Main script to run the game.
- `README.md`: This README file providing an overview of the project.
- `burakole.pdf`: Documentation related to the project.
- `requirements.txt`: Lists all the Python dependencies needed to run the game.

## Technology Stack: 🔍
- **Language:** Python
- **Libraries:** Pygame for game development, PyAutoGUI for handling automation and GUI interactions
- **Tools and Techniques:**
    - **Graphics Handling**: Pygame for rendering 2D graphics and managing animations.
    - **Sound Management**: Pygame for playing sound effects and background music.
    - **Collision Detection**: Pygame's built-in functions for handling collisions between game objects.
    - **Event Handling**: Pygame for managing user inputs and game events.
    - **Game Loop**: Core loop to keep the game running and updating.
    - **Automation**: PyAutoGUI for automating tasks within the game.

## What is it capable of? 🚀
Brave Heart is a 2D game featuring various mechanics such as:
- **Character Movement**: Smooth and responsive controls for the player.
- **Enemy AI**: Enemies with basic artificial intelligence.
- **Level Progression**: Multiple levels with increasing difficulty.
- **Interactive Elements**: Collectibles, obstacles, and power-ups.
- **User Interface**: Menus, HUDs, and in-game notifications.
- **Sound Effects**: Background music and sound effects to enhance gameplay.
- **Automation**: Using PyAutoGUI to automate certain game actions for testing purposes.

## About the Project: 📜
Brave Heart is a 2D game developed using Python, Pygame, and PyAutoGUI. The game features various levels, character interactions, and a detailed user interface. The project showcases skills in game development, including game logic, asset management, and user interface design.

## Concepts Implemented: 📗
### Game Mechanics 🕹️
- **Player Controls**: Implementing smooth and responsive controls for the player character.
- **Enemy Behavior**: Designing basic AI for enemy characters.
- **Collision Detection**: Managing interactions between game objects.

### Asset Management 🎨
- **Image Handling**: Loading and displaying game sprites.
- **Sound Management**: Incorporating background music and sound effects.

### Game Design 🛠️
- **Level Design**: Creating engaging and challenging levels.
- **UI Design**: Designing intuitive menus and HUDs for better user experience.

## How to Run the Game: 🕹️
My game can be run on any Linux distribution or macOS system. To start, you need to go to the **game/** folder, since the program modules are looking for a relative path from this directory. After that, use the command to run **main.py**.

```bash
cd game
python3 main.py
```
