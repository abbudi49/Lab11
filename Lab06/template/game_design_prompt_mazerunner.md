# Prompt for Generating a Maze Runner Game

## 1. Objective

Create a complete, single-file Python application for a simple **Maze Runner** game using the **Pygame** library. The game should be easy to run and control, featuring a clean and visually appealing interface.

## 2. Core Gameplay Mechanics

*   **Game World / Environment:**
    *   The game is played on a grid-based maze.
    *   Window dimensions: **600x600 pixels**.
    *   Grid size: **30x30 pixels per cell** (20x20 grid).
    *   The maze layout can be predefined or randomly generated.

*   **Player Character:**
    *   The player is represented as a **colored circle or square** (25x25 pixels).
    *   Starting position: **Top-left corner** of the maze (or designated start cell).
    *   Movement controls: **WASD** or **Arrow Keys** (up, down, left, right).
    *   The player can only move to adjacent cells that are not walls.
    *   Movement is grid-based (snaps to cells).

*   **Maze Structure:**
    *   The maze consists of **walls** (impassable) and **paths** (passable).
    *   Walls are represented as solid blocks.
    *   Paths are empty spaces.
    *   Include a **goal/exit** location (e.g., bottom-right corner).

*   **Collectibles (Optional Enhancement):**
    *   Place **3-5 collectible items** (coins, stars) throughout the maze.
    *   The player can collect items by moving over them.
    *   Collecting all items before reaching the goal can give bonus points.

*   **Scoring / Progression:**
    *   Starting score: **0**.
    *   Reaching the goal: **+100 points**.
    *   Each collectible: **+10 points**.
    *   Optional: Track time taken and give bonus for fast completion.

*   **Win / Loss Conditions:**
    *   **Win:** The player reaches the goal/exit cell. Display "YOU WIN!" message.
    *   There is no explicit loss condition; the player can retry until they succeed.

*   **Game Flow:**
    *   Can restart the game by pressing the **'R' key**.
    *   Can optionally generate a new random maze on restart.

## 3. GUI (Graphical User Interface)

*   **Art Style & Graphics:**
    *   Simple, clean, 2D top-down graphics.
    *   Player appearance: **Blue circle or square**.
    *   Walls: **Gray or brown solid blocks**.
    *   Path: **Light gray or white background**.
    *   Goal/Exit: **Green square or flag symbol**.
    *   Collectibles: **Yellow circles (coins) or stars**.

*   **User Interface (UI):**
    *   Display the current score in the **top-left corner**.
    *   Display collectibles remaining or collected in the **top-right corner** (e.g., "Coins: 3/5").
    *   Optional: Display a timer showing elapsed time.

*   **Sound & Music:**
    *   No sound required.

## 4. Code Structure and Implementation

*   **Language and Library:**
    *   Use Python 3.
    *   Use the **`pygame`** library.

*   **Structure:**
    *   Organize the code within a **`MazeRunnerGame`** class to encapsulate all game-related logic and data.
    *   Use constants for key game parameters (window dimensions, colors, grid size, cell size, etc.).
    *   Represent the maze as a 2D list/array (0 for path, 1 for wall, 2 for collectible, 3 for goal).
    *   Create separate methods for handling user input, updating the game state (player movement, collision detection), and rendering.
    *   Include a main game loop that controls the flow of the game.
    *   The code should be well-commented to explain the logic.

*   **Sample Maze Layout:**
    *   Provide a simple predefined maze as a starting point (can be hardcoded as a 2D list).
    *   For example:
    ```python
    # 1 = wall, 0 = path, 3 = goal, 2 = collectible
    maze = [
        [0, 1, 0, 0, 0, ...],
        [0, 1, 0, 1, 0, ...],
        [0, 0, 0, 1, 0, ...],
        ...
        [..., 0, 0, 0, 3]
    ]
    ```

## 5. Deliverable

A single Python file (`mazerunner_game.py`) containing the complete, runnable game.
