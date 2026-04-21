# Prompt for Generating a Flappy Bird Game

## 1. Objective

Create a complete, single-file Python application for a **Flappy Bird** style game using the **Pygame** library. The game should be easy to run and control, featuring a clean and visually appealing interface.

## 2. Core Gameplay Mechanics

*   **Game World / Environment:**
    *   The game is played in a side-scrolling window.
    *   Window dimensions: **400x600 pixels**.
    *   The background should scroll to create the illusion of forward movement.

*   **Player Character (Bird):**
    *   The bird is represented as a **circle or small sprite** (30x30 pixels).
    *   Starting position: **Left side of the screen, vertically centered**.
    *   The bird is affected by gravity and constantly falls downward.
    *   Movement control: **Press Space or Up Arrow to flap and move upward**.
    *   Each flap gives the bird an upward velocity boost.

*   **Obstacles (Pipes):**
    *   Vertical pipes appear from the right side of the screen and scroll left.
    *   Each obstacle consists of a **top pipe and bottom pipe with a gap** in between.
    *   Gap size: **150 pixels** (enough for the bird to pass through).
    *   Pipe width: **70 pixels**.
    *   Pipes appear at regular intervals (e.g., every 1.5 seconds).
    *   The vertical position of the gap should vary randomly.

*   **Scoring / Progression:**
    *   Starting score: **0**.
    *   Each pipe successfully passed: **+1 point**.
    *   The game speed can gradually increase as the score increases (optional enhancement).

*   **Win / Loss Conditions:**
    *   **Loss:** The bird collides with a pipe, the ground, or the ceiling.
    *   What happens on game over: **A "GAME OVER" message is displayed with the final score**.
    *   There is no explicit win condition; the goal is to achieve the highest score.

*   **Game Flow:**
    *   The player can restart after a game over by pressing the **'R' key**.
    *   The player can pause the game by pressing **'P' key**.

## 3. GUI (Graphical User Interface)

*   **Art Style & Graphics:**
    *   Simple, clean, 2D graphics with a cartoony feel.
    *   Bird appearance: **A yellow circle with a small black eye, or a simple bird sprite**.
    *   Pipe appearance: **Green rectangles**.
    *   Background: **Light blue sky color, optionally with cloud decorations**.
    *   Ground: **A brown or green bar at the bottom of the screen**.

*   **User Interface (UI):**
    *   Display the current score in the **top-center** of the screen in large, clear font.
    *   Display "Press SPACE to start" message before the game begins.

*   **Sound & Music:**
    *   No sound required.

## 4. Code Structure and Implementation

*   **Language and Library:**
    *   Use Python 3.
    *   Use the **`pygame`** library.

*   **Structure:**
    *   Organize the code within a **`FlappyBirdGame`** class to encapsulate all game-related logic and data.
    *   Use constants for key game parameters (window dimensions, colors, gravity, flap strength, pipe speed, etc.).
    *   Create separate methods for handling user input, updating the game state (bird physics, pipe scrolling, collision detection), and rendering.
    *   Include a main game loop that controls the flow of the game.
    *   The code should be well-commented to explain the logic.

## 5. Deliverable

A single Python file (`flappybird_game.py`) containing the complete, runnable game.
