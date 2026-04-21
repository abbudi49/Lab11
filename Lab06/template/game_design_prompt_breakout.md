# Prompt for Generating a Breakout Game

## 1. Objective

Create a complete, single-file Python application for a classic **Breakout** (Brick Breaker) game using the **Pygame** library. The game should be easy to run and control, featuring a clean and visually appealing interface.

## 2. Core Gameplay Mechanics

*   **Game World / Environment:**
    *   The game is played in a rectangular window.
    *   Window dimensions: **800x600 pixels**.
    *   The play area is bounded by walls on the top, left, and right sides.

*   **Player Paddle:**
    *   A horizontal paddle at the bottom of the screen.
    *   Paddle dimensions: **100x15 pixels**.
    *   Movement controls: **Left Arrow (move left) and Right Arrow (move right)** or **'A' (left) and 'D' (right)**.
    *   The paddle cannot move off-screen.

*   **The Ball:**
    *   A single ball starts on top of the paddle.
    *   Ball size: **10x10 pixels** (square or circle).
    *   Press **Space** to launch the ball.
    *   The ball bounces off the top, left, and right walls.
    *   The ball bounces off the paddle and bricks.
    *   If the ball falls below the paddle, the player loses a life.

*   **Bricks:**
    *   Bricks are arranged in rows at the top of the screen.
    *   Create **5 rows** of bricks with **10 bricks per row**.
    *   Each brick is **75x20 pixels**.
    *   When the ball hits a brick, the brick disappears.
    *   Bricks can have different colors based on their row (red, orange, yellow, green, blue).

*   **Lives:**
    *   The player starts with **3 lives**.
    *   Lose a life when the ball falls below the paddle.
    *   When a life is lost, the ball resets on the paddle.

*   **Scoring / Progression:**
    *   Starting score: **0**.
    *   Each brick destroyed: **+10 points**.
    *   Top row bricks can be worth more: **+20 points**.

*   **Win / Loss Conditions:**
    *   **Win:** All bricks are destroyed. Display "YOU WIN!" message.
    *   **Loss:** The player runs out of lives. Display "GAME OVER" message.

*   **Game Flow:**
    *   Can restart after win/loss by pressing the **'R' key**.
    *   Can pause the game by pressing **'P' key**.

## 3. GUI (Graphical User Interface)

*   **Art Style & Graphics:**
    *   Simple, clean, 2D graphics.
    *   Paddle appearance: **White rectangle**.
    *   Ball appearance: **White circle or square**.
    *   Brick appearance: **Colored rectangles with a subtle border/shadow for depth**.
    *   Background: **Black or dark blue**.

*   **User Interface (UI):**
    *   Display the current score in the **top-left corner**.
    *   Display the number of lives remaining in the **top-right corner** (e.g., "Lives: 3").

*   **Sound & Music:**
    *   No sound required.

## 4. Code Structure and Implementation

*   **Language and Library:**
    *   Use Python 3.
    *   Use the **`pygame`** library.

*   **Structure:**
    *   Organize the code within a **`BreakoutGame`** class to encapsulate all game-related logic and data.
    *   Use constants for key game parameters (window dimensions, colors, paddle size, ball speed, brick layout, etc.).
    *   Create separate methods for handling user input, updating the game state, and rendering.
    *   Include a main game loop that controls the flow of the game.
    *   The code should be well-commented to explain the logic.

## 5. Deliverable

A single Python file (`breakout_game.py`) containing the complete, runnable game.
