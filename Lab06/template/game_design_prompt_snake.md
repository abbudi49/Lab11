## 1. Objective

Create a complete, single-file Python application for a classic Snake game using the Pygame library. The game should be easy to run and control, featuring a clean and visually appealing interface.

## 2. Core Gameplay Mechanics

*   **Game Board:**
    *   The game should be played on a grid-based window.
    *   Window dimensions: 800x600 pixels.
    *   Grid size: 20x20 pixels.

*   **Snake:**
    *   The snake starts in the center of the screen, moving horizontally.
    *   The snake is composed of square segments, fitting the grid.
    *   The snake's head should be a distinct color from its body.
    *   The snake continuously moves in its current direction.
    *   The player can change the snake's direction using WASD keys.
    *   The snake cannot reverse its direction (e.g., from moving right to moving left).

*   **Food:**
    *   Food items appear at random locations on the grid.
    *   There should be multiple food items on the screen at once (e.g., 3).
    *   When the snake eats a food item, it grows longer by one segment.
    *   A new food item should appear at a random location after one is eaten.
    *   Food should not spawn on top of the snake.

*   **Scoring:**
    *   The player's score starts at 0.
    *   Each food item eaten increases the score by 10 points.

*   **Game Over:**
    *   The game ends if the snake collides with the boundaries of the window.
    *   The game ends if the snake collides with its own body.
    *   When the game is over, a "GAME OVER" message should be displayed prominently in the center of the screen.

*   **Restarting:**
    *   After a game over, the player can restart the game by pressing the 'R' key.

## 3. GUI

*   **Graphics:**
    *   Use simple, clean, 2D graphics.
    *   The snake should be green, with a brighter green for the head.
    *   Food items should be visually distinct, with a 3D-like effect (e.g., a circle with a shadow and highlight).
    *   The background should be black.

*   **User Interface (UI):**
    *   Display the current score in the top-left corner of the screen.
    *   Display the number of food items currently on the screen below the score.

*   **Sound:**
    *   No.

## 4. Code Structure and Implementation

*   **Language and Library:**
    *   Use Python 3.
    *   Use the `pygame` library.

*   **Structure:**
    *   Organize the code within a `SnakeGame` class to encapsulate all game-related logic and data.
    *   Use constants for key game parameters like window dimensions, grid size, colors, etc.
    *   Create separate methods for handling user input, updating the game state, and rendering the game.
    *   Include a main game loop that controls the flow of the game.
    *   The code should be well-commented to explain the logic.

## 5. Deliverable

A single Python file (`snake_game.py`) containing the complete, runnable game.