# Wumpus World Game

This project is a grid-based game developed in Python using the Pygame library. The game involves a player navigating through a grid filled with monsters, pits, and gold.

## Key Features

1. **File Dialog**: The Tkinter library is used to create a file dialog for selecting game files.

2. **Game Elements**: The game includes several elements such as a player, monsters, pits, and gold. Each of these elements is represented by a class that is a subclass of `pygame.sprite.Sprite`.

3. **Game Map**: The game map is represented by the `Map` class. This class includes methods for updating the map and reading it from a file.

4. **Player's Agent**: The player's agent is represented by the `Agent` class. This class includes properties for the agent's location, whether it's alive or not, and its score.

5. **Game Loop**: The game loop is implemented in the `main` function, where Pygame events are handled, the game state is updated, and the game window is redrawn.

6. **Player Movement and Arrow Firing**: The game includes functionality for handling the movement of the player's agent and the firing of arrows.

## Code Structure

The project is divided into several Python files, each containing classes and functions related to a specific aspect of the game:

- `main.py`: Contains the main game loop and initialization code.

- `Map.py`: Contains the `Map` class for representing the game map.

- `Object.py`: Contains the `Cell`, `Object`, `Wumpus`, and `Arrow` classes for representing different game elements.

- `Player.py`: Contains the `Player` class for representing the player's agent.

## How to Run

To run the game, execute the `main.py` file. A file dialog will appear for you to select the game file. After selecting the file, the game window will appear and you can start playing.

